import streamlit as st
import time
import math
import pandas as pd
import numpy as np

st.set_page_config(page_title="SpeedySearch Pro", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
:root{--bg:#0c0e14;--surf:#12151f;--border:#1e2235;--text:#c8d0e0;--muted:#525d75;--blue:#4f8ef7;--cyan:#20d4ea;--red:#f25f5c;--green:#29c98f;--amber:#f5a623;--mono:'JetBrains Mono',monospace;--sans:'Inter',sans-serif;}
html,body,[class*="css"]{background-color:var(--bg)!important;color:var(--text)!important;font-family:var(--sans);}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding-top:1.8rem!important;max-width:1200px;}
.hero{background:linear-gradient(120deg,#0c1424 0%,#0c0e14 70%);border:1px solid var(--border);border-left:4px solid var(--blue);border-radius:12px;padding:2rem 2.4rem 1.6rem;margin-bottom:1.8rem;position:relative;overflow:hidden;}
.hero::after{content:'⚡';position:absolute;right:2rem;top:1.2rem;font-size:5rem;opacity:0.04;pointer-events:none;}
.eyebrow{font-family:var(--mono);font-size:0.65rem;letter-spacing:0.22em;text-transform:uppercase;color:var(--cyan);margin-bottom:0.5rem;}
.hero h1{font-family:var(--mono);font-size:2.2rem;font-weight:700;color:#fff;margin:0 0 0.45rem;line-height:1.1;}
.hero h1 em{color:var(--blue);font-style:normal;}
.hero p{color:var(--muted);font-size:0.9rem;line-height:1.65;max-width:640px;margin:0;}
.sec{font-family:var(--mono);font-size:0.62rem;letter-spacing:0.22em;text-transform:uppercase;color:var(--cyan);border-bottom:1px solid var(--border);padding-bottom:0.45rem;margin:1.8rem 0 1.1rem;}
.acard{background:var(--surf);border:1px solid var(--border);border-radius:10px;padding:1.3rem 1.4rem;height:100%;}
.acard .badge{display:inline-block;font-family:var(--mono);font-size:0.62rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;padding:0.18rem 0.55rem;border-radius:4px;margin-bottom:0.7rem;}
.badge-r{background:rgba(242,95,92,0.12);color:var(--red);}
.badge-b{background:rgba(79,142,247,0.12);color:var(--blue);}
.badge-g{background:rgba(41,201,143,0.12);color:var(--green);}
.acard h3{font-family:var(--mono);font-size:0.95rem;font-weight:700;color:#fff;margin:0 0 0.3rem;}
.acard .big{font-family:var(--mono);font-size:1.55rem;font-weight:700;margin:0.4rem 0 0.45rem;line-height:1;}
.big-r{color:var(--red);}.big-b{color:var(--blue);}.big-g{color:var(--green);}
.acard p{font-size:0.8rem;color:var(--muted);line-height:1.55;margin:0;}
.rcard{background:var(--surf);border:1px solid var(--border);border-radius:10px;padding:1.4rem;text-align:center;}
.rcard .rlabel{font-family:var(--mono);font-size:0.6rem;letter-spacing:0.18em;text-transform:uppercase;color:var(--muted);margin-bottom:0.55rem;}
.rcard .rval{font-family:var(--mono);font-size:1.75rem;font-weight:700;line-height:1;}
.rcard .rsub{font-size:0.75rem;color:var(--muted);margin-top:0.4rem;}
.insight{background:rgba(79,142,247,0.05);border:1px solid rgba(79,142,247,0.18);border-radius:10px;padding:1.1rem 1.4rem;margin-top:1rem;}
.insight .ilabel{font-family:var(--mono);font-size:0.6rem;letter-spacing:0.18em;text-transform:uppercase;color:var(--cyan);margin-bottom:0.4rem;}
.insight p{font-size:0.85rem;color:var(--text);margin:0;line-height:1.65;}
.srow{display:flex;gap:0.8rem;align-items:flex-start;margin-bottom:0.75rem;}
.snum{font-family:var(--mono);font-size:0.62rem;font-weight:700;color:var(--blue);background:rgba(79,142,247,0.1);border-radius:4px;padding:0.2rem 0.45rem;white-space:nowrap;margin-top:2px;}
.stxt{font-size:0.8rem;color:var(--muted);line-height:1.5;}
.stxt strong{color:var(--text);}
.chart-wrap{background:var(--surf);border:1px solid var(--border);border-radius:10px;padding:1.2rem 0.6rem 0.8rem;margin-top:0.5rem;}
section[data-testid="stSidebar"]{background:var(--surf)!important;border-right:1px solid var(--border)!important;}
.stButton>button{background:var(--blue)!important;color:#fff!important;border:none!important;font-family:var(--mono)!important;font-size:0.82rem!important;font-weight:600!important;letter-spacing:0.05em!important;border-radius:8px!important;padding:0.55rem 1.8rem!important;}
.stButton>button:hover{opacity:0.82!important;}
.stTabs [data-baseweb="tab-list"]{background:var(--surf);border-radius:8px;padding:3px;gap:3px;border:1px solid var(--border);}
.stTabs [data-baseweb="tab"]{font-family:var(--mono)!important;font-size:0.74rem!important;color:var(--muted)!important;background:transparent!important;border-radius:6px!important;}
.stTabs [aria-selected="true"]{background:var(--blue)!important;color:#fff!important;}
code{font-family:var(--mono)!important;background:rgba(79,142,247,0.09)!important;color:var(--cyan)!important;padding:0.08rem 0.38rem!important;border-radius:3px!important;font-size:0.8rem!important;}
</style>
""", unsafe_allow_html=True)

# ── helpers ──────────────────────────────────
def fmt_time(t):
    if t < 1e-3: return f"{t*1e6:.1f} µs"
    elif t < 1:  return f"{t*1e3:.2f} ms"
    return f"{t:.4f} s"

def binary_search(arr, target):
    lo, hi = 0, len(arr)-1
    while lo <= hi:
        mid = (lo+hi)//2
        if arr[mid] == target: return True
        elif arr[mid] < target: lo = mid+1
        else: hi = mid-1
    return False

def run_benchmark(n, scenario):
    data = list(range(n))
    sl = data[:]
    ds = set(data)
    target = {"worst": n-1, "best": 0, "average": n//2}[scenario]
    t0 = time.perf_counter(); _ = target in data;          lt = time.perf_counter()-t0
    t0 = time.perf_counter(); _ = binary_search(sl, target); bt = time.perf_counter()-t0
    t0 = time.perf_counter(); _ = target in ds;             st = time.perf_counter()-t0
    return lt, bt, st, target

# ── SVG charts ───────────────────────────────
def svg_bar(times, width=660, height=175):
    labels = list(times.keys())
    vals   = list(times.values())
    max_v  = max(vals) if max(vals) > 0 else 1
    cols   = {"Linear O(N)":"#f25f5c","Binary O(log N)":"#4f8ef7","Set O(1)":"#29c98f"}
    ml, mr, bar_h, gap = 164, 130, 31, 17
    svg = [f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block;"><rect width="{width}" height="{height}" fill="transparent"/>']
    for i,(label,val) in enumerate(zip(labels, vals)):
        y   = 14 + i*(bar_h+gap)
        bw  = max(3, int((val/max_v)*(width-ml-mr)))
        col = cols.get(label, "#4f8ef7")
        svg.append(f'<rect x="{ml}" y="{y}" width="{width-ml-mr}" height="{bar_h}" rx="5" fill="#1e2235"/>')
        svg.append(f'<rect x="{ml}" y="{y}" width="{bw}" height="{bar_h}" rx="5" fill="{col}" opacity="0.88"/>')
        svg.append(f'<text x="{ml-10}" y="{y+bar_h//2+5}" font-family="JetBrains Mono,monospace" font-size="11" fill="#c8d0e0" text-anchor="end">{label}</text>')
        svg.append(f'<text x="{ml+bw+8}" y="{y+bar_h//2+5}" font-family="JetBrains Mono,monospace" font-size="11" fill="{col}">{fmt_time(val)}</text>')
    svg.append('</svg>')
    return ''.join(svg)

def svg_growth(n_max, width=700, height=295):
    ml,mr,mt,mb = 60,20,22,42
    pw, ph = width-ml-mr, height-mt-mb
    ns = [10**(i*0.12) for i in range(9, 63)]
    ns = [n for n in ns if n <= max(n_max*2, 1e7)]
    log_min = math.log10(ns[0]);  log_max = math.log10(ns[-1])
    log_max_y = log_max+0.5;      log_min_y = -0.2
    def cx(n): return ml + (math.log10(n)-log_min)/(log_max-log_min)*pw
    def cy(ops):
        ops = max(ops, 0.6)
        return mt + ph - (math.log10(ops)-log_min_y)/(log_max_y-log_min_y)*ph
    def poly(pts, col):
        p = " ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
        return f'<polyline points="{p}" fill="none" stroke="{col}" stroke-width="2.2" stroke-linejoin="round"/>'
    svg = [f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block;"><rect width="{width}" height="{height}" fill="transparent"/>']
    for exp in range(1, 8):
        ng = 10**exp
        if ng > ns[-1]*1.2: break
        x = cx(ng)
        svg.append(f'<line x1="{x:.1f}" y1="{mt}" x2="{x:.1f}" y2="{mt+ph}" stroke="#1e2235" stroke-width="1"/>')
        svg.append(f'<text x="{x:.1f}" y="{mt+ph+15}" font-family="JetBrains Mono,monospace" font-size="9" fill="#525d75" text-anchor="middle">10^{exp}</text>')
    for oe in range(0, 8):
        og = 10**oe; yg = cy(og)
        if yg < mt or yg > mt+ph: continue
        svg.append(f'<line x1="{ml}" y1="{yg:.1f}" x2="{ml+pw}" y2="{yg:.1f}" stroke="#1e2235" stroke-width="1"/>')
        svg.append(f'<text x="{ml-6}" y="{yg+4:.1f}" font-family="JetBrains Mono,monospace" font-size="9" fill="#525d75" text-anchor="end">10^{oe}</text>')
    svg.append(poly([(cx(n), cy(n)) for n in ns], "#f25f5c"))
    svg.append(poly([(cx(n), cy(math.log2(n))) for n in ns], "#4f8ef7"))
    svg.append(poly([(cx(n), cy(1)) for n in ns], "#29c98f"))
    xm = cx(n_max)
    svg.append(f'<line x1="{xm:.1f}" y1="{mt}" x2="{xm:.1f}" y2="{mt+ph}" stroke="#f5a623" stroke-width="1.5" stroke-dasharray="5,3"/>')
    svg.append(f'<text x="{xm+4:.1f}" y="{mt+12}" font-family="JetBrains Mono,monospace" font-size="9" fill="#f5a623">N={n_max:,}</text>')
    svg.append(f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{mt+ph}" stroke="#1e2235" stroke-width="1.5"/>')
    svg.append(f'<line x1="{ml}" y1="{mt+ph}" x2="{ml+pw}" y2="{mt+ph}" stroke="#1e2235" stroke-width="1.5"/>')
    for i,(name,col) in enumerate([("O(N)  Linear","#f25f5c"),("O(log N)  Binary","#4f8ef7"),("O(1)  Set","#29c98f")]):
        ly = mt+14+i*18; lx = ml+16
        svg.append(f'<rect x="{lx}" y="{ly-7}" width="18" height="4" rx="2" fill="{col}"/>')
        svg.append(f'<text x="{lx+22}" y="{ly}" font-family="JetBrains Mono,monospace" font-size="10" fill="#c8d0e0">{name}</text>')
    svg.append(f'<text x="{ml+pw//2}" y="{height-4}" font-family="JetBrains Mono,monospace" font-size="9" fill="#525d75" text-anchor="middle">Dataset size N (log) — Y: operations (log)</text>')
    svg.append('</svg>')
    return ''.join(svg)

def svg_sweep(df, width=700, height=300):
    ml,mr,mt,mb = 72,20,22,44
    pw, ph = width-ml-mr, height-mt-mb
    ns = df["N"].tolist()
    max_t = max(df[["Linear","Binary","Set"]].values.max(), 1e-9)
    min_n, max_n = ns[0], ns[-1]
    def cx(n): return ml + (n-min_n)/(max_n-min_n)*pw if max_n != min_n else ml+pw/2
    def cy(t): return mt + ph - (t/max_t)*ph
    svg = [f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block;"><rect width="{width}" height="{height}" fill="transparent"/>']
    for i in range(5):
        yg = mt+i*ph/4; tv = max_t*(4-i)/4
        svg.append(f'<line x1="{ml}" y1="{yg:.1f}" x2="{ml+pw}" y2="{yg:.1f}" stroke="#1e2235" stroke-width="1"/>')
        svg.append(f'<text x="{ml-6}" y="{yg+4:.1f}" font-family="JetBrains Mono,monospace" font-size="9" fill="#525d75" text-anchor="end">{fmt_time(tv)}</text>')
    for cn, color in [("Linear","#f25f5c"),("Binary","#4f8ef7"),("Set","#29c98f")]:
        pts = [(cx(row["N"]), cy(row[cn])) for _,row in df.iterrows()]
        ps  = " ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
        svg.append(f'<polyline points="{ps}" fill="none" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>')
        for x,y in pts: svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{color}"/>')
    svg.append(f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{mt+ph}" stroke="#1e2235" stroke-width="1.5"/>')
    svg.append(f'<line x1="{ml}" y1="{mt+ph}" x2="{ml+pw}" y2="{mt+ph}" stroke="#1e2235" stroke-width="1.5"/>')
    step = max(1, len(ns)//5)
    for n in ns[::step]:
        x = cx(n)
        svg.append(f'<text x="{x:.1f}" y="{mt+ph+15}" font-family="JetBrains Mono,monospace" font-size="9" fill="#525d75" text-anchor="middle">{n//1000}K</text>')
    for i,(name,col) in enumerate([("Linear","#f25f5c"),("Binary","#4f8ef7"),("Set","#29c98f")]):
        ly = mt+14+i*18; lx = ml+16
        svg.append(f'<rect x="{lx}" y="{ly-7}" width="18" height="4" rx="2" fill="{col}"/>')
        svg.append(f'<text x="{lx+22}" y="{ly}" font-family="JetBrains Mono,monospace" font-size="10" fill="#c8d0e0">{name}</text>')
    svg.append(f'<text x="{ml+pw//2}" y="{height-4}" font-family="JetBrains Mono,monospace" font-size="9" fill="#525d75" text-anchor="middle">Dataset size N</text>')
    svg.append('</svg>')
    return ''.join(svg)

# ── Sidebar ───────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sec">⚙ Configuration</div>', unsafe_allow_html=True)
    n_elements = st.slider("Dataset size (N)", 10_000, 5_000_000, 1_000_000, 50_000)
    st.caption(f"**{n_elements:,}** elements · list ≈{n_elements*28//1_000_000} MB · set ≈{n_elements*8//1_000_000} MB")
    st.markdown("---")
    st.markdown('<div class="sec">🎯 Scenario</div>', unsafe_allow_html=True)
    scenario = st.radio("Target position", ["worst","average","best"],
        format_func=lambda x: {"worst":"⬇ Worst  (last element)","average":"↔ Average (middle)","best":"⬆ Best   (first element)"}[x])
    st.markdown("---")
    st.markdown('<div class="sec">📈 Sweep</div>', unsafe_allow_html=True)
    run_sweep = st.checkbox("Multi-size sweep", False, help="Benchmarks 8 sizes 10K→N and draws a line chart.")
    st.markdown("---")
    st.markdown('<p style="font-size:0.7rem;color:#525d75;line-height:1.6;">Deps: <code>streamlit</code> · <code>pandas</code> · <code>numpy</code> only. Every chart is hand-drawn SVG — no Plotly, no Matplotlib.</p>', unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="eyebrow">Algorithm Benchmark Lab</div>
  <h1>Speedy<em>Search</em> Pro ⚡</h1>
  <p>Live empirical analysis of <strong>O(N)</strong> linear search, <strong>O(log N)</strong> binary search,
  and <strong>O(1)</strong> hash-set lookup — benchmarked on your machine on up to 5 million elements.
  No external chart libraries: every visual is hand-drawn SVG.</p>
</div>""", unsafe_allow_html=True)

# ── Algo cards ────────────────────────────────
st.markdown('<div class="sec">The three contenders</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""<div class="acard"><span class="badge badge-r">Unsorted list</span><h3>Linear Search</h3>
    <div class="big big-r">O(N)</div>
    <p>Checks every element from index 0 until it finds the target or runs out of list.
    Zero preprocessing, works on any sequence — but cost grows <em>linearly</em>.
    At 5 M elements worst-case means 5 million comparisons.</p></div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="acard"><span class="badge badge-b">Sorted list</span><h3>Binary Search</h3>
    <div class="big big-b">O(log N)</div>
    <p>Requires a <em>sorted</em> array. Repeatedly halves the search space by pivoting on the midpoint.
    5 M elements → at most log₂(5 000 000) ≈ 23 comparisons.
    A ~200 000× reduction in worst-case steps vs. linear.</p></div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div class="acard"><span class="badge badge-g">Hash set</span><h3>Set Lookup</h3>
    <div class="big big-g">O(1)</div>
    <p>Python's <code>set</code> stores elements in a hash table. A lookup hashes the target,
    jumps to its bucket, checks only that slot — independent of N.
    Build cost is O(N) once; every subsequent lookup is effectively instantaneous.</p></div>""", unsafe_allow_html=True)

# ── Run button ────────────────────────────────
st.markdown("")
bc, ic = st.columns([1, 3])
with bc:
    run_bench = st.button("▶  Run Benchmark", type="primary", use_container_width=True)
with ic:
    lbls = {"worst":"worst-case (target at end)","average":"average-case (target in middle)","best":"best-case (target at start)"}
    st.markdown(f'<p style="font-size:0.8rem;color:#525d75;padding-top:0.65rem;">N = <strong style="color:#c8d0e0">{n_elements:,}</strong> · Scenario: <strong style="color:#c8d0e0">{lbls[scenario]}</strong></p>', unsafe_allow_html=True)

# ── Benchmark ─────────────────────────────────
if run_bench:
    with st.spinner("Building structures & timing searches…"):
        lt, bt, st_t, target_val = run_benchmark(n_elements, scenario)

    st.markdown('<div class="sec">Results</div>', unsafe_allow_html=True)
    sp_bl = lt/bt   if bt   > 0 else float("inf")
    sp_sl = lt/st_t if st_t > 0 else float("inf")
    sp_bs = bt/st_t if st_t > 0 else float("inf")

    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown(f'<div class="rcard" style="border-top:3px solid var(--red)"><div class="rlabel">Linear Search · O(N)</div><div class="rval" style="color:var(--red)">{fmt_time(lt)}</div><div class="rsub">Baseline · up to {n_elements:,} comparisons</div></div>', unsafe_allow_html=True)
    with r2:
        st.markdown(f'<div class="rcard" style="border-top:3px solid var(--blue)"><div class="rlabel">Binary Search · O(log N)</div><div class="rval" style="color:var(--blue)">{fmt_time(bt)}</div><div class="rsub">{sp_bl:.0f}× faster than linear · ≤{math.ceil(math.log2(n_elements))} comparisons</div></div>', unsafe_allow_html=True)
    with r3:
        st.markdown(f'<div class="rcard" style="border-top:3px solid var(--green)"><div class="rlabel">Set Lookup · O(1)</div><div class="rval" style="color:var(--green)">{fmt_time(st_t)}</div><div class="rsub">{sp_sl:.0f}× faster than linear · {sp_bs:.0f}× faster than binary</div></div>', unsafe_allow_html=True)

    winner = "hash set" if st_t <= bt else "binary search"
    st.markdown(f'<div class="insight"><div class="ilabel">💡 Analysis</div><p>Searching for element <strong>{target_val:,}</strong> in <strong>{n_elements:,}</strong> elements ({scenario}-case): linear took <strong>{fmt_time(lt)}</strong>, binary finished in <strong>{fmt_time(bt)}</strong> ({sp_bl:.0f}× faster), and the hash-set lookup completed in <strong>{fmt_time(st_t)}</strong> ({sp_sl:.0f}× faster than linear). The <strong>{winner}</strong> wins this round. Remember: set construction is O(N) — if you only search once, linear may be the more pragmatic choice.</p></div>', unsafe_allow_html=True)

    # Charts
    st.markdown('<div class="sec">Visualisations</div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["  Bar chart  ", "  Growth curves  "])
    with tab1:
        s = svg_bar({"Linear O(N)": lt, "Binary O(log N)": bt, "Set O(1)": st_t}, width=660, height=175)
        st.markdown(f'<div class="chart-wrap">{s}</div>', unsafe_allow_html=True)
    with tab2:
        s = svg_growth(n_elements, width=700, height=300)
        st.markdown(f'<div class="chart-wrap">{s}</div>', unsafe_allow_html=True)
        st.caption("Both axes log-scale. Orange line = your selected N. Y-axis = number of operations.")

    # Table
    st.markdown('<div class="sec">Comparison table</div>', unsafe_allow_html=True)
    steps_lin = {"worst": n_elements, "average": n_elements//2, "best": 1}[scenario]
    steps_bin = math.ceil(math.log2(n_elements))
    df_t = pd.DataFrame([
        {"Algorithm":"Linear Search","Complexity":"O(N)",     "Steps this run":f"{steps_lin:,}","Time":fmt_time(lt), "Speedup vs Linear":"1×",           "Preprocessing":"None"},
        {"Algorithm":"Binary Search","Complexity":"O(log N)", "Steps this run":str(steps_bin),  "Time":fmt_time(bt), "Speedup vs Linear":f"{sp_bl:.0f}×", "Preprocessing":"Sort  O(N log N)"},
        {"Algorithm":"Set Lookup",   "Complexity":"O(1)",     "Steps this run":"≈1",             "Time":fmt_time(st_t),"Speedup vs Linear":f"{sp_sl:.0f}×","Preprocessing":"Build set  O(N)"},
    ])
    st.dataframe(df_t, use_container_width=True, hide_index=True)

    # Sweep
    if run_sweep:
        st.markdown('<div class="sec">Multi-size sweep</div>', unsafe_allow_html=True)
        sizes = [int(x) for x in np.linspace(10_000, n_elements, 8)]
        recs  = []
        prog  = st.progress(0, text="Sweeping…")
        for i, sz in enumerate(sizes):
            l, b, s_t, _ = run_benchmark(sz, scenario)
            recs.append({"N": sz, "Linear": l, "Binary": b, "Set": s_t})
            prog.progress((i+1)/len(sizes), text=f"N = {sz:,}")
        prog.empty()
        df_sw = pd.DataFrame(recs)
        s = svg_sweep(df_sw, width=700, height=300)
        st.markdown(f'<div class="chart-wrap">{s}</div>', unsafe_allow_html=True)
        st.caption("Each dot = single cold measurement. Re-run to observe natural variance.")

# ── How it works ──────────────────────────────
st.markdown('<div class="sec">How each algorithm works</div>', unsafe_allow_html=True)
h1, h2, h3 = st.columns(3)
with h1:
    st.markdown("""<div class="acard"><span class="badge badge-r">Linear</span>
    <div class="srow"><div class="snum">01</div><div class="stxt"><strong>Start at index 0</strong> of the unsorted list.</div></div>
    <div class="srow"><div class="snum">02</div><div class="stxt">Compare element to target — match? Return <code>True</code>.</div></div>
    <div class="srow"><div class="snum">03</div><div class="stxt">Advance to next index; repeat until found or list ends.</div></div>
    <div class="srow"><div class="snum">04</div><div class="stxt"><strong>Worst case:</strong> target is last — N comparisons.</div></div>
    </div>""", unsafe_allow_html=True)
with h2:
    st.markdown("""<div class="acard"><span class="badge badge-b">Binary</span>
    <div class="srow"><div class="snum">01</div><div class="stxt"><strong>Prerequisite:</strong> the list must be sorted.</div></div>
    <div class="srow"><div class="snum">02</div><div class="stxt">Check the <strong>midpoint</strong> — equal to target? Done.</div></div>
    <div class="srow"><div class="snum">03</div><div class="stxt">Discard the half that cannot contain the target.</div></div>
    <div class="srow"><div class="snum">04</div><div class="stxt"><strong>Each step halves</strong> remaining space → log₂(N) max.</div></div>
    </div>""", unsafe_allow_html=True)
with h3:
    st.markdown("""<div class="acard"><span class="badge badge-g">Set</span>
    <div class="srow"><div class="snum">01</div><div class="stxt"><strong>Build once</strong> in O(N) — Python hashes every element.</div></div>
    <div class="srow"><div class="snum">02</div><div class="stxt">Lookup: compute <code>hash(target)</code> → jump to bucket.</div></div>
    <div class="srow"><div class="snum">03</div><div class="stxt">Check only that bucket (constant size on average).</div></div>
    <div class="srow"><div class="snum">04</div><div class="stxt"><strong>Cost is constant</strong> regardless of N.</div></div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")
st.markdown('<p style="font-size:0.7rem;color:#525d75;text-align:center;">SpeedySearch Pro · streamlit + pandas + numpy · all charts hand-drawn SVG · no Plotly · no Matplotlib</p>', unsafe_allow_html=True)