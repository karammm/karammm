"""Generate assets/terminal.svg, the animated terminal at the top of the profile README.

    python3 scripts/make_terminal.py

Edit LINES below and re-run. Each line appears in turn, like a live terminal session,
then the animation loops. Viewers with "reduce motion" switched on see the finished frame.
"""

from html import escape
from pathlib import Path

PROMPT = "karamjit@github:~$ "

# (kind, text): "cmd" lines are typed at the prompt; "out" lines are command output.
# Output text can colour words with {{word|class}} where class is one of: key, val, accent, dim.
LINES = [
    ("cmd", "whoami"),
    ("out", "{{Karamjit Verma|key}} · {{Senior Software Engineer|accent}} @ {{OptiValue Tek|val}} · Full-Stack"),
    ("cmd", "cat about.txt"),
    ("out", "5+ years building production web apps, APIs and cloud deployments."),
    ("out", "Delhi, India · working remotely"),
    ("cmd", "cat experience.log"),
    ("out", "{{2025–now  |key}}  Senior Software Engineer · {{OptiValue Tek|val}}"),
    ("out", "{{2025      |key}}  Senior Software Engineer · {{InCred Financial Services|val}}"),
    ("out", "{{2023–2025 |key}}  Software Engineer        · {{Builder.ai|val}}"),
    ("out", "{{2021–2023 |key}}  SDE                      · {{Ameha Technologies|val}}"),
    ("out", "{{cert      |key}}  AWS Certified Solutions Architect – Associate {{(2020–2023)|dim}}"),
    ("cmd", "stack --top"),
    ("out", "{{frontend|key}}   Angular · React · JavaScript · TypeScript"),
    ("out", "{{mobile  |key}}   React Native"),
    ("out", "{{backend |key}}   Python · Flask · FastAPI"),
    ("out", "{{cloud   |key}}   AWS · Docker · CI/CD"),
    ("cmd", "ls ~/open-source"),
    ("out", "{{openmoderate/|accent}}   image & video moderation  {{· PyPI · CLIP deep learning|dim}}"),
    ("out", "{{safetype/|accent}}       real-time text moderation {{· npm · React/Vue/Angular|dim}}"),
    ("cmd", "contact"),
    ("out", "{{linkedin|key}}  linkedin.com/in/karamjit-verma"),
    ("out", "{{email   |key}}  karamjitverma89@gmail.com"),
]

W, PAD, LINE_H, TOP = 900, 26, 25, 66
LOOP_S = 18.0
SHOW_END = 93.0  # % of the loop when everything fades out


def styled(text: str) -> str:
    """Turn {{word|class}} markers into coloured tspans."""
    out, rest = [], text
    while "{{" in rest:
        before, _, tail = rest.partition("{{")
        inner, _, rest = tail.partition("}}")
        word, _, cls = inner.partition("|")
        out.append(escape(before))
        out.append(f'<tspan class="{cls}">{escape(word)}</tspan>')
    out.append(escape(rest))
    return "".join(out)


def build() -> str:
    height = TOP + len(LINES) * LINE_H + 28
    times, clock = [], 0.5
    for kind, _ in LINES:
        clock += 0.85 if kind == "cmd" else 0.3
        times.append(clock)
        if kind == "cmd":
            clock += 0.45
    frames, rules = [], []
    for i, start in enumerate(times):
        p = min(start / LOOP_S * 100, SHOW_END - 1)
        frames.append(
            f"@keyframes l{i} {{ 0%, {p:.2f}% {{ opacity: 0 }} {p + 0.5:.2f}%, {SHOW_END}% "
            f"{{ opacity: 1 }} 100% {{ opacity: 0 }} }}"
        )
        rules.append(f".l{i} {{ opacity: 0; animation: l{i} {LOOP_S}s linear infinite; }}")
    css = "\n".join(frames + rules) + """
  text { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 15px; white-space: pre; fill: #e6edf3; }
  .prompt { fill: #3fb950; } .key { fill: #79c0ff; } .val { fill: #d2a8ff; }
  .accent { fill: #ffa657; font-weight: 600; } .dim { fill: #8b949e; } .title { fill: #8b949e; font-size: 13px; }
  .cursor { fill: #e6edf3; animation: blink 1s steps(1) infinite; }
  @keyframes blink { 50% { opacity: 0; } }
  @media (prefers-reduced-motion: reduce) { .ln { animation: none !important; opacity: 1 !important; } }
"""
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" '
        f'viewBox="0 0 {W} {height}" role="img" aria-labelledby="t d">',
        "<title id='t'>Karamjit Verma — terminal introduction</title>",
        "<desc id='d'>An animated terminal: Karamjit Verma, Senior Software Engineer at OptiValue "
        "Tek, full-stack, 5+ years of experience, Delhi, India. Experience: OptiValue Tek, InCred "
        "Financial Services, Builder.ai, Ameha Technologies. AWS Certified Solutions Architect – "
        "Associate (2020–2023). Stack: Angular, React, React Native, "
        "JavaScript, TypeScript, Python, Flask, FastAPI, AWS, Docker. Open source: openmoderate "
        "and SafeType.js. Contact: LinkedIn karamjit-verma.</desc>",
        f"<style>{css}</style>",
        f'<rect width="{W}" height="{height}" rx="12" fill="#0d1117" stroke="#30363d"/>',
        '<circle cx="24" cy="22" r="6" fill="#ff5f57"/><circle cx="44" cy="22" r="6" fill="#febc2e"/>'
        '<circle cx="64" cy="22" r="6" fill="#28c840"/>',
        f'<text x="{W / 2}" y="27" text-anchor="middle" class="title">karamjit — zsh</text>',
    ]
    for i, (kind, text) in enumerate(LINES):
        y = TOP + i * LINE_H
        if kind == "cmd":
            body = f'<tspan class="prompt">{escape(PROMPT)}</tspan>{escape(text)}'
        else:
            body = styled(text)
        parts.append(f'<text x="{PAD}" y="{y}" class="ln l{i}">{body}</text>')
    cursor_y = TOP + len(LINES) * LINE_H
    parts.append(
        f'<text x="{PAD}" y="{cursor_y}" class="ln l{len(LINES) - 1}">'
        f'<tspan class="prompt">{escape(PROMPT)}</tspan><tspan class="cursor">█</tspan></text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "terminal.svg"
    out.write_text(build(), encoding="utf-8")
    print(f"wrote {out}")
