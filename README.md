# Nornir Network Automation Portfolio

A six-project Nornir learning track, basic -> advanced, against a two-site
spine/leaf lab (CML). Each project builds on the last; the capstone orchestrates
them into a gated NetDevOps pipeline.

![Topology](docs/topology.png)

## Projects
| # | Project | Skill | Status |
|---|---------|-------|--------|
| 01 | Inventory, connections & first tasks | Nornir fundamentals | done |
| 02 | Multi-device config backup | Custom tasks, failure handling, Git history | in progress |
| 03 | Template-driven deploy (Jinja2) | Intent + dry-run/diff/apply | planned |
| 04 | Compliance & drift detection | Structured state, collect/compare/report | planned |
| 05 | NetBox SSOT dynamic inventory | Single source of truth | planned (featured) |
| 06 | NetDevOps CI/CD pipeline | render -> validate -> deploy -> rollback | planned (featured) |

## Conventions
- One shared `inventory/` + `config.yaml` (SSOT discipline — no duplicated facts).
- Credentials load from `.env` (git-ignored); nothing secret is committed.
- Each project is a numbered folder with its own README.

## Quickstart
```
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in lab creds
```