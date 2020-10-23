import os
import subprocess
import re
import json

for filename in os.listdir('data/bgbl'):
    if (os.path.splitext(filename)[1] == '.html'):
        continue
    if (os.path.exists('data/extracted/' + os.path.splitext(filename)[0])):
        continue
    print(filename)
    output = subprocess.check_output('pdfsig data/bgbl/' + filename, shell = True).decode('utf-8')
    m = re.search('- Signing Time:\s+(.+)', output)
    d = {}
    if m:
        d['SignatureTimestamp'] = m.group(1)
    output = subprocess.check_output('pdfinfo data/bgbl/' + filename, shell = True).decode('utf-8')
    m = re.search('CreationDate:\s+(.+)', output)
    if m:
        d['CreationTimestamp'] = m.group(1)
    output = open('data/bgbl/' + os.path.splitext(filename)[0] + '.html').read()
    timestamps = set()
    m = re.findall('(tritt|treten) mit (.+?) (in|außer) Kraft', output)
    if m:
        for g in m:
            if (g[2] == 'in'):
                timestamps.add(g[1])
    d['LegalValidityTimestamp'] = list(timestamps)
    open('data/extracted/' + os.path.splitext(filename)[0], 'w').write(json.dumps(d, ensure_ascii=False))
