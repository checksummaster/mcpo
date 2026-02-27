from pathlib import Path
path = Path('README.md')
text = path.read_text(encoding='utf-8')
if '\x08' in text:
    text = text.replace('\x08', '')
    with path.open('w', encoding='utf-8', newline='\r\n') as fh:
        fh.write(text)
