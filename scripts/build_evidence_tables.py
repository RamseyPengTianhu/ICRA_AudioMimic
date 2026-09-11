"""Regenerate populated paper tables from fetched, immutable evaluation summaries."""
from pathlib import Path
import json, hashlib, re
root=Path(__file__).resolve().parents[1]
p=root/'evidence/foredance'
q=json.loads((p/'motion-quality.json').read_text())
rows=[]
for startup in ['AM']:
 histories=[('HCLEAN','Clean history')]
 if startup=='AM':histories.append(('HDROP','History dropout'))
 histories.append(('FHC','History corruption'))
 for hist,hlabel in histories:
  mean=q['routes'][f'FD-DF-L-{startup}-{hist}']['mean']
  vals=[mean[k] for k in ['FIDk-G1','FIDg-G1','Divk-G1','Divg-G1','G1FKRoboPerformBAS','PFC-G1']]
  cells=[f'{v:.4f}' if i==4 else f'{v:.3f}' for i,v in enumerate(vals)]
  rows.append(f"{hlabel} & "+' & '.join(cells)+r' \\')
(p/'training_rows.tex').write_text('\n'.join(rows)+'\n')
calibration=p/'mmr-accepted/source/docs/experiments/reviews/EXP-20260907-mmr-g1-plus-correspondence-candidate-selection.md'
match=re.search(r'^\| 1 \| R_cosine5 \| ([0-9.]+) \| ([0-9.]+) \| ([0-9.]+) \| ([0-9.]+) \|$',calibration.read_text(),re.M)
assert match, 'Missing accepted evaluator calibration row'
ordinary,confusing=map(float,match.groups()[2:])
(p/'evaluator_validation_rows.tex').write_text(
 f"Ordinary alternative music & {ordinary:.2f} "+r'\\'+'\n'+
 f"Similar alternative music & {confusing:.2f} "+r'\\'+'\n')
execution=p/'team-execution'
tracking=json.loads((execution/'tracking.json').read_text())
source=(execution/'teammate-main-20260908.tex').read_bytes()
assert hashlib.sha256(source).hexdigest()==tracking['source_sha256']
table=source.decode().split('\\label{tab:tracking_retention}',1)[1].split('\\end{table}',1)[0]
original=re.findall(r'^([ABCD]) & ([0-9.]+) & ([0-9.]+) & ([0-9.]+)',table,re.M)
assert len(original)==len(tracking['rows'])==4
rows=[]
for (key,rmse,amp,dyn),record in zip(original,tracking['rows']):
 assert key==record['source_id']
 assert [float(rmse),float(amp),float(dyn)]==[record['aligned_rmse_rad'],record['median_amplitude_retention'],record['median_squared_velocity_retention']]
 rows.append(f"{record['label']} & {rmse} & {amp} & {dyn} "+r' \\')
(execution/'tracking_rows.tex').write_text('\n'.join(rows)+'\n')
manifest=json.loads((p/'SHA256SUMS.json').read_text())
for f in p.rglob('*.json'):
 if f.name != 'SHA256SUMS.json':manifest[str(f.relative_to(p))]=hashlib.sha256(f.read_bytes()).hexdigest()
(p/'SHA256SUMS.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print('Verified generation tables and archived execution-table transcription; generated motion-quality and execution tables.')
