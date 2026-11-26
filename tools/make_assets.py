"""Generate the profile's SVG assets:  python tools/make_assets.py  ->  assets/"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
FONT = "Segoe UI, Helvetica, Arial, sans-serif"
MONO = "SFMono-Regular, Consolas, Menlo, monospace"

PROJECTS = [
    # slug, title, kicker, one-liner (2 lines max), metric, tags, accent pair, glyph
    ("13-gait-evolution", "Gait Evolution", "ROBOTICS · OPTIMISATION",
     "Evolves walking gaits for a 12-servo robot dog with from-scratch CMA-ES",
     "rediscovered the walk animals use", ["CMA-ES", "IK", "NumPy"], ("#22d3ee", "#6366f1"), "dog"),
    ("12-telemetry-doctor", "Telemetry Doctor", "ROBOTICS · RELIABILITY",
     "Catches and diagnoses servo faults from the robot's own telemetry",
     "48/48 diagnosed · 0 false alarms/h", ["CUSUM", "Diagnosis", "Python"], ("#34d399", "#0ea5e9"), "pulse"),
    ("11-where-is-it", "Where Is It?", "ROBOTICS · PROBABILISTIC AI",
     "Bayesian object memory: 'where are my keys?' with calibrated confidence",
     "confidently-wrong 14.8% → 2.6%", ["Kalman", "Bayes", "A*"], ("#f472b6", "#8b5cf6"), "pin"),
    ("05-quadruped", "Quadruped", "ROBOTICS · CONTROL",
     "IK + gait controller for a 12-servo robot dog, with a live browser simulator",
     "MG996R + PCA9685 hardware", ["IK", "Gaits", "Sim"], ("#fb923c", "#f43f5e"), "dog"),
    ("08-slam", "Grid SLAM", "ROBOTICS · LOCALISATION",
     "2D grid SLAM with scan matching + Monte Carlo localisation",
     "recovers from robot kidnapping", ["SLAM", "MCL", "NumPy"], ("#a3e635", "#14b8a6"), "map"),
    ("10-sensor-fusion", "Sensor Fusion", "ROBOTICS · ESTIMATION",
     "EKF fusing IMU + wheel odometry + GPS with bias estimation",
     "NEES/NIS consistency checked", ["EKF", "IMU", "GPS"], ("#38bdf8", "#22c55e"), "fuse"),
    ("09-path-planning", "Path Planning", "ROBOTICS · PLANNING",
     "A*, Dijkstra, Theta*, RRT and RRT* compared and benchmarked",
     "5 planners, one benchmark", ["A*", "RRT*", "Theta*"], ("#facc15", "#f97316"), "path"),
    ("06-vision", "Robot Vision", "COMPUTER VISION",
     "YOLO ONNX detection API for robots with tracking and follow-me control",
     "bearing + distance per object", ["YOLO", "ONNX", "FastAPI"], ("#e879f9", "#6366f1"), "eye"),
    ("agent-hq", "Agent HQ", "AI · MULTI-AGENT",
     "An office of 28 AI agents with one shared brain, on a MacBook",
     "zero-cost, runs locally", ["Agents", "Memory", "Ollama"], ("#818cf8", "#ec4899"), "brain"),
    ("01-rag", "RAG with Receipts", "AI · RETRIEVAL",
     "Q&A over your own PDFs that cites document + page and says 'I don't know'",
     "eval prints a pass rate", ["RAG", "Embeddings", "Eval"], ("#2dd4bf", "#3b82f6"), "doc"),
    ("02-agents", "Long-Horizon Agent", "AI · AGENTS",
     "Plan-act-check loop, parallel sub-agents, sandboxed code, guardrails",
     "step logs + task eval", ["Agents", "Sandbox", "Guardrails"], ("#c084fc", "#f43f5e"), "brain"),
    ("07-llm-eval", "LLM Eval Harness", "AI · EVALUATION",
     "Rule + LLM-as-judge scorers, CI regression gate, tracing, HTML reports",
     "latency · tokens · cost", ["Evals", "CI", "Tracing"], ("#fbbf24", "#ef4444"), "chart"),
    ("04-finetune", "QLoRA Fine-tune", "AI · TRAINING",
     "QLoRA fine-tune of a small LLM on a free T4 for structured extraction",
     "before/after eval", ["QLoRA", "PEFT", "HF"], ("#4ade80", "#06b6d4"), "chip"),
    ("03-deploy", "LLM Serving", "AI · INFERENCE",
     "Serve an open model with vLLM on a free T4 and measure it properly",
     "TTFT · ITL · throughput", ["vLLM", "Latency", "GPU"], ("#60a5fa", "#a855f7"), "bolt"),
]


def glyph(kind, c):
    s = f'fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"'
    return {
        "dog": f'<g {s}><rect x="6" y="12" width="26" height="10" rx="4"/><circle cx="36" cy="12" r="5"/>'
               f'<path d="M10 22l-3 10M15 22l2 10M24 22l-3 10M29 22l2 10"/></g>',
        "pulse": f'<path {s} d="M2 22h8l4-12 6 22 5-16 3 6h12"/>',
        "pin": f'<g {s}><path d="M20 36s-11-11-11-19a11 11 0 0 1 22 0c0 8-11 19-11 19z"/><circle cx="20" cy="17" r="4"/></g>',
        "map": f'<g {s}><path d="M3 9l11-4 12 4 11-4v26l-11 4-12-4-11 4z"/><path d="M14 5v26M26 9v26"/></g>',
        "fuse": f'<g {s}><circle cx="12" cy="20" r="8"/><circle cx="28" cy="20" r="8"/></g>',
        "path": f'<g {s}><circle cx="6" cy="32" r="3"/><circle cx="34" cy="8" r="3"/><path d="M9 32h10a6 6 0 0 0 0-12h-4a6 6 0 0 1 0-12h16"/></g>',
        "eye": f'<g {s}><path d="M2 20s7-12 18-12 18 12 18 12-7 12-18 12S2 20 2 20z"/><circle cx="20" cy="20" r="5"/></g>',
        "brain": f'<g {s}><circle cx="20" cy="20" r="5"/><circle cx="6" cy="8" r="3"/><circle cx="34" cy="8" r="3"/><circle cx="6" cy="32" r="3"/><circle cx="34" cy="32" r="3"/><path d="M9 10l7 6M31 10l-7 6M9 30l7-6M31 30l-7-6"/></g>',
        "doc": f'<g {s}><path d="M9 3h15l8 8v26H9z"/><path d="M24 3v8h8M14 20h12M14 26h12M14 32h7"/></g>',
        "chart": f'<g {s}><path d="M4 36h32"/><rect x="8" y="22" width="5" height="14"/><rect x="18" y="12" width="5" height="24"/><rect x="28" y="4" width="5" height="32"/></g>',
        "chip": f'<g {s}><rect x="10" y="10" width="20" height="20" rx="3"/><path d="M15 4v6M25 4v6M15 30v6M25 30v6M4 15h6M4 25h6M30 15h6M30 25h6"/></g>',
        "bolt": f'<path {s} d="M22 2L6 22h12l-2 16 16-20H20z"/>',
    }[kind]


def card(slug, title, kicker, desc, metric, tags, accent, g):
    a, b = accent
    w, h = 420, 196
    words, lines, cur = desc.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > 52:
            lines.append(cur)
            cur = wd
        else:
            cur = f"{cur} {wd}".strip()
    lines.append(cur)
    desc_svg = "".join(f'<tspan x="24" dy="{0 if i == 0 else 19}">{escape(l)}</tspan>' for i, l in enumerate(lines[:2]))
    tx, chips = 24, ""
    for t in tags:
        tw = 14 + 7.2 * len(t)
        chips += (f'<rect x="{tx}" y="160" width="{tw:.0f}" height="22" rx="11" fill="{a}" fill-opacity="0.14" stroke="{a}" stroke-opacity="0.45"/>'
                  f'<text x="{tx + tw / 2:.0f}" y="175" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{a}">{escape(t)}</text>')
        tx += tw + 8
    uid = slug.replace("-", "")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>
  <linearGradient id="g{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>
  <radialGradient id="r{uid}" cx="0.9" cy="0.1" r="0.8"><stop offset="0" stop-color="{b}" stop-opacity="0.35"/><stop offset="1" stop-color="{b}" stop-opacity="0"/></radialGradient>
</defs>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="#0d1117"/>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="url(#r{uid})"/>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="none" stroke="url(#g{uid})" stroke-width="1.6" stroke-opacity="0.8"/>
<rect x="1" y="1" width="6" height="{h - 2}" rx="3" fill="url(#g{uid})"/>
<g transform="translate({w - 64},20)" opacity="0.95">{glyph(g, a)}</g>
<text x="24" y="34" font-family="{MONO}" font-size="10.5" letter-spacing="1.6" fill="{a}">{escape(kicker)}</text>
<text x="24" y="64" font-family="{FONT}" font-size="25" font-weight="700" fill="#f0f6fc">{escape(title)}</text>
<text x="24" y="92" font-family="{FONT}" font-size="13.5" fill="#9da7b3">{desc_svg}</text>
<text x="24" y="146" font-family="{FONT}" font-size="13" font-weight="600" fill="url(#g{uid})">▸ {escape(metric)}</text>
{chips}
</svg>'''


def section(text, sub, a="#38bdf8", b="#a78bfa"):
    uid = "".join(ch for ch in text if ch.isalnum())
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="880" height="64" viewBox="0 0 880 64">
<defs><linearGradient id="s{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs>
<text x="0" y="34" font-family="{FONT}" font-size="26" font-weight="700" fill="url(#s{uid})">{escape(text)}</text>
<text x="0" y="56" font-family="{MONO}" font-size="12" fill="#8b949e">{escape(sub)}</text>
<rect x="0" y="60" width="880" height="2" rx="1" fill="url(#s{uid})" opacity="0.35"/>
<rect x="0" y="60" width="120" height="2" rx="1" fill="url(#s{uid})"><animate attributeName="x" values="0;760;0" dur="8s" repeatCount="indefinite"/></rect>
</svg>'''


def header():
    # walking quadruped: legs swing with a lateral-sequence phase pattern (FL, RR, FR, RL a quarter apart)
    def leg(x, phase):
        b = f"{phase:.2f}s"
        return (f'<g transform="translate({x},0)"><line x1="0" y1="0" x2="0" y2="34" stroke="#e6edf3" stroke-width="5" stroke-linecap="round">'
                f'<animateTransform attributeName="transform" type="rotate" values="-18;18;-18" keyTimes="0;0.85;1" dur="1.6s" begin="{b}" repeatCount="indefinite"/></line>'
                f'<circle cx="0" cy="0" r="4.5" fill="#38bdf8"/></g>')

    legs = leg(-38, -0.0) + leg(-26, -0.8) + leg(26, -0.4) + leg(38, -1.2)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="260" viewBox="0 0 1000 260">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#050816"/><stop offset="0.55" stop-color="#0b1a33"/><stop offset="1" stop-color="#1b1036"/></linearGradient>
  <linearGradient id="gl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#38bdf8"/><stop offset="0.5" stop-color="#818cf8"/><stop offset="1" stop-color="#f472b6"/></linearGradient>
  <radialGradient id="orb1" cx="0.15" cy="0.2" r="0.5"><stop offset="0" stop-color="#38bdf8" stop-opacity="0.35"/><stop offset="1" stop-color="#38bdf8" stop-opacity="0"/></radialGradient>
  <radialGradient id="orb2" cx="0.85" cy="0.9" r="0.5"><stop offset="0" stop-color="#f472b6" stop-opacity="0.28"/><stop offset="1" stop-color="#f472b6" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#ffffff" stroke-opacity="0.045"/></pattern>
  <clipPath id="clip"><rect width="1000" height="260" rx="20"/></clipPath>
</defs>
<g clip-path="url(#clip)">
<rect width="1000" height="260" fill="url(#bg)"/>
<rect width="1000" height="260" fill="url(#orb1)"/><rect width="1000" height="260" fill="url(#orb2)"/>
<rect width="1000" height="260" fill="url(#grid)"/>
<g fill="#ffffff">
  <circle cx="90" cy="40" r="1.2" opacity="0.6"><animate attributeName="opacity" values="0.1;0.8;0.1" dur="3s" repeatCount="indefinite"/></circle>
  <circle cx="300" cy="28" r="1" opacity="0.5"><animate attributeName="opacity" values="0.8;0.1;0.8" dur="4s" repeatCount="indefinite"/></circle>
  <circle cx="610" cy="34" r="1.3"><animate attributeName="opacity" values="0.2;0.9;0.2" dur="3.5s" repeatCount="indefinite"/></circle>
  <circle cx="930" cy="60" r="1"><animate attributeName="opacity" values="0.9;0.2;0.9" dur="2.6s" repeatCount="indefinite"/></circle>
  <circle cx="470" cy="230" r="1.1"><animate attributeName="opacity" values="0.1;0.7;0.1" dur="3.2s" repeatCount="indefinite"/></circle>
</g>
<g stroke="url(#gl)" stroke-width="1.8" fill="none" opacity="0.5">
  <path d="M0 206 H110 L140 176 H240" stroke-dasharray="270" stroke-dashoffset="270"><animate attributeName="stroke-dashoffset" values="270;0;0;270" dur="7s" repeatCount="indefinite"/></path>
  <path d="M1000 44 H900 L870 74 H780" stroke-dasharray="240" stroke-dashoffset="240"><animate attributeName="stroke-dashoffset" values="240;0;0;240" dur="7s" begin="2s" repeatCount="indefinite"/></path>
</g>
<!-- text block -->
<text x="64" y="92" font-family="{MONO}" font-size="14" letter-spacing="3" fill="#38bdf8">HELLO, I'M</text>
<text x="62" y="144" font-family="{FONT}" font-size="58" font-weight="800" fill="#ffffff">Pribin K Benny</text>
<text x="64" y="180" font-family="{FONT}" font-size="20" font-weight="600" fill="url(#gl)">AI &amp; Robotics Engineer</text>
<text x="64" y="212" font-family="{MONO}" font-size="13" fill="#8b949e">MSc AI &amp; Robotics (Distinction) · Bengaluru, India</text>
<!-- robot dog walking on a treadmill line -->
<g transform="translate(790,128)">
  <animateTransform attributeName="transform" type="translate" values="790,128;790,124;790,128" dur="0.8s" repeatCount="indefinite"/>
  <rect x="-48" y="-18" width="96" height="26" rx="10" fill="#111827" stroke="url(#gl)" stroke-width="2.5"/>
  <rect x="-30" y="-12" width="44" height="6" rx="3" fill="#38bdf8" opacity="0.7"><animate attributeName="opacity" values="0.3;0.9;0.3" dur="1.6s" repeatCount="indefinite"/></rect>
  <g transform="translate(58,-26)">
    <rect x="-14" y="-12" width="30" height="22" rx="8" fill="#111827" stroke="url(#gl)" stroke-width="2.5"/>
    <circle cx="5" cy="-2" r="3.4" fill="#38bdf8"><animate attributeName="r" values="3.4;3.4;0.6;3.4" keyTimes="0;0.9;0.95;1" dur="4s" repeatCount="indefinite"/></circle>
    <line x1="-4" y1="-12" x2="-8" y2="-22" stroke="#e6edf3" stroke-width="2.5" stroke-linecap="round"/><circle cx="-8" cy="-23" r="2.6" fill="#f472b6"/>
  </g>
  <g transform="translate(0,6)">{legs}</g>
</g>
<g transform="translate(700,176)">
  <rect x="0" y="0" width="190" height="3" rx="1.5" fill="#1f2937"/>
  <g fill="url(#gl)">
    <rect x="0" y="0" width="22" height="3" rx="1.5"><animate attributeName="x" values="190;-22" dur="1.6s" repeatCount="indefinite"/></rect>
    <rect x="0" y="0" width="22" height="3" rx="1.5"><animate attributeName="x" values="95;-22;190;95" keyTimes="0;0.38;0.38;1" dur="1.6s" repeatCount="indefinite"/></rect>
  </g>
</g>
<text x="795" y="216" text-anchor="middle" font-family="{MONO}" font-size="11" fill="#8b949e">evolved lateral-sequence walk</text>
</g>
<rect x="1" y="1" width="998" height="258" rx="20" fill="none" stroke="url(#gl)" stroke-opacity="0.35"/>
</svg>'''


def footer():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="90" viewBox="0 0 1000 90">
<defs><linearGradient id="f" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#38bdf8"/><stop offset="0.5" stop-color="#818cf8"/><stop offset="1" stop-color="#f472b6"/></linearGradient></defs>
<path fill="url(#f)" opacity="0.18" d="M0 50 Q125 20 250 50 T500 50 T750 50 T1000 50 V90 H0Z"><animate attributeName="d" dur="8s" repeatCount="indefinite" values="M0 50 Q125 20 250 50 T500 50 T750 50 T1000 50 V90 H0Z;M0 50 Q125 80 250 50 T500 50 T750 50 T1000 50 V90 H0Z;M0 50 Q125 20 250 50 T500 50 T750 50 T1000 50 V90 H0Z"/></path>
<path fill="url(#f)" opacity="0.35" d="M0 62 Q125 82 250 62 T500 62 T750 62 T1000 62 V90 H0Z"><animate attributeName="d" dur="6s" repeatCount="indefinite" values="M0 62 Q125 82 250 62 T500 62 T750 62 T1000 62 V90 H0Z;M0 62 Q125 42 250 62 T500 62 T750 62 T1000 62 V90 H0Z;M0 62 Q125 82 250 62 T500 62 T750 62 T1000 62 V90 H0Z"/></path>
<text x="500" y="30" text-anchor="middle" font-family="SFMono-Regular, Consolas, Menlo, monospace" font-size="13" fill="#8b949e">building robots that walk, see and remember · thanks for visiting</text>
</svg>'''


def main():
    (OUT / "cards").mkdir(parents=True, exist_ok=True)
    (OUT / "hero.svg").write_text(header())
    (OUT / "footer.svg").write_text(footer())
    for p in PROJECTS:
        (OUT / "cards" / f"{p[0]}.svg").write_text(card(*p))
    sections = {
        "about": ("About me", "// who I am and what I'm working towards", "#38bdf8", "#818cf8"),
        "stack": ("Tech stack", "// tools I ship with", "#22d3ee", "#a78bfa"),
        "robotics": ("Robotics", "// a 12-servo robot dog, end to end: control, perception, reliability", "#fb923c", "#f472b6"),
        "ai": ("AI & LLM systems", "// measured, not just demoed", "#818cf8", "#ec4899"),
        "gallery": ("See it move", "// live outputs straight from the repos", "#34d399", "#38bdf8"),
        "stats": ("Activity", "// shipping in public", "#facc15", "#f97316"),
    }
    for k, v in sections.items():
        (OUT / f"section-{k}.svg").write_text(section(*v))


if __name__ == "__main__":
    main()
