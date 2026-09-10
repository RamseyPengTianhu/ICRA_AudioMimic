"""Gallery-independent shared readouts for calibration, retrieval and generation."""
from __future__ import annotations

import numpy as np
import torch

SCORE_VERSION = "mmr_g1_plus_posterior_mean_cosine_5s_stride1_v1"
TIE_ATOL = 1e-7
NORM_MIN = 1e-6


def cosine(left, right):
    left, right = np.asarray(left, dtype=np.float64), np.asarray(right, dtype=np.float64)
    nl, nr = np.linalg.norm(left, axis=-1), np.linalg.norm(right, axis=-1)
    if not np.isfinite(left).all() or not np.isfinite(right).all() or np.any(nl < NORM_MIN) or np.any(nr < NORM_MIN):
        raise ValueError("nonfinite/collapsed posterior mean; inspect latent norms")
    return np.sum(left*right, axis=-1)/(nl*nr)


def readout(music, motion, kind="cosine5"):
    """Leading dimensions are windows, then (for 1s) five segments, then latent."""
    music, motion = np.asarray(music, dtype=np.float64), np.asarray(motion, dtype=np.float64)
    if kind in ("cosine5", "cosine1"):
        values = cosine(music, motion)
        return values.mean(-1) if kind == "cosine1" else values
    if kind in ("l2_5", "l2_1"):
        values = -np.square(music-motion).sum(-1)
        return values.mean(-1) if kind == "l2_1" else values
    if kind == "ms":
        feature = np.square(music-motion).sum(-1).mean(-1)
        dynamics = np.linalg.norm(np.diff(motion, axis=-2)-np.diff(music, axis=-2), axis=-1).sum(-1)
        return -np.sqrt(.7*feature + .3*dynamics)
    raise ValueError(kind)


def preference(delta):
    delta = np.asarray(delta)
    return np.where(delta > TIE_ATOL, 1., np.where(delta < -TIE_ATOL, 0., .5))


def interaction(scores):
    scores = np.asarray(scores, dtype=np.float64)
    return .5*(scores[..., 0, 0]+scores[..., 1, 1]-scores[..., 0, 1]-scores[..., 1, 0])


@torch.no_grad()
def encode_windows(model, music, motion, *, seconds=5, batch_size=128):
    device = next(model.parameters()).device
    music, motion = torch.as_tensor(music), torch.as_tensor(motion)
    if tuple(music.shape[1:]) != (150, 4800) or tuple(motion.shape[1:]) != (100, 357):
        raise ValueError("encoder inputs must be complete five-second windows")
    n = len(music)
    if seconds == 1:
        music, motion = music.reshape(-1, 30, 4800), motion.reshape(-1, 20, 357)
    elif seconds != 5:
        raise ValueError("seconds must be 1 or 5")
    out = [[], []]
    model.eval()
    for start in range(0, len(music), batch_size):
        for tower, values in enumerate((music, motion)):
            x = values[start:start+batch_size].to(device=device, dtype=torch.float32)
            mask = torch.ones(x.shape[:2], dtype=torch.bool, device=device)
            encoder = model.encode_music if tower == 0 else model.encode_motion
            # FP32 inference is fixed for every readout and both training families.
            z, _ = encoder(x, mask, sample_mean=True)
            out[tower].append(z.float().cpu().numpy())
    result = [np.concatenate(x) for x in out]
    return tuple(x.reshape(n, 5, -1) if seconds == 1 else x for x in result)


def score_pair(models, music, motion, *, kind="cosine5"):
    """Normalized continuous features; never normalize, crop or reset per candidate gallery."""
    music, motion = np.asarray(music), np.asarray(motion)
    seconds = min(len(music)/30, len(motion)/20)
    starts = list(range(max(0, int(np.floor(seconds-5+1e-8))+1)))
    if not starts:
        return {"score_version": SCORE_VERSION, "readout": kind, "status": "not_applicable", "windows": 0}
    a = np.stack([music[s*30:s*30+150] for s in starts])
    x = np.stack([motion[s*20:s*20+100] for s in starts])
    scores = [readout(*encode_windows(m, a, x, seconds=1 if kind in ("ms", "cosine1", "l2_1") else 5), kind)
              for m in models]
    values = np.mean(scores, axis=0)
    return {"score_version": SCORE_VERSION, "readout": kind, "score": float(values.mean()),
            "window_scores": values.tolist(), "windows": len(starts), "seconds": seconds,
            "coverage": (starts[-1]+5)/seconds}
