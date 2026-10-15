#!/usr/bin/env python3
"""The call brief as one page, built from jobs/<id>/call-prep.md.

    python3 code/call_prep_page.py <job_id> [--open]

/sales-call-prep writes call-prep.md, the checked source. This renders it as the one
page a member glances at during the call: the client and the job on top, the seven
stops of the call in one column in the order they are said, and under them, side by side, a few facts about the
business and the person under them. Nothing on it has to be studied first. The sources
fold away at the foot.

Output is `call-prep.html` beside the brief, in the member's job folder and gitignored
like it. It is built from that one file and reaches no service. The look is the
stylesheet of `code/context_page.py` on the tokens in `website/app/tokens.css`, the
sheet every page in this repository shares; only the stops are styled here.
"""
import argparse
import html
import re
import sys
import pathlib
import webbrowser

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'code'))
import call_prep  # noqa: E402  (the shape of the brief: HEADINGS, STOPS)
import context_page as cp  # noqa: E402  (the shared sheet)
import pipeline  # noqa: E402  (read-only use: jobs_dir)

STOPS = call_prep.STOPS
ID = re.compile(r'^[0-9]{6,25}$')
LINK = re.compile(r'\[([^\]\n]+)\]\(([^)\s]+)\)')
SAFE_URL = re.compile(r'^(?:https?://[^\s"<>]+|[\w][\w./-]*)$')

CSS = """
  .bar, .sheet, .foot { max-width: 860px; }
  .bar { padding: 16px 6px 10px; }
  .sheet { padding: 28px 44px 26px; }
  .kicker { margin-bottom: 6px; }
  h1 { font-size: clamp(30px, 3.4vw, 42px); letter-spacing: -1px; }
  .headline { font-size: 16px; margin-top: 6px; max-width: none; }
  .lead { margin: 10px 0 0; max-width: 62em; } .lead li { font-size: 14px; line-height: 1.5; color: var(--body); }
  section { padding-top: 20px; } h2 { margin-bottom: 10px; }
  .stop { break-inside: avoid; display: grid; grid-template-columns: 40px 1fr; gap: 0 14px; padding: 0 0 12px; }
  .stop .n { width: 36px; height: 36px; border-radius: 50%; display: grid; place-items: center;
             background: var(--terracotta-soft); color: var(--terracotta-text); font: 500 17px/1 var(--display);
             box-shadow: inset 0 0 0 1px rgba(201, 100, 66, .22); }
  .stop h3 { margin: 6px 0 2px; font: 500 19px/1.2 var(--display); letter-spacing: -.3px; }
  .stop li { position: relative; padding: 2px 0 2px 15px; font-size: 14.5px; line-height: 1.4; color: var(--ink); }
  .stop li::before { content: ""; position: absolute; left: 0; top: 10px; width: 5px; height: 5px; border-radius: 50%; background: var(--terracotta); }
  .stop.skip .n { background: none; color: var(--label); box-shadow: none; border: 1px dashed var(--ring); }
  .stop.skip h3, .stop.skip li { color: var(--label); }
  .stop.skip h3::after { content: "optional"; margin-left: 10px; font: 400 10px/1 var(--mono); letter-spacing: 1.4px; text-transform: uppercase; color: var(--label); }
  .known { display: grid; grid-template-columns: 1fr 1fr; gap: 0 40px; }
  .group h3 { margin: 0 0 6px; font: 400 10px/1.6 var(--mono); letter-spacing: 1.4px; text-transform: uppercase; color: var(--terracotta-active); }
  .facts li { padding: 5px 0; border-top: 1px solid var(--hairline); font-size: 13.5px; line-height: 1.45; color: var(--body); }
  .facts li:first-child { border-top: 0; padding-top: 0; }
  a { color: var(--terracotta-text); text-decoration: underline; text-underline-offset: 2px; }
  details { margin-top: 18px; } summary { cursor: pointer; font: 400 11px/1 var(--mono); letter-spacing: 2.2px; text-transform: uppercase; color: var(--label); }
  details li { padding: 3px 0; font-size: 12.5px; word-break: break-all; }
  @media (max-width: 880px) { .known { grid-template-columns: 1fr; } }
  @media print { .stop li, .facts li { font-size: 9px; } .stop h3 { font-size: 12px; } details { display: none; } }
"""


class NotReady(Exception):
    """The brief is missing or is not in the shape this page reads."""


def inline(text):
    """Escaped text with its markdown links and **bold** kept. A link that is not a web
    address or a file beside the brief is left as plain words: nothing here may run."""
    out, last = [], 0
    for match in LINK.finditer(text):
        out.append(bold(text[last:match.start()]))
        label, url = match.group(1), match.group(2)
        out.append(f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener">{cp.esc(label)}</a>'
                   if SAFE_URL.fullmatch(url) else cp.esc(label))
        last = match.end()
    out.append(bold(text[last:]))
    return ''.join(out)


def bold(text):
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', cp.esc(text))


def split(text, level):
    """The parts of a text under each heading of one level, in order, with what stands before the first."""
    marks = list(re.finditer(rf'^{"#" * level}[ \t]+(.+?)[ \t]*$', text, re.M))
    head = text[:marks[0].start()] if marks else text
    parts = [(mark.group(1), text[mark.end():marks[i + 1].start() if i + 1 < len(marks) else len(text)])
             for i, mark in enumerate(marks)]
    return head, parts


def bullets(text):
    return [line.strip()[2:].strip() for line in text.splitlines() if re.match(r'^\s*[-*]\s+\S', line)]


def items(lines, classes=''):
    return f'<ul{f" class={chr(34)}{classes}{chr(34)}" if classes else ""}>' + ''.join(f'<li>{inline(line)}</li>' for line in lines) + '</ul>'


def stop_html(number, name, lines):
    skip = bool(lines) and lines[0].lower().startswith('skip it')
    return (f'<div class="stop{" skip" if skip else ""}"><span class="n">{number}</span><div><h3>{cp.esc(name)}</h3>'
            + items(lines) + '</div></div>')


def build(text):
    head, sections = split(text, 2)
    found = dict(sections)
    stops = split(found.get('The call, in order', ''), 3)[1]
    wanted = [f'{number} · {name}' for number, name in enumerate(STOPS, 1)]
    if [name for name, _ in sections] != call_prep.HEADINGS or [name for name, _ in stops] != wanted:
        raise NotReady('call-prep.md is not in the seven-stop shape. Run /sales-call-prep <job id> again to rewrite it.')
    title = next((line[2:].strip() for line in head.splitlines() if line.startswith('# ')), 'Call prep')
    parts = [part.strip() for part in title.split('·')]
    client = parts[1] if len(parts) > 1 else title
    job = ' · '.join(parts[2:])
    lead = [line.strip() for line in head.splitlines() if line.strip() and not line.startswith('#')]
    groups = ''.join(f'<div class="group"><h3>{cp.esc(name)}</h3>{items(bullets(body), "facts")}</div>'
                     for name, body in split(found['What we know'], 3)[1] if bullets(body))
    sources = bullets(found['Sources'])
    block = lambda name, inner: f'<section><h2>{cp.esc(name)}</h2>{inner}</section>' if inner else ''
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{cp.esc(client)} · Call prep</title>\n<style>' + cp.tokens() + cp.CSS + CSS + '</style>\n</head>\n<body>\n'
            '<div class="bar"><span>Call prep</span></div>\n<main class="sheet">\n'
            f'<p class="kicker">Call prep</p><h1>{cp.esc(client)}</h1>'
            + (f'<p class="headline">{cp.esc(job)}</p>' if job else '') + items(lead, 'lead') + '\n'
            + block('The call, in order', '<div class="stops">' + ''.join(
                stop_html(number, name.split('·', 1)[1].strip(), bullets(body))
                for number, (name, body) in enumerate(stops, 1)) + '</div>')
            + '\n' + block('What we know', f'<div class="known">{groups}</div>' if groups else '') + '\n'
            + ('<details><summary>Sources</summary>' + items([f'[{url}]({url})' for url in sources]) + '</details>' if sources else '')
            + '\n</main>\n<p class="foot">The call runs on Upwork\'s video, and no contact details or payment change hands off Upwork. '
            'Built from call-prep.md on this machine: it sends nothing.</p>\n'
            '</body>\n</html>\n')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('job_id')
    parser.add_argument('--open', action='store_true', help='open it in the browser')
    args = parser.parse_args(argv)
    if not ID.fullmatch(args.job_id):
        print('ABORT: that job id is not valid.')
        return 1
    folder = pipeline.jobs_dir() / args.job_id
    source, target = folder / 'call-prep.md', folder / 'call-prep.html'
    try:
        page = build(source.read_text(encoding='utf-8'))
    except (OSError, UnicodeError):
        print(f'ABORT: no call brief for {args.job_id} yet. /sales-call-prep {args.job_id} writes it.')
        return 1
    except NotReady as problem:
        print(f'ABORT: {problem}')
        return 1
    target.write_text(page, encoding='utf-8')
    print(f'{pipeline.shown(target)} written')
    if args.open:
        webbrowser.open(target.as_uri())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
