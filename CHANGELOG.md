# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [1.0.0] — 2022-05-19

### Added
- Initial release of WinDrift
- `windrift.py` — single-file implementation of the concept drift detector
- Mode I (Consecutive): detects drift between adjacent time windows within a cycle
- Mode II (Corresponding): detects drift between same-period windows across cycles
- ECDF-based KS detection via `scipy.stats.percentileofscore`
- Critical value formula: `D_crit = 1.36 × √(1/n + 1/m)`
- Configurable window levels via `win_lev_size` array — supports W = 1, 3, 6, 12
- CSV data loader supporting variable column counts
- Console output of per-comparison drift flags for both modes
- Optional CDF plots via `showgraphs` flag (matplotlib)
- Debug output via `debugflag` and `printvaluesflag` toggles
- `runnative` and `runcorresponding` flags to enable/disable each mode independently
