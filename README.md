# ⚡ SpeedySearch Pro

> **Algorithm Benchmark Lab** — live empirical runtime analysis of three fundamental search strategies, side-by-side on datasets up to 5 million elements.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/deps-streamlit%20%7C%20pandas%20%7C%20numpy-informational)]()

---

## What is this?

SpeedySearch Pro is an interactive Streamlit web app that benchmarks three classic search algorithms **live on your machine** and visualises the results:

| Algorithm | Data structure | Time complexity |
|-----------|---------------|-----------------|
| Linear Search | Unsorted list | O(N) |
| Binary Search | Sorted list | O(log N) |
| Set Lookup | Python hash set | O(1) amortised |

You pick a dataset size (10 K → 5 M elements), choose a search scenario (best / average / worst case), hit **Run Benchmark**, and get exact timing numbers, speedup ratios, and charts — all rendered in milliseconds.

---

## Features

- **Live benchmarking** — `time.perf_counter` measurements run directly in your Python process so results reflect your hardware.
- **Three scenarios** — worst-case (target at end), average-case (target in middle), best-case (target at start). Scenario choice directly affects linear search time while binary and set are unaffected.
- **Hand-drawn SVG charts** — every visual (bar chart, log/log growth curves, multi-size sweep) is generated as raw SVG strings. Zero Plotly, zero Matplotlib.
  - *Bar chart* — horizontal bars with exact time labels.
  - *Growth curves* — log/log plot of O(N) vs O(log N) vs O(1) from N=10 to N=10 M with your selected N marked.
  - *Sweep chart* — benchmarks 8 evenly-spaced sizes from 10 K to your chosen N and plots all three algorithms together.
- **Comparison table** — steps taken, measured time, speedup ratio, and preprocessing cost in a `st.dataframe`.
- **Dark terminal UI** — custom CSS using JetBrains Mono (numbers/code) + Inter (prose), electric-blue / red / green accent system, no default Streamlit chrome.
- **Minimal dependencies** — only `streamlit`, `pandas`, and `numpy`. No chart libraries.

---

## Quick start

```bash
# 1. Clone
git clone https://github.com/your-username/speedysearch-pro.git
cd speedysearch-pro

# 2. Install dependencies
pip install streamlit pandas numpy

# 3. Run
streamlit run app.py
```

The app opens at `http://localhost:8501` in your default browser.

---

## Project structure

```
speedysearch-pro/
├── app.py          # Single-file Streamlit application
├── README.md       # This file
├── requirements.txt
└── LICENSE
```

### `requirements.txt`

```
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.23.0
```

---

## How the benchmark works

```python
# Build structures once
data        = list(range(n))   # unsorted list
sorted_list = data[:]          # sorted list (range is already monotonic)
data_set    = set(data)        # hash set — O(N) construction

# Time each search independently
t0 = time.perf_counter()
target in data                  # O(N) linear scan
linear_time = time.perf_counter() - t0

t0 = time.perf_counter()
binary_search(sorted_list, target)  # O(log N) iterative halving
binary_time = time.perf_counter() - t0

t0 = time.perf_counter()
target in data_set              # O(1) hash lookup
set_time = time.perf_counter() - t0
```

The binary search is a pure-Python iterative implementation (no `bisect`) so the overhead is visible and educational.

---

## Algorithm explainer

### Linear Search — O(N)

Scans every element from index 0 until the target is found or the list is exhausted. No preprocessing required. At 5 M elements, worst-case means 5 million comparisons. Simple and universally applicable, but cost scales directly with dataset size.

### Binary Search — O(log N)

Requires a **sorted** array. Repeatedly halves the search space by comparing the target to the midpoint element:

- If equal → found.
- If target is smaller → discard the right half.
- If target is larger → discard the left half.

At 5 M elements the maximum number of comparisons is `ceil(log₂(5_000_000))` = **23** — roughly a 200,000× reduction in worst-case steps compared to linear search.

### Set Lookup — O(1)

Python's `set` is backed by a hash table. Looking up an element:
1. Computes `hash(target)`.
2. Maps the hash to a bucket index.
3. Checks only that bucket (a handful of items on average, regardless of N).

Each lookup is effectively constant-time. The trade-off is O(N) construction time and roughly 2–3× the memory of a plain list.

---

## Interpreting results

- **Set wins on repeat lookups** — if you build the set once and search many times, amortised cost per lookup is negligible.
- **Binary search wins on sorted data you already have** — no extra memory beyond the sorted array, and log N is very fast in practice.
- **Linear wins for tiny datasets or one-off searches** — no preprocessing cost, simpler code, and for very small N the constant factors of hashing can make linear competitive.
- **Scenario matters for linear** — worst-case is N comparisons, best-case is 1. Binary and set are unaffected by where the target sits.

---

## Customisation

| What | Where |
|------|-------|
| Slider range (dataset size) | `st.slider` call in the sidebar section of `app.py` |
| Number of sweep points | `np.linspace(10_000, n_elements, 8)` — change `8` |
| Colour palette | CSS `:root` variables at the top of the `<style>` block |
| Chart dimensions | `width` / `height` keyword args to `svg_bar`, `svg_growth`, `svg_sweep` |

---

## License

MIT — see [LICENSE](LICENSE).

---

## Acknowledgements

Built with [Streamlit](https://streamlit.io). Typography: [JetBrains Mono](https://www.jetbrains.com/lp/mono/) + [Inter](https://rsms.me/inter/).
