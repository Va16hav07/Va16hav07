"""Generates the SVG panels used by README.md.

Edit the data below and run:  python3 scripts/build_assets.py
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

BG = "#0b0f14"
PANEL = "#111821"
BORDER = "#1e2a36"
TRACE = "#1b2733"
ACCENT = "#3ddc97"
TEXT = "#e6edf3"
MUTED = "#8b98a5"
DIM = "#4f5d6b"

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

STYLE = f"""<style>
.m{{font-family:{MONO}}}
.s{{font-family:{SANS}}}
.pulse{{animation:pulse 1.6s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.2}}}}
.ring{{transform-box:fill-box;transform-origin:center;animation:ring 2s ease-out infinite}}
@keyframes ring{{0%{{transform:scale(.6);opacity:.9}}100%{{transform:scale(2.4);opacity:0}}}}
.flow{{stroke-dasharray:10 600;animation:flow 3.2s linear infinite}}
@keyframes flow{{from{{stroke-dashoffset:610}}to{{stroke-dashoffset:0}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>"""


def svg(w, h, body, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">'
        f"<title>{escape(label)}</title>{STYLE}{body}</svg>\n"
    )


def card(w, h):
    return (
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" '
        f'fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>'
    )


def text(x, y, s, cls, size, fill, anchor="start", weight=400, extra=""):
    return (
        f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" fill="{fill}" '
        f'font-weight="{weight}" text-anchor="{anchor}" {extra}>{escape(s)}</text>'
    )


def trace(points, delay):
    d = "M" + " L".join(f"{x},{y}" for x, y in points)
    end = points[-1]
    return (
        f'<path d="{d}" fill="none" stroke="{TRACE}" stroke-width="2"/>'
        f'<path d="{d}" fill="none" stroke="{ACCENT}" stroke-width="2" '
        f'stroke-linecap="round" class="flow" style="animation-delay:{delay}s"/>'
        f'<circle cx="{end[0]}" cy="{end[1]}" r="4" fill="{BG}" stroke="{TRACE}" stroke-width="2"/>'
    )


# ---------------------------------------------------------------- header
def header():
    w, h = 1200, 400
    cx, cy, half = 960, 200, 80  # chip centre and half-size
    left, right, top, bottom = cx - half, cx + half, cy - half, cy + half
    offs = [-52, -26, 0, 26, 52]

    traces, pins = [], []
    for i, o in enumerate(offs):
        y = cy + o
        # left: short stubs ending in vias
        traces.append(trace([(left - 8, y), (left - 40 - 12 * (i % 2), y)], i * 0.4))
        # right: out to the edge with a jog
        jog = 1040 + 18 * i
        traces.append(trace([(right + 8, y), (jog, y), (jog + 30, y + (o // 2)), (1175, y + (o // 2))], 0.2 + i * 0.5))
        x = cx + o
        # top and bottom: run towards the card edges
        traces.append(trace([(x, top - 8), (x, top - 40), (x + o // 3, top - 70), (x + o // 3, 28)], 0.6 + i * 0.35))
        traces.append(trace([(x, bottom + 8), (x, bottom + 40), (x - o // 3, bottom + 70), (x - o // 3, 372)], 1.0 + i * 0.3))
        for px, py, pw, ph in (
            (left - 9, y - 4, 9, 8), (right, y - 4, 9, 8),
            (x - 4, top - 9, 8, 9), (x - 4, bottom, 8, 9),
        ):
            pins.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="1.5" fill="#2b3a48"/>')

    chip = (
        f'<rect x="{left}" y="{top}" width="{2*half}" height="{2*half}" rx="12" '
        f'fill="{PANEL}" stroke="#2b3a48" stroke-width="2"/>'
        f'<rect x="{left+14}" y="{top+14}" width="{2*half-28}" height="{2*half-28}" rx="6" '
        f'fill="none" stroke="{BORDER}" stroke-dasharray="3 4"/>'
        f'<circle cx="{left+22}" cy="{top+22}" r="4" fill="{DIM}"/>'
        + text(cx, cy + 14, "AI", "m", 48, ACCENT, "middle", 700)
        + text(cx, cy + 40, "VK-01", "m", 12, MUTED, "middle", extra='letter-spacing="3"')
    )

    body = (
        card(w, h)
        + '<defs><pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
        f'<circle cx="1.5" cy="1.5" r="1.2" fill="#16202a"/></pattern></defs>'
        f'<rect x="2" y="2" width="{w-4}" height="{h-4}" rx="13" fill="url(#dots)"/>'
        + "".join(traces) + "".join(pins) + chip
        + text(60, 62, "VK-01  //  PROFILE.README", "m", 13, DIM, extra='letter-spacing="1.5"')
        + "<g>"
        f'<rect x="60" y="92" width="196" height="30" rx="15" fill="#0f2a1f" stroke="#1d4d38"/>'
        f'<circle cx="80" cy="107" r="5" fill="{ACCENT}" class="pulse"/>'
        + text(94, 112, "STATUS: BUILDING", "m", 13, ACCENT, weight=600, extra='letter-spacing="1"')
        + text(58, 200, "Vaibhav Kumawat", "s", 64, TEXT, weight=700)
        + f'<text x="60" y="248" class="s" font-size="26" fill="{TEXT}">Working on a startup, '
        f'<tspan fill="{ACCENT}" font-weight="600">in stealth</tspan>.</text>'
        + text(60, 288, "AI agents  ·  voice  ·  MCP  ·  full stack", "s", 18, MUTED)
        + text(60, 318, "3rd-year CS @ Polaris School of Technology  ·  Bengaluru", "s", 18, MUTED)
        + "</g>"
        + text(60, 368, "PREV: ZUVEES  ·  VALZY  ·  KUBESTELLAR (IFoS)", "m", 12, DIM, extra='letter-spacing="1.5"')
    )
    return svg(w, h, body, "Vaibhav Kumawat — working on a startup in stealth")



# ---------------------------------------------------------------- divider
def divider(num, title):
    w, h = 1200, 48
    tw = 14 + len(title) * 10.5
    body = (
        card(w, h)
        + text(28, 30, num, "m", 14, ACCENT, weight=700)
        + text(64, 30, title, "m", 14, TEXT, weight=600, extra='letter-spacing="3"')
        + f'<line x1="{80 + tw}" y1="24" x2="1140" y2="24" stroke="{TRACE}" stroke-width="2"/>'
        + f'<line x1="{80 + tw}" y1="24" x2="1140" y2="24" stroke="{ACCENT}" stroke-width="2" class="flow"/>'
        + f'<circle cx="1160" cy="24" r="5" fill="{ACCENT}" class="pulse"/>'
    )
    return svg(w, h, body, title.title())


# ---------------------------------------------------------------- timeline
EXPERIENCE = [
    ("JUN → AUG 2025", "IFoS Intern", "KubeStellar", "open source · remote", False),
    ("JUL → DEC 2025", "Software Engineer Intern", "ZUVEES", "Bengaluru · on-site", False),
    ("APR → SEP 2026", "Intern", "Valzy", "valzy.co.in", False),
    ("NOW", "Working on", "A startup", "in stealth", True),
]


def timeline():
    w, h = 1200, 270
    xs = [180, 460, 740, 1020]
    y = 120
    parts = [
        card(w, h),
        text(40, 44, "LOG // EXPERIENCE", "m", 13, DIM, extra='letter-spacing="1.5"'),
        f'<line x1="70" y1="{y}" x2="1130" y2="{y}" stroke="{TRACE}" stroke-width="3"/>',
        f'<line x1="70" y1="{y}" x2="1130" y2="{y}" stroke="{ACCENT}" stroke-width="3" '
        f'class="flow" style="animation-duration:4s"/>',
    ]
    for x, (date, role, org, note, now) in zip(xs, EXPERIENCE):
        colour = ACCENT if now else MUTED
        parts.append(text(x, y - 30, date, "m", 13, colour, "middle", 600, 'letter-spacing="1"'))
        if now:
            parts.append(f'<circle cx="{x}" cy="{y}" r="9" fill="none" stroke="{ACCENT}" stroke-width="2" class="ring"/>')
        parts.append(
            f'<circle cx="{x}" cy="{y}" r="8" fill="{ACCENT if now else BG}" '
            f'stroke="{ACCENT if now else "#3a4a5a"}" stroke-width="3"/>'
        )
        parts.append(text(x, y + 46, role, "s", 18, TEXT, "middle", 700))
        parts.append(text(x, y + 72, org, "s", 16, ACCENT, "middle", 600))
        parts.append(text(x, y + 96, note, "m", 12, DIM, "middle"))
    return svg(w, h, "".join(parts), "Experience timeline")


# ---------------------------------------------------------------- project cards
PROJECTS = [
    ("peak", "INCIDENT RESPONSE", "TEAM BUILD", "PEAK",
     ["Finds the commit that broke production from Sentry and",
      "GitHub, posts the root cause, reverts after approval."],
     ["Python", "MCP", "Sentry", "Slack"]),
    ("ojt", "DOC AUTOMATION", "TOP REPO", "OJT Journal Maker",
     ["Turns an internship summary into day-by-day journal",
      "entries and fills the PDF template automatically."],
     ["FastAPI", "Gemini", "PDF"]),
    ("aria", "VOICE AI", "OPEN SOURCE", "Voice Agent Aria",
     ["Voice assistant with tool-calling to-dos and long-term",
      "memory, running on Groq's fast inference."],
     ["Flask", "Groq", "Web Speech"]),
    ("travel", "MULTI-AGENT", "OPEN SOURCE", "Multi-Agent Travel Planner",
     ["Four specialised agents collaborate to turn a free-text",
      "request into a complete, budgeted travel plan."],
     ["LangGraph", "LangChain", "Python"]),
]


def project(tag, status, title, lines, chips):
    w, h = 600, 220
    parts = [
        card(w, h),
        f'<rect x="1" y="30" width="4" height="60" rx="2" fill="{ACCENT}"/>',
        text(32, 44, tag, "m", 12, DIM, extra='letter-spacing="1.5"'),
        f'<circle cx="{w - 40 - len(status) * 8.4}" cy="40" r="4" fill="{ACCENT}" class="pulse"/>',
        text(w - 28, 44, status, "m", 12, ACCENT, "end", 600, 'letter-spacing="1"'),
        text(32, 88, title, "s", 26, TEXT, weight=700),
    ]
    for i, line in enumerate(lines):
        parts.append(text(32, 122 + i * 22, line, "s", 15, MUTED))
    x = 32
    for c in chips:
        cw = len(c) * 7.6 + 22
        parts.append(f'<rect x="{x}" y="166" width="{cw}" height="28" rx="14" fill="{PANEL}" stroke="{BORDER}"/>')
        parts.append(text(x + cw / 2, 184, c, "m", 12, TEXT, "middle"))
        x += cw + 8
    return svg(w, h, "".join(parts), f"{title}: {' '.join(lines)}")


# ---------------------------------------------------------------- footer
def footer():
    w, h = 1200, 80
    body = (
        card(w, h)
        + f'<circle cx="40" cy="40" r="5" fill="{ACCENT}" class="pulse"/>'
        + text(58, 45, "EOF", "m", 14, ACCENT, weight=700, extra='letter-spacing="2"')
        + text(110, 45, "thanks for scrolling. let's build something that thinks.", "m", 14, MUTED)
        + text(1160, 45, "VK-01 · REV 3.0", "m", 12, DIM, "end", extra='letter-spacing="1.5"')
    )
    return svg(w, h, body, "End of profile")


def main():
    OUT.mkdir(exist_ok=True)
    files = {
        "header.svg": header(),
        "experience.svg": timeline(),
        "footer.svg": footer(),
        "div-about.svg": divider("01", "ABOUT"),
        "div-experience.svg": divider("02", "EXPERIENCE"),
        "div-projects.svg": divider("03", "SELECTED WORK"),
        "div-stack.svg": divider("04", "STACK"),
        "div-stats.svg": divider("05", "ACTIVITY"),
    }
    for slug, *rest in PROJECTS:
        files[f"project-{slug}.svg"] = project(*rest)
    for name, content in files.items():
        (OUT / name).write_text(content)
    print(f"wrote {len(files)} files to {OUT}")


if __name__ == "__main__":
    main()
