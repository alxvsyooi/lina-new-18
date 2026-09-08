import re, base64, mimetypes

with open('_source.html', 'r', encoding='utf-8') as f:
    src = f.read()

SKIP_EXT = ('.mp3', '.wav', '.ogg', '.m4a')

def repl(m):
    path = 'assets/' + m.group(1)
    if path.lower().endswith(SKIP_EXT):
        print('SKIP (audio, too big for Artifact inline):', path)
        return m.group(0)
    try:
        with open(path, 'rb') as af:
            data = af.read()
    except FileNotFoundError:
        print('WARNING: missing asset, left as-is:', path)
        return m.group(0)
    mime = mimetypes.guess_type(path)[0] or 'application/octet-stream'
    b64 = base64.b64encode(data).decode('ascii')
    return f'data:{mime};base64,{b64}'

out = re.sub(r'assets/([\w.-]+)', repl, src)

with open('_inlined.html', 'w', encoding='utf-8') as f:
    f.write(out)

print('done', len(out))
