# WinDrift

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**WinDrift** — Early Detection of Concept Drift Using Corresponding and Hierarchical Time Window.
> N. Naqvi, S. U. Rehman, and M. Z. Islam, “WinDrift: Early Detection of Concept Drift Using Corresponding and Hierarchical Time Windows,” in Australasian Conference on Data Mining. Australia: Springer, 2022, pp. 73–89.

---

## 📄 Abstract
In today's interconnected society, large volumes of time-series data are usually collected from real-time applications. This data is generally used for data-driven decision-making. With time, changes may emerge in the statistical characteristics of this data - this is also known as _concept drift_. A concept drift can be detected using a concept drift detector. An ideal detector should detect drift accurately and efficiently. However, these properties may not be easy to achieve. To address this gap, a novel drift detection method _WinDrift (WD)_ is presented in this research. The foundation of WD is the early detection of concept drift using corresponding and hierarchical time windows. To assess drift, the proposed method uses two sample hypothesis tests with Kolmogorov-Smirnov (KS) statistical distance. These tests are carried out on sliding windows configured on multiple hierarchical levels that assess drift by comparing statistical distance between two windows of corresponding time period on each level. To evaluate the efficacy of WD, 4 real datasets and 10 reproducible synthetic datasets are used. A comparison with 5 existing state-of-the-art drift detection methods demonstrates that WinDrift detects drift efficiently with minimal false alarms and has efficient computational resource usage. 

Synthetic datasets and the WD code designed for this work have been made publicly available at https://github.com/Naureenaqvi/windrift. 

---

## 💡 Impact Statement
Modern data-driven systems increasingly rely on continuous time-series streams from real-time applications such as IoT sensing, smart infrastructure, finance, and cyber-security. In these settings, undetected or delayed concept drift can silently degrade predictive models, leading to unstable decisions, unnecessary retraining, and increased operational cost. This research introduced _WinDrift (WD)_ as an early and efficient drift detection technique designed specifically for long-running streaming environments with limited computational resources.

The key impact of WinDrift lies in demonstrating that reliable and timely drift detection can be achieved without complex models or excessive computation. By exploiting corresponding and hierarchical time windows, WD enables earlier detection of meaningful distributional change while substantially reducing false alarms. This improves the stability of downstream learning systems and allows adaptation to be triggered only when truly necessary, preserving useful model structure over time.

WinDrift provides a practical foundation for scalable stream-learning systems by balancing detection accuracy, responsiveness, and computational efficiency. Its lightweight design makes it suitable for continuous deployment in resource-constrained environments, where traditional detectors struggle to operate reliably. By releasing the implementation and benchmark datasets openly, this work also supports reproducible research and establishes a baseline upon which more advanced adaptive and context-aware drift regulation frameworks, including subsequent WinDrift extensions, are built.

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

## Citation

```bibtex
@inproceedings{naqvi2022windrift,
  title={WinDrift: Early Detection of Concept Drift Using Corresponding and Hierarchical Time Windows},
  author={Naqvi, Naureen and Rehman, Sabih Ur and Islam, Md Zahidul},
  booktitle={Australasian Conference on Data Mining},
  pages={73--89},
  year={2022},
  organization={Springer}
}
```

## License

MIT License. See [LICENSE](LICENSE).
