# WinDrift

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Python implementation of **WinDrift** — a concept drift detector that compares data distributions across sliding time windows using the Kolmogorov–Smirnov statistical test.

---

## Algorithm Overview

WinDrift detects distributional change between time windows by computing the empirical CDF of each window and measuring the maximum absolute difference. If this exceeds a critical value, drift is flagged.

**Two detection modes:**
- **Mode I (Consecutive):** compares adjacent windows — e.g. January vs February within the same year
- **Mode II (Corresponding):** compares same-period windows across years — e.g. January 2019 vs January 2020

**Window levels:** configurable via `win_lev_size` — supports monthly (1), quarterly (3), semi-annual (6), and annual (12) comparisons.

---

## Project Structure

```
windrift/
├── windrift.py          ← Main script — run this
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Requirements

```
Python 3.9+
numpy
pandas
scipy
matplotlib
psutil
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Configuration

All settings are defined at the top of `windrift.py`:

```python
# **** Flags ****
debugflag          = 0     # 1 = print debug output
printvaluesflag    = 0     # 1 = print d_stat and d_crit values
showgraphs         = 0     # 1 = display CDF plots
runnative          = 1     # 1 = run Mode I (Consecutive)
runcorresponding   = 1     # 1 = run Mode II (Corresponding)

# **** Constants ****
win_lev_size  = [12, 1, 6, 3]   # window sizes in months
alpha         = 0.5              # plot transparency
```

Set the path to your input CSV:
```python
datacsvpath = 'path/to/your/data.csv'
```

---

## Input Format

The input is a CSV file where:
- **Row 1:** column headers (e.g. month labels: `Jan-2019`, `Feb-2019`, ...)
- **Rows 2+:** observations for that month (one observation per row)
- **Each column** represents one time period

Example (5 observations, 4 months):
```
Jan-2019, Feb-2019, Mar-2019, Apr-2019
4.2, 4.8, 5.1, 7.9
3.9, 5.0, 4.7, 8.1
4.1, 4.6, 5.3, 7.7
4.4, 5.2, 4.9, 8.3
3.8, 4.9, 5.0, 7.5
```

---

## Running

```bash
python windrift.py
```

Output is printed to the console:
```
results for mode 1
dflag for  Jan-2019 VS Feb-2019 : 0
dflag for  Feb-2019 VS Mar-2019 : 0
...
*****************************
results for mode 2
dflag for  dbcount : 13 win level 1 Jan-2019 VS Jan-2020 : 1
...
```

A drift flag of `1` indicates distributional change was detected between the two windows. A flag of `0` indicates no significant change.

---

## How It Works

### ECDF Comparison

For two windows X and Y, WinDrift:
1. Merges and sorts all values into a combined array
2. Computes the empirical CDF of X and Y over the combined points using `scipy.stats.percentileofscore`
3. Computes the maximum absolute difference: `D_stat = max|F(x) - G(x)|`
4. Computes the critical value: `D_crit = 1.36 × √(1/n + 1/m)`
5. Flags drift if `D_stat ≥ D_crit`

### Window Construction

For window level W > 1, WinDrift aggregates W consecutive columns into a single block before comparison, allowing detection of drift across longer time horizons.

---

## License

MIT License. See [LICENSE](LICENSE).
