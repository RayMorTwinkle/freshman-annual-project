from pathlib import Path
from collections import Counter
import csv,json,hashlib,subprocess
from PIL import Image,ImageStat
root=Path('/content/drive/MyDrive/大一年度项目复现/补充素材')
manifest=json.loads((root/'manifest.json').read_text())
print('Manifest type:',type(manifest).__name__)
entries=manifest if isinstance(manifest,list) else manifest.get('files',manifest.get('entries'))
assert entries and len(entries)==27,(type(manifest),list(manifest)[:5])
counts=Counter()
for row in entries:
    p=root/row['file'];assert p.is_file() and p.stat().st_size>0,p
    counts[p.suffix]+=1
    if p.suffix=='.png':
        with Image.open(p) as im:
            assert min(im.size)>500,(p.name,im.size)
            assert max(ImageStat.Stat(im.convert('RGB')).stddev)>10,p.name
        with Image.open(p) as im:
            im.verify()
assert counts=={'.png':22,'.csv':3,'.txt':2},counts
for name in ['R4-data-structure.csv','S2-latency-by-episode.csv','S4-instruction-components.csv']:
    rows=list(csv.DictReader((root/name).open()))
    print(name, len(rows),'rows',list(rows[0]))
    assert len(rows)=={'R4-data-structure.csv':8,'S2-latency-by-episode.csv':3,'S4-instruction-components.csv':6}[name]
result={'status':'passed','files':len(entries),'counts':dict(counts),'sha256':{r['file']:hashlib.sha256((root/r['file']).read_bytes()).hexdigest() for r in entries}}
(root/'validation.json').write_text(json.dumps(result,indent=2))
(root/'cpu-environment-freeze.txt').write_text(subprocess.run(['python','-m','pip','freeze'],capture_output=True,text=True,check=True).stdout)
print('VALIDATED:',dict(counts),len(entries),'artifacts. Validation and environment archived on Drive.')
