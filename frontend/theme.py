"""Cortex visual identity — ISO 7010 safety-sign system.

Color encodes meaning, never decoration:
  yellow #FFC400 = warning / brand marker     blue  #005EB8 = mandatory action
  green  #2E7D4F = safe condition / correct   red   #D63A2F = prohibition / error
"""
import streamlit as st

INK = "#1A2332"
PAPER = "#F7F8F6"
YELLOW = "#FFC400"
BLUE = "#005EB8"
GREEN = "#2E7D4F"
RED = "#D63A2F"

_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"], .stMarkdown, p, li {{
    font-family: 'IBM Plex Sans', sans-serif;
    color: {INK};
}}

h1, h2, h3 {{
    font-family: 'Barlow Condensed', sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 0.02em;
    color: {INK};
}}

/* Brand header: name + yellow hazard rule */
.cx-brand {{
    display: flex; align-items: baseline; gap: 0.6rem;
    border-bottom: 4px solid {YELLOW};
    padding-bottom: 0.4rem; margin-bottom: 0.2rem;
}}
.cx-brand .cx-name {{
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700; font-size: 2.4rem; text-transform: uppercase;
    letter-spacing: 0.04em; line-height: 1;
}}
.cx-brand .cx-name::before {{
    content: ""; display: inline-block;
    width: 0.7em; height: 0.7em; margin-right: 0.35rem;
    background: {YELLOW}; vertical-align: baseline;
}}
.cx-eyebrow {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem; letter-spacing: 0.14em; text-transform: uppercase;
    color: {INK}; opacity: 0.65;
}}

/* Citation permit-tags — the signature element */
.cx-tags {{ margin-top: 0.6rem; }}
.cx-tag {{
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace; font-size: 0.78rem;
    padding: 0.15rem 0.55rem; margin: 0 0.4rem 0.3rem 0;
    border: 1px solid {INK}; border-left: 6px solid {YELLOW};
    background: #FFFFFF; color: {INK};
}}
.cx-confidence {{
    font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem;
    letter-spacing: 0.1em; text-transform: uppercase; opacity: 0.6;
}}

/* Buttons: mandatory-action blue */
.stButton > button, .stFormSubmitButton > button {{
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 600; font-size: 1.05rem;
    text-transform: uppercase; letter-spacing: 0.06em;
    background: {BLUE}; color: #FFFFFF;
    border: none; border-radius: 2px;
    padding: 0.45rem 1.4rem;
}}
.stButton > button:hover, .stFormSubmitButton > button:hover {{
    background: #004A94; color: #FFFFFF;
}}
.stButton > button:focus-visible, .stFormSubmitButton > button:focus-visible {{
    outline: 3px solid {YELLOW}; outline-offset: 2px;
}}

/* Quiz verdict rows */
.cx-correct {{ border-left: 6px solid {GREEN}; padding: 0.4rem 0.8rem; background: #EDF5EF; margin-bottom: 0.3rem; }}
.cx-wrong   {{ border-left: 6px solid {RED};   padding: 0.4rem 0.8rem; background: #FBEEEC; margin-bottom: 0.3rem; }}

/* Winner chip on eval dashboard */
.cx-winner {{
    display: inline-block; font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem; letter-spacing: 0.08em; text-transform: uppercase;
    padding: 0.1rem 0.5rem; background: {GREEN}; color: #FFFFFF;
}}

/* Tabs */
.stTabs [data-baseweb="tab"] {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.1rem; text-transform: uppercase; letter-spacing: 0.05em;
}}

/* Top decoration strip: solid hazard yellow, not the default gradient */
[data-testid="stDecoration"] {{
    background: {YELLOW};
}}

/* Metrics and tables compare numbers — keep digits aligned */
[data-testid="stMetricValue"], .stDataFrame, .cx-tag {{
    font-variant-numeric: tabular-nums;
}}

@media (prefers-reduced-motion: reduce) {{
    * {{ animation: none !important; transition: none !important; }}
}}
</style>
"""


def inject_theme():
    st.markdown(_CSS, unsafe_allow_html=True)


def brand_header(eyebrow: str):
    st.markdown(
        f'<div class="cx-eyebrow">{eyebrow}</div>'
        f'<div class="cx-brand"><span class="cx-name">Cortex</span></div>',
        unsafe_allow_html=True,
    )


def citation_tags(citations: list[dict]) -> str:
    tags = "".join(
        f'<span class="cx-tag">&sect; {c["section"]} &middot; p.{c["page"]}</span>'
        for c in citations
    )
    return f'<div class="cx-tags">{tags}</div>'
