"""Matched R/H five-second cosine comparison on the same archived motions."""
import json

import numpy as np

from scripts.rescore_mmr_generators import ROOT, ROUTES, SEEDS, summary


def main():
    sources = [json.loads((ROOT / folder / 'source-manifest.json').read_text())
               for folder in ('generator-rescore', 'generator-rescore-H-cosine5')]
    if sources[0] != sources[1]:
        raise ValueError('different source manifests')
    reports = {}
    for family, folder in [('R', 'generator-rescore'), ('H', 'generator-rescore-H-cosine5')]:
        path = ROOT / folder
        if (path / 'run.exit').read_text().strip() != '0':
            raise ValueError(f'incomplete run: {family}')
        report = json.loads((path / 'aggregate.json').read_text())
        for route in ROUTES:
            for train in SEEDS:
                for sample in SEEDS:
                    scores = np.load(path / f'{route}_train{train}_sample{sample}_scores.npz')['pair_scores']
                    if scores.shape != (11, 11, 56) or not np.isfinite(scores).all():
                        raise ValueError('invalid pair matrices')
                    rows = [r for r in report['records'] if r['route'] == route
                            and r['training_seed'] == train and r['sampling_seed'] == sample]
                    if len(rows) != 11:
                        raise ValueError('missing tracks')
                    for i, row in enumerate(rows):
                        correct = scores[i, i]
                        wrong = np.delete(scores[:, i], i, axis=0)
                        delta = correct[None] - wrong
                        actual = [correct.mean(), wrong.mean(), delta.mean(),
                                  100 * np.where(delta > 1e-7, 1, np.where(delta < -1e-7, 0, .5)).mean()]
                        np.testing.assert_allclose(actual, [row[k] for k in
                            ('score', 'wrong_track_score', 'margin', 'preference_accuracy')], atol=1e-7)
        reports[family] = report
    keys = ('route', 'training_seed', 'sampling_seed', 'sequence_id', 'track')
    if [[r[k] for k in keys] for r in reports['R']['records']] != [[r[k] for k in keys] for r in reports['H']['records']]:
        raise ValueError('unmatched generator records')
    result = {'comparison': 'H_cosine5 minus R_cosine5; fixed gallery, matched motions',
              'audit': '396 records verified against 36 pair-score matrices', 'results': {}}
    for route in ROUTES:
        result['results'][route] = {}
        for metric in ('score', 'wrong_track_score', 'margin', 'preference_accuracy'):
            values = {f: np.array([r[metric] for r in reports[f]['records'] if r['route'] == route]).reshape(3, 3, 11)
                      for f in ('R', 'H')}
            for f in ('R', 'H'):
                computed = summary(values[f])
                expected = reports[f]['results'][route][metric]
                np.testing.assert_allclose(computed['mean'], expected['mean'])
                np.testing.assert_allclose(computed['ci95'], expected['ci95'])
            result['results'][route][metric] = {'R': reports['R']['results'][route][metric],
                'H': reports['H']['results'][route][metric], 'H_minus_R': summary(values['H'] - values['R'])}
    output = ROOT / 'generator-rescore-H-cosine5/comparison.json'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
