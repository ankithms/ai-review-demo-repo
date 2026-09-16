# AI Review Demo Order Service

This repository is a compact, synthetic Python 3.12+ order-processing service used to generate authentic pull-request review data for an AI code-review product. It is deliberately separate from the product itself: no code here calls, configures, or modifies the AI code-review application.

`main` is the safe baseline. Every `demo/*` branch intentionally contains insecure, incorrect, inefficient, or hard-to-read code for review demonstrations. **Never deploy a demo branch.** All customers, tokens, addresses, deliveries, persistence, and failures are fake and remain in memory.

## Setup and tests

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
pytest
python scripts/show_demo_state.py
```

Tests automatically replace common socket entry points with a failing guard. Callback address resolution, notification delivery, and callback delivery are injected; the service never needs public network access.

## Architecture

The package uses a `src` layout. `models.py` contains the domain dataclasses; `validation.py`, `catalog.py`, `pricing.py`, and `inventory.py` implement the processing stages; `repositories.py` provides tenant-scoped in-memory idempotency; `notifications.py`, `audit.py`, and `callbacks.py` isolate side effects; and `orders.py` coordinates the workflow. Protocols keep network-like behavior replaceable by deterministic fakes.

The baseline validates nonempty orders and positive quantities, bulk-loads products, calculates readable discounts, reserves inventory, compensates if persistence fails, treats post-persistence delivery errors as warnings, emits non-confidential audit data, and validates HTTPS callback destinations against resolved IP safety and an optional allowlist.

## Branches

| Branch | Purpose |
|---|---|
| `main` | Clean production-style baseline |
| `demo/single-fix` | One edge-case finding for an inline `/ai-fix` reply |
| `demo/all-categories` | Seven findings across all supported categories |
| `demo/fix-all` | Five isolated findings for top-level `/ai-fix all` |
| `demo/lifecycle` | Initial three-finding incremental-review state |
| `demo/lifecycle-step-2` | Local preparation branch with the manual LC-2 fix |
| `demo/lifecycle-step-3` | Local preparation branch with relocated LC-3 code |
| `demo/manual-actions` | Ignore, manual resolution, and coordinated-review examples |

See [DEMO_EXPECTATIONS.md](DEMO_EXPECTATIONS.md) for the finding contract and [DEMO_SCRIPT.md](DEMO_SCRIPT.md) for presenter commands. AI review output is nondeterministic, so documented classifications and counts are targets rather than guarantees.

