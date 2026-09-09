"""Regenerate populated paper tables from fetched, immutable evaluation summaries."""
from pathlib import Path
import json, hashlib, re
root=Path(__file__).resolve().parents[1]
p=root/'evidence/foredance'
a=json.loads((p/'condition-analysis.json').read_text())
q=json.loads((p/'motion-quality.json').read_text())
rows=[]
for startup,label in [('AM','Mixed-start'),('AJ','Continuation-start')]:
 route=f'FD-DF-L-{startup}-FHC'
 v=a['conditioned_minus_trained_no_music'][route]['mmr_ms']
 mean=q['routes'][route]['mean']['MMR-MS']
 baseline=q['routes'][route+'-NM']['mean']['MMR-MS']
 assert abs((baseline-mean)-v['point'])<1e-8
 assert v['training_seeds']==3 and v['paired_cells']==162
 rows.append(f"{label} & {v['point']:.3f} & [{v['ci95'][0]:.3f}, {v['ci95'][1]:.3f}] \\\\")
(p/'music_use_rows.tex').write_text('\n'.join(rows)+'\n')
rows=[]
for startup,label in [('AM','Mixed-start'),('AJ','Continuation-start')]:
 for hist,hlabel in [('HCLEAN','Clean history'),('FHC','History corruption')]:
  mean=q['routes'][f'FD-DF-L-{startup}-{hist}']['mean']
  vals=[mean[k] for k in ['MMR-MS','FIDk-G1','FIDg-G1','Divk-G1','Divg-G1','PFC-G1']]
  rows.append(f"{label} & {hlabel} & "+' & '.join(f'{v:.3f}' for v in vals)+r' \\')
(p/'training_rows.tex').write_text('\n'.join(rows)+'\n')
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
manifest={str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in p.rglob('*.json') if f.name != 'SHA256SUMS.json'}
(p/'SHA256SUMS.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Verified generation tables and archived execution-table transcription; generated three tables.')
