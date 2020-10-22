import os
import subprocess
import re
import json

for filename in os.listdir('data'):
    print filename
    output = subprocess.check_output('pdfsig data/' + filename, shell = True)
    m = re.search('- Signing Time:\s+(.+)', output)
    d = dict()
    if m:
        d['SignatureTimestamp'] = m.group(1)
    output = subprocess.check_output('pdfinfo data/' + filename, shell = True)
    m = re.search('CreationDate:\s+(.+)', output)
    if m:
        d['CreationTimestamp'] = m.group(1)
    open('extracted/' + filename, 'wb').write(json.dumps(d))
