#!/usr/bin/env python3
"""
Generate Excalidraw diagram files for Phil documentation.
Outputs .excalidraw JSON files to assets/diagrams/.
"""

import json, random, os

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'diagrams')

# ── Color palette (matches site CSS variables) ────────────────────────────────
C = dict(
    bg='#0d1117', surface='#161b22', border='#30363d', text='#f0f6fc',
    muted='#7d8590', accent='#f0a500', green='#3fb950', blue='#58a6ff',
    purple='#bc8cff', red='#f85149',
)


def uid():
    return ''.join(random.choices(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=20))


def _b():
    return dict(
        angle=0, strokeWidth=2, strokeStyle='solid', roughness=0, opacity=100,
        groupIds=[], frameId=None, roundness=None,
        seed=random.randint(1, 2**31), version=1,
        versionNonce=random.randint(1, 2**31), isDeleted=False,
        boundElements=[], updated=1700000000000, link=None, locked=False,
    )


# ── Element factories ─────────────────────────────────────────────────────────

def rect(x, y, w, h, lbl='', stroke=None, fill=None, fc=None, fs=15, rounded=True):
    """Rectangle with optional centered label."""
    rid = uid()
    el = {**_b(), 'id': rid, 'type': 'rectangle',
          'x': x, 'y': y, 'width': w, 'height': h,
          'strokeColor': stroke or C['border'],
          'backgroundColor': fill or C['surface'],
          'fillStyle': 'solid', 'boundElements': []}
    if rounded:
        el['roundness'] = {'type': 3}
    els = [el]
    if lbl:
        tid = uid()
        te = {**_b(), 'id': tid, 'type': 'text',
              'x': x, 'y': y, 'width': w, 'height': h,
              'text': lbl, 'originalText': lbl,
              'fontSize': fs, 'fontFamily': 1,
              'textAlign': 'center', 'verticalAlign': 'middle',
              'lineHeight': 1.25,
              'strokeColor': fc or C['text'],
              'backgroundColor': 'transparent', 'fillStyle': 'solid',
              'containerId': rid, 'boundElements': []}
        el['boundElements'].append({'type': 'text', 'id': tid})
        els.append(te)
    return els, rid


def diamond(x, y, w, h, lbl='', stroke=None, fill=None, fc=None, fs=14):
    did = uid()
    el = {**_b(), 'id': did, 'type': 'diamond',
          'x': x, 'y': y, 'width': w, 'height': h,
          'strokeColor': stroke or C['accent'],
          'backgroundColor': fill or C['surface'],
          'fillStyle': 'solid', 'boundElements': []}
    els = [el]
    if lbl:
        tid = uid()
        te = {**_b(), 'id': tid, 'type': 'text',
              'x': x, 'y': y, 'width': w, 'height': h,
              'text': lbl, 'originalText': lbl,
              'fontSize': fs, 'fontFamily': 1,
              'textAlign': 'center', 'verticalAlign': 'middle',
              'lineHeight': 1.25,
              'strokeColor': fc or C['text'],
              'backgroundColor': 'transparent', 'fillStyle': 'solid',
              'containerId': did, 'boundElements': []}
        el['boundElements'].append({'type': 'text', 'id': tid})
        els.append(te)
    return els, did


def txt(x, y, s, fs=13, color=None, align='left'):
    tid = uid()
    lines = s.count('\n') + 1
    el = {**_b(), 'id': tid, 'type': 'text',
          'x': x, 'y': y,
          'width': max(len(s.replace('\n', '')) * fs * 0.62, 40),
          'height': fs * 1.4 * lines,
          'text': s, 'originalText': s,
          'fontSize': fs, 'fontFamily': 1,
          'textAlign': align, 'verticalAlign': 'top',
          'lineHeight': 1.4,
          'strokeColor': color or C['muted'],
          'backgroundColor': 'transparent', 'fillStyle': 'solid',
          'boundElements': []}
    return [el], tid


def arr(x1, y1, x2, y2, color=None, dashed=False, bidir=False):
    aid = uid()
    el = {**_b(), 'id': aid, 'type': 'arrow',
          'x': x1, 'y': y1,
          'width': abs(x2 - x1), 'height': abs(y2 - y1),
          'points': [[0, 0], [x2 - x1, y2 - y1]],
          'lastCommittedPoint': None,
          'startBinding': None, 'endBinding': None,
          'startArrowhead': 'arrow' if bidir else None,
          'endArrowhead': 'arrow',
          'strokeColor': color or C['muted'],
          'backgroundColor': 'transparent', 'fillStyle': 'solid',
          'strokeStyle': 'dashed' if dashed else 'solid',
          'boundElements': []}
    return [el], aid


def save_diagram(name, els):
    path = os.path.join(OUT_DIR, f'{name}.excalidraw')
    doc = {
        'type': 'excalidraw', 'version': 2,
        'source': 'https://excalidraw.com',
        'elements': els, 'files': {},
        'appState': {
            'viewBackgroundColor': C['bg'],
            'gridSize': 20, 'currentItemFontFamily': 1,
        },
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
    print(f'  ✓  {name}.excalidraw')


def flat(*groups):
    r = []
    for g in groups:
        r.extend(g[0] if (isinstance(g, tuple) and len(g) == 2 and isinstance(g[0], list)) else g)
    return r


# ══════════════════════════════════════════════════════════════════════════════
# 1.  SYSTEM ARCHITECTURE
# ══════════════════════════════════════════════════════════════════════════════
def make_architecture():
    els = []

    els += flat(txt(290, 15, 'Phil — System Architecture', fs=22, color=C['text']))

    # Layer labels
    els += flat(txt(18, 105, 'Frontend', fs=12, color=C['blue']))
    els += flat(txt(18, 278, 'Backend', fs=12, color=C['accent']))
    els += flat(txt(18, 455, 'AI & Data', fs=12, color=C['purple']))

    # ── Frontend ──────────────────────────────────────────────────────────────
    fe_data = [
        ('Phil\nChat UI', C['blue'], 80),
        ('Dashboard', C['green'], 300),
        ('Mail\nView', C['accent'], 520),
        ('Calendar', C['purple'], 740),
    ]
    fe_cx = []
    for lbl, clr, x in fe_data:
        e, _ = rect(x, 80, 180, 55, lbl, stroke=clr, fs=14)
        els += e
        fe_cx.append(x + 90)

    # ── Backend ───────────────────────────────────────────────────────────────
    be_data = [
        ('FastAPI\nRoutes', C['blue'], 80),
        ('LLMClient', C['accent'], 300),
        ('RAG\nEngine', C['green'], 520),
        ('Graph\nService', C['purple'], 740),
    ]
    be_cx = []
    for lbl, clr, x in be_data:
        e, _ = rect(x, 255, 180, 55, lbl, stroke=clr, fs=14)
        els += e
        be_cx.append(x + 90)

    # Arrows: Frontend → Backend (vertical, same x-center)
    for cx in fe_cx:
        els += flat(arr(cx, 135, cx, 255, color=C['muted']))

    # ── AI & Data ─────────────────────────────────────────────────────────────
    ai_data = [
        ('Exchange\nEWS/IMAP', C['blue'], 55),
        ('LM Studio\n(Local)', C['green'], 225),
        ('Anthropic\nClaude API', C['accent'], 395),
        ('ChromaDB\nVectors', C['blue'], 565),
        ('Neo4j\nGraph DB', C['purple'], 735),
    ]
    ai_cx = []
    for lbl, clr, x in ai_data:
        e, _ = rect(x, 430, 155, 65, lbl, stroke=clr, fs=13)
        els += e
        ai_cx.append(x + 77)

    # Arrows: Backend → AI/Data
    # FastAPI → Exchange
    els += flat(arr(be_cx[0], 310, ai_cx[0], 430, color=C['blue']))
    # LLMClient → LM Studio
    els += flat(arr(be_cx[1], 310, ai_cx[1], 430, color=C['green']))
    # LLMClient → Anthropic
    els += flat(arr(be_cx[1], 310, ai_cx[2], 430, color=C['accent']))
    # RAG → ChromaDB
    els += flat(arr(be_cx[2], 310, ai_cx[3], 430, color=C['blue']))
    # Graph → Neo4j
    els += flat(arr(be_cx[3], 310, ai_cx[4], 430, color=C['purple']))

    # Stack labels (top-right corner)
    els += flat(txt(940, 82, 'React + Vite', fs=11, color=C['muted']))
    els += flat(txt(940, 257, 'Python 3.12', fs=11, color=C['muted']))

    save_diagram('architecture', els)


# ══════════════════════════════════════════════════════════════════════════════
# 2.  RAG PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
def make_rag_pipeline():
    els = []

    els += flat(txt(280, 15, 'RAG Pipeline — Phil Knowledge Engine', fs=22, color=C['text']))

    # ── Index Phase ───────────────────────────────────────────────────────────
    els += flat(txt(50, 60, 'INDEX PHASE', fs=12, color=C['accent']))

    idx = [
        ('Source\nDocuments', C['muted'], 50, 85),
        ('Text\nChunker', C['blue'], 260, 85),
        ('Embedder\n(1536-dim)', C['green'], 470, 85),
        ('ChromaDB\nVector Store', C['purple'], 680, 85),
    ]
    for lbl, clr, x, y in idx:
        e, _ = rect(x, y, 170, 60, lbl, stroke=clr, fs=14)
        els += e

    for i in range(len(idx) - 1):
        x1 = idx[i][2] + 170
        x2 = idx[i + 1][2]
        els += flat(arr(x1, 115, x2, 115, color=C['muted']))

    # ── Query Phase ───────────────────────────────────────────────────────────
    els += flat(txt(50, 205, 'QUERY PHASE', fs=12, color=C['accent']))

    q_items = [
        ('User\nQuery', C['blue'], 50, 230),
        ('Embedder\n(same model)', C['green'], 265, 230),
        ('Top-K\nChunks', C['purple'], 680, 230),
        ('LLM +\nCO-STAR', C['accent'], 890, 230),
    ]
    for lbl, clr, x, y in q_items:
        e, _ = rect(x, y, 170, 60, lbl, stroke=clr, fs=14)
        els += e

    # Decision diamond: cosine similarity
    e, _ = diamond(470, 218, 175, 85, 'Cosine\nSimilarity', stroke=C['accent'], fs=13)
    els += e

    # Query phase arrows
    els += flat(arr(220, 260, 265, 260, color=C['muted']))   # Query → Embedder
    els += flat(arr(435, 260, 470, 260, color=C['muted']))   # Embedder → Cosine (left edge)
    els += flat(arr(645, 260, 680, 260, color=C['muted']))   # Cosine → Top-K (right edge of diamond)
    els += flat(arr(850, 260, 890, 260, color=C['muted']))   # Top-K → LLM

    # Response box
    e, _ = rect(890, 365, 170, 55, 'Answer\n+ Sources', stroke=C['green'], fs=14)
    els += e
    els += flat(arr(975, 290, 975, 365, color=C['green']))   # LLM → Answer

    # ChromaDB ↗ Cosine (index feeds query)
    els += flat(arr(765, 170, 558, 218, color=C['muted'], dashed=True))

    # Annotation
    els += flat(txt(475, 168, 'top-5 chunks · cosine(q⃗, d⃗)', fs=11, color=C['muted']))

    save_diagram('rag-pipeline', els)


# ══════════════════════════════════════════════════════════════════════════════
# 3.  HYBRID LLM DECISION FLOW
# ══════════════════════════════════════════════════════════════════════════════
def make_hybrid_llm():
    els = []

    els += flat(txt(195, 15, 'Hybrid LLM — Decision Flow', fs=22, color=C['text']))

    # Request
    e, _ = rect(300, 60, 200, 55, 'Incoming\nRequest', stroke=C['blue'], fs=15)
    els += e

    # Decision
    e, _ = diamond(265, 170, 270, 100, 'Local LLM\nAvailable?', stroke=C['accent'], fs=14)
    els += e

    # Local branch
    e, _ = rect(60, 345, 200, 60, 'Local LLM\n(localhost:1234/v1)', stroke=C['green'], fs=14)
    els += e
    e, _ = rect(60, 445, 200, 50, 'Zero data\ntransmitted', stroke=C['green'], fill='#0a1f0d', fs=12)
    els += e

    # Cloud branch
    e, _ = rect(540, 345, 200, 60, 'Anthropic\nClaude API', stroke=C['accent'], fs=14)
    els += e
    e, _ = rect(540, 445, 200, 50, 'Token cost\napplies', stroke=C['muted'], fill=C['surface'], fs=12)
    els += e

    # Merge → Response
    e, _ = rect(300, 520, 200, 55, 'Response\n→ Frontend', stroke=C['blue'], fs=15)
    els += e

    # Arrows
    els += flat(arr(400, 115, 400, 170, color=C['muted']))      # Request → Diamond
    els += flat(arr(265, 220, 160, 345, color=C['green']))       # Diamond → Local
    els += flat(arr(535, 220, 640, 345, color=C['accent']))      # Diamond → Cloud
    els += flat(arr(160, 405, 350, 520, color=C['green']))       # Local → Response
    els += flat(arr(640, 405, 450, 520, color=C['accent']))      # Cloud → Response

    # Branch labels
    els += flat(txt(185, 250, 'Yes\n(Local)', fs=12, color=C['green']))
    els += flat(txt(545, 250, 'No\n(Cloud)', fs=12, color=C['accent']))

    # Timeout note
    els += flat(txt(255, 300, '5 s timeout → fallback', fs=11, color=C['muted']))

    save_diagram('hybrid-llm', els)


# ══════════════════════════════════════════════════════════════════════════════
# 4.  MAIL TRIAGE PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
def make_mail_triage():
    els = []

    els += flat(txt(300, 15, 'Mail Triage Pipeline', fs=22, color=C['text']))

    # ── Ingestion row ─────────────────────────────────────────────────────────
    row1 = [
        ('Exchange\nEWS / IMAP', C['blue'], 40),
        ('HTML\nStripper', C['muted'], 270),
        ('Batch\nCollector', C['muted'], 500),
        ('CO-STAR\nPrompt', C['accent'], 730),
    ]
    for lbl, clr, x in row1:
        e, _ = rect(x, 65, 190, 60, lbl, stroke=clr, fs=14)
        els += e

    for i in range(len(row1) - 1):
        x1 = row1[i][2] + 190
        x2 = row1[i + 1][2]
        els += flat(arr(x1, 95, x2, 95, color=C['muted']))

    # ── LLM box ───────────────────────────────────────────────────────────────
    e, _ = rect(730, 200, 190, 60, 'LLM\n(Local · Cloud)', stroke=C['green'], fs=14)
    els += e
    els += flat(arr(825, 125, 825, 200, color=C['accent']))   # CO-STAR → LLM

    # ── Output row (right-to-left) ────────────────────────────────────────────
    row2 = [
        ('Dashboard\nDisplay', C['blue'], 40),
        ('Category\n+ Priority', C['accent'], 270),
    ]
    for lbl, clr, x in row2:
        e, _ = rect(x, 200, 190, 60, lbl, stroke=clr, fs=14)
        els += e

    els += flat(arr(730, 230, 460, 230, color=C['accent']))   # LLM → Category
    els += flat(arr(270, 230, 230, 230, color=C['muted']))    # Category → Dashboard

    # Category labels
    els += flat(txt(275, 272, 'Urgent · Important · Delegate · Trash', fs=11, color=C['muted']))

    # Powered-by note (neutral — any of the three)
    e, _ = rect(730, 305, 190, 80,
                'Powered by\nLM Studio · Claude\nor both (Hybrid)',
                stroke=C['muted'], fill=C['surface'], fs=11, fc=C['muted'])
    els += e
    els += flat(arr(825, 260, 825, 305, color=C['muted'], dashed=True))

    save_diagram('mail-triage', els)


# ══════════════════════════════════════════════════════════════════════════════
# 5.  UI DASHBOARD WIREFRAME
# ══════════════════════════════════════════════════════════════════════════════
def make_ui_dashboard():
    els = []

    els += flat(txt(290, 15, 'Phil Dashboard — UI Wireframe', fs=22, color=C['text']))

    # Browser chrome
    e, _ = rect(30, 50, 970, 610, '', stroke=C['border'], fill='#0a0e13', rounded=False)
    els += e

    # Sidebar
    e, _ = rect(30, 50, 185, 610, '', stroke=C['border'], fill='#111519', rounded=False)
    els += e
    els += flat(txt(55, 70, 'Phil', fs=20, color=C['accent']))

    sidebar_items = [
        ('Inbox  (12)', True),
        ('Dashboard', False),
        ('Kalender', False),
        ('Aufgaben', False),
        ('Analytik', False),
        ('Einstellungen', False),
    ]
    for i, (item, active) in enumerate(sidebar_items):
        y = 108 + i * 44
        if active:
            e, _ = rect(36, y - 4, 173, 34, item, stroke=C['border'], fill=C['surface'], fs=13)
            els += e
        else:
            els += flat(txt(52, y, item, fs=13, color=C['muted']))

    # Badge
    e, _ = rect(170, 107, 28, 20, '12', stroke=C['red'], fill=C['red'], fs=11, fc=C['text'])
    els += e

    # Top bar
    e, _ = rect(215, 50, 785, 50, '', stroke=C['border'], fill='#0d1117', rounded=False)
    els += e
    els += flat(txt(230, 67, 'Dashboard', fs=16, color=C['text']))
    els += flat(txt(810, 67, '⌕  Suchen', fs=13, color=C['muted']))

    # Stat tiles
    stat_tiles = [
        ('48', 'E-Mails heute', C['accent']),
        ('12', 'Ungelesen', C['red']),
        ('5',  'Aufgaben offen', C['green']),
        ('3',  'Termine heute', C['blue']),
    ]
    for i, (num, lbl, clr) in enumerate(stat_tiles):
        x = 220 + i * 188
        e, _ = rect(x, 110, 178, 70, f'{num}\n{lbl}', stroke=clr, fill=C['surface'], fs=14)
        els += e

    # Mail list header
    els += flat(txt(220, 198, 'Neueste E-Mails', fs=14, color=C['muted']))

    mail_items = [
        ('Michael Braun', 'Meeting morgen früh — bitte...', 'Urgent', C['red']),
        ('Sarah König', 'Q1 Report Draft attached — p...', 'Important', C['accent']),
        ('Newsletter', 'Weekly AI Digest — Top news...', 'Trash', C['muted']),
    ]
    for i, (sender, preview, cat, clr) in enumerate(mail_items):
        y = 218 + i * 68
        e, _ = rect(220, y, 395, 58, '', stroke=C['border'], fill=C['surface'])
        els += e
        els += flat(txt(234, y + 9, sender, fs=13, color=C['text']))
        els += flat(txt(234, y + 30, preview, fs=11, color=C['muted']))
        e2, _ = rect(566, y + 14, 82, 24, cat, stroke=clr, fill='transparent', fs=11, fc=clr)
        els += e2

    # Calendar panel
    e, _ = rect(632, 198, 358, 225, '', stroke=C['border'], fill=C['surface'])
    els += e
    els += flat(txt(648, 210, 'Kalender — Februar 2026', fs=13, color=C['text']))

    cal_events = [
        ('09:00  Team Standup', C['blue']),
        ('14:00  Projekt-Review', C['accent']),
        ('16:30  1:1 mit Manager', C['green']),
    ]
    for i, (ev, clr) in enumerate(cal_events):
        y = 238 + i * 53
        e, _ = rect(642, y, 338, 40, ev, stroke=clr, fill='transparent', fs=13)
        els += e

    # Task list
    e, _ = rect(220, 430, 395, 200, '', stroke=C['border'], fill=C['surface'])
    els += e
    els += flat(txt(234, 442, 'Aufgaben', fs=14, color=C['text']))

    tasks = [
        ('☐  Präsentation für Donnerstag', C['text']),
        ('☐  Code Review — PR #47', C['text']),
        ('☑  Meeting-Notizen verteilen', C['muted']),
        ('☐  RAG-Index aktualisieren', C['text']),
    ]
    for i, (task, clr) in enumerate(tasks):
        els += flat(txt(234, 468 + i * 40, task, fs=12, color=clr))

    # Analytics
    e, _ = rect(632, 430, 358, 200, '', stroke=C['border'], fill=C['surface'])
    els += e
    els += flat(txt(648, 442, 'Mail-Analytik', fs=14, color=C['text']))
    els += flat(txt(648, 470, '72 %   automatisch kategorisiert', fs=12, color=C['green']))
    els += flat(txt(648, 494, '3.2 s   ⌀ Triage-Zeit', fs=12, color=C['blue']))
    els += flat(txt(648, 518, '96 %   Genauigkeit (letzte 30 T)', fs=12, color=C['accent']))
    els += flat(txt(648, 556, 'Modell: LM Studio · Qwen2.5-32B Q4', fs=11, color=C['muted']))

    save_diagram('ui-dashboard', els)


# ══════════════════════════════════════════════════════════════════════════════
# 6.  UI CHAT WIREFRAME
# ══════════════════════════════════════════════════════════════════════════════
def make_ui_chat():
    els = []

    els += flat(txt(290, 15, 'Phil Chat Interface — UI Wireframe', fs=22, color=C['text']))

    # Outer frame
    e, _ = rect(30, 50, 1010, 620, '', stroke=C['border'], fill='#0a0e13', rounded=False)
    els += e

    # Header bar
    e, _ = rect(30, 50, 1010, 52, '', stroke=C['border'], fill='#0d1117', rounded=False)
    els += e
    els += flat(txt(50, 65, 'Phil — Chat', fs=16, color=C['text']))

    # LLM mode badge (left)
    e, _ = rect(155, 61, 65, 28, 'Hybrid', stroke=C['accent'], fill='transparent', fs=11, fc=C['accent'])
    els += e

    # Context toggle label + chips (right)
    els += flat(txt(755, 67, 'Kontext:', fs=12, color=C['muted']))
    for i, (lbl, clr) in enumerate([('Mail', C['accent']), ('Kalender', C['blue']), ('Aufgaben', C['green'])]):
        x = 820 + i * 68
        e, _ = rect(x, 61, 60, 28, lbl, stroke=clr, fill='transparent', fs=11, fc=clr)
        els += e

    # Chat area
    e, _ = rect(30, 102, 690, 460, '', stroke=C['border'], fill=C['bg'], rounded=False)
    els += e

    # User message (right-aligned)
    e, _ = rect(355, 120, 345, 60, 'Was waren meine\nwichtigsten Mails heute?', stroke=C['blue'], fill='#0d2036', fs=13)
    els += e
    els += flat(txt(696, 183, 'Du', fs=11, color=C['muted']))

    # Assistant response (left)
    e, _ = rect(42, 205, 500, 100, 'Du hattest heute 48 E-Mails. Die wichtigsten:\nMichael Braun (Urgent — Meeting morgen),\nSarah König (Report angehängt, Deadline Fr).', stroke=C['green'], fill='#0a1a0c', fs=13)
    els += e
    els += flat(txt(42, 310, 'Phil · LM Studio · Qwen2.5-32B · 22 tok/s', fs=11, color=C['muted']))

    # Second user message
    e, _ = rect(355, 340, 345, 50, 'Erstelle eine Zusammenfassung\nfür mein Meeting um 14:00', stroke=C['blue'], fill='#0d2036', fs=12)
    els += e

    # Typing indicator
    e, _ = rect(42, 415, 120, 38, '● ● ●', stroke=C['muted'], fill=C['surface'], fs=16, fc=C['muted'])
    els += e

    # TTS button (floating)
    e, _ = rect(650, 415, 60, 38, '♪ TTS', stroke=C['purple'], fill='transparent', fs=12, fc=C['purple'])
    els += e

    # Input area
    e, _ = rect(30, 562, 690, 108, '', stroke=C['border'], fill='#111519', rounded=False)
    els += e
    e, _ = rect(44, 575, 590, 40, 'Nachricht eingeben…', stroke=C['border'], fill=C['surface'], fs=13, fc=C['muted'])
    els += e
    e, _ = rect(648, 575, 60, 40, 'Send', stroke=C['accent'], fill=C['accent'], fs=13, fc='#0d1117')
    els += e
    e, _ = rect(44, 625, 664, 35, 'Senden', stroke=C['accent'], fill=C['accent'], fs=14, fc='#0d1117')
    els += e

    # RAG context panel (right)
    e, _ = rect(732, 102, 308, 460, '', stroke=C['border'], fill=C['surface'])
    els += e
    els += flat(txt(748, 114, 'RAG-Kontext', fs=14, color=C['text']))
    els += flat(txt(748, 136, '3 Quellen gefunden', fs=11, color=C['muted']))

    sources = [
        ('mail_2026-02-23_braun.txt', 'score: 0.94', C['accent']),
        ('tasks_2026-02-23.json', 'score: 0.87', C['green']),
        ('calendar_today.ics', 'score: 0.82', C['blue']),
    ]
    for i, (src, score, clr) in enumerate(sources):
        y = 162 + i * 88
        e, _ = rect(740, y, 288, 72, '', stroke=clr, fill=C['bg'])
        els += e
        els += flat(txt(752, y + 8, src, fs=12, color=C['text']))
        els += flat(txt(752, y + 30, score, fs=11, color=clr))
        els += flat(txt(752, y + 50, 'Top-5 Chunks · cosine similarity', fs=10, color=C['muted']))

    # Knowledge graph panel (bottom of right panel)
    e, _ = rect(732, 562, 308, 108, '', stroke=C['border'], fill=C['surface'])
    els += e
    els += flat(txt(748, 574, 'Knowledge Graph', fs=13, color=C['purple']))
    els += flat(txt(748, 596, 'Phil → hatMail → braun_2026-02-23', fs=11, color=C['muted']))
    els += flat(txt(748, 616, 'Braun → hatTermin → 2026-02-24 09:00', fs=11, color=C['muted']))
    els += flat(txt(748, 636, 'SPARQL · RDF · OWL inference', fs=11, color=C['muted']))

    save_diagram('ui-chat', els)


# ══════════════════════════════════════════════════════════════════════════════
# 7.  INTELLECTUAL LINEAGE TIMELINE
# ══════════════════════════════════════════════════════════════════════════════
def make_timeline():
    els = []

    els += flat(txt(280, 15, 'Intellectual Lineage — The Path to Phil', fs=22, color=C['text']))

    # Horizontal spine
    els += flat(arr(60, 120, 1120, 120, color=C['border']))

    MILESTONES = [
        (1935, 'Mundaneum\nOtlet', C['muted'], 'below'),
        (1945, 'Memex\nVannevar Bush', C['blue'], 'above'),
        (1950, 'Turing Test\nAlan Turing', C['muted'], 'below'),
        (1960, 'Man–Computer\nSymbiosis · Licklider', C['blue'], 'above'),
        (1963, 'Sketchpad\nSutherland', C['muted'], 'below'),
        (1968, 'Mother of\nAll Demos · Engelbart', C['blue'], 'above'),
        (1972, 'Dynabook\nAlan Kay', C['muted'], 'below'),
        (1987, 'Knowledge Navigator\nApple · Phil', C['accent'], 'above'),
        (2022, 'ChatGPT\nOpenAI', C['green'], 'below'),
        (2026, 'Phil\nThis project', C['accent'], 'above'),
    ]

    year_min, year_max = 1930, 2030
    total_span = year_max - year_min
    x_left, x_right = 60, 1120
    x_range = x_right - x_left

    for year, label, color, side in MILESTONES:
        x = int(x_left + (year - year_min) / total_span * x_range)

        # Node dot
        dot_id = uid()
        dot = {**_b(), 'id': dot_id, 'type': 'ellipse',
               'x': x - 5, 'y': 115, 'width': 10, 'height': 10,
               'strokeColor': color, 'backgroundColor': color,
               'fillStyle': 'solid', 'roughness': 0, 'boundElements': []}
        els.append(dot)

        # Vertical stem
        if side == 'above':
            els += flat(arr(x, 115, x, 68, color=color))
        else:
            els += flat(arr(x, 125, x, 162, color=color))

        # Year label
        yr_y = 58 if side == 'above' else 162
        els += flat(txt(x - 15, yr_y, str(year), fs=11, color=color, align='center'))

        # Text label
        lbl_y = 35 if side == 'above' else 178
        els += flat(txt(x - 50, lbl_y, label, fs=10, color=C['text'] if color == C['accent'] else C['muted'], align='center'))

    # "1935 – 2026" caption
    els += flat(txt(540, 230, '91 years of ideas. One project.', fs=14, color=C['muted'], align='center'))

    save_diagram('timeline', els)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f'Generating diagrams → {OUT_DIR}\n')
    make_architecture()
    make_rag_pipeline()
    make_hybrid_llm()
    make_mail_triage()
    make_ui_dashboard()
    make_ui_chat()
    make_timeline()
    print('\nDone! 7 diagrams generated.')
