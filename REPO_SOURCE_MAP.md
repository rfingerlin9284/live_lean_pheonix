# REPO SOURCE MAP — Where Every File Comes From

This document maps each file in the final RBOTZILLA PHOENIX system to the exact GitHub repository it comes from. Use this as a reference when the VS Code agent is assembling the project or when a file needs to be refreshed from its source.

---

## PRIMARY CODEBASE

**`rick_clean_live`** — Most recently updated (February 23, 2026). This is the primary working system for OANDA and Coinbase. Use this as the first source for any file that exists here.

GitHub: https://github.com/rfingerlin9284/rick_clean_live

| Final File | Source Path in Repo |
|---|---|
| `brokers/oanda_connector.py` | `brokers/oanda_connector.py` |
| `brokers/oanda_connector_enhanced.py` | `brokers/oanda_connector_enhanced.py` |
| `brokers/coinbase_connector.py` | `brokers/coinbase_connector.py` |
| `brokers/ib_connector.py` | `brokers/ib_connector.py` |
| `strategies/bearish_wolf.py` | `strategies/bearish_wolf.py` |
| `strategies/bullish_wolf.py` | `strategies/bullish_wolf.py` |
| `strategies/sideways_wolf.py` | `strategies/sideways_wolf.py` |
| `wolf_packs/__init__.py` | `wolf_packs/__init__.py` |
| `wolf_packs/_base.py` | `wolf_packs/_base.py` |
| `wolf_packs/extracted_oanda.py` | `wolf_packs/extracted_oanda.py` |
| `wolf_packs/orchestrator.py` | `wolf_packs/orchestrator.py` |
| `wolf_packs/stochastic_config.py` | `wolf_packs/stochastic_config.py` |
| `stochastic.py` | `stochastic.py` |
| `requirements.txt` | `requirements.txt` |
| `run_headless.py` | `run_headless.py` |
| `autonomous_trading.py` | `autonomous_trading.py` |
| `RBOTZILLA_LAUNCH.sh` | `RBOTZILLA_LAUNCH.sh` |
| `system_audit.sh` | `system_audit.sh` |
| `verify_system.py` | `verify_system.py` |
| `verify_system_ready.py` | `verify_system_ready.py` |
| `narration_daemon.py` | `narration_daemon.py` |
| `dashboard_supervisor.py` | `dashboard_supervisor.py` |
| `canary_to_live.py` | `canary_to_live.py` |
| `monitor_positions.py` | `monitor_positions.py` |
| `view_live_narration.sh` | `view_live_narration.sh` |
| `view_tmux_session.sh` | `view_tmux_session.sh` |
| `verify_live_safety.sh` | `verify_live_safety.sh` |
| `verify_paper_mode.sh` | `verify_paper_mode.sh` |
| `dashboard/dashboard.html` | `dashboard/dashboard.html` |
| `dashboard/advanced_multi_window_dashboard.html` | `dashboard/advanced_multi_window_dashboard.html` |
| `util/progress_tracker.py` | `util/progress_tracker.py` |
| `.gitignore` | `.gitignore` |

---

## STRATEGY FILES

**`Rbotzilla_pheonix_v1`** — Multi-platform version (February 22, 2026). Contains all five main strategies plus regime wolf pack files, full .env template.

GitHub: https://github.com/rfingerlin9284/Rbotzilla_pheonix_v1

| Final File | Source Path in Repo |
|---|---|
| `strategies/base.py` | `strategies/base.py` |
| `strategies/fabio_aaa_full.py` | `strategies/fabio_aaa_full.py` |
| `strategies/price_action_holy_grail.py` | `strategies/price_action_holy_grail.py` |
| `strategies/trap_reversal_scalper.py` | `strategies/trap_reversal_scalper.py` |
| `strategies/institutional_sd.py` | `strategies/institutional_sd.py` |
| `strategies/ema_scalper.py` | `strategies/ema_scalper.py` |
| `strategies/registry.py` | `strategies/registry.py` |
| `strategies/liquidity_sweep.py` | `strategies/liquidity_sweep.py` |
| `strategies/fib_confluence_breakout.py` | `strategies/fib_confluence_breakout.py` |
| `strategies/crypto_breakout.py` | `strategies/crypto_breakout.py` |
| `.env.example` | `.env.example` |
| `.env.live.example` | `.env.live.example` |
| `.env.live` | `.env.live` *(contains template values — replace keys)* |

---

## FOUNDATION, RISK, SWARM, AND UTILITIES

**`RBOTZILLA_FINAL_v001`** — Clean structured system (October 2025). Contains the trading charter, risk management, swarm bot, and utility modules.

GitHub: https://github.com/rfingerlin9284/RBOTZILLA_FINAL_v001

| Final File | Source Path in Repo |
|---|---|
| `foundation/rick_charter.py` | `foundation/rick_charter.py` |
| `risk/risk_control_center.py` | `risk/risk_control_center.py` |
| `risk/dynamic_sizing.py` | `risk/dynamic_sizing.py` |
| `risk/oco_validator.py` | `risk/oco_validator.py` |
| `swarm/swarm_bot.py` | `swarm/swarm_bot.py` |
| `util/mode_manager.py` | `util/mode_manager.py` |
| `util/narration_logger.py` | `util/narration_logger.py` |
| `util/logging.py` | `util/logging.py` |
| `util/timezone_manager.py` | `util/timezone_manager.py` |
| `canary_trading_engine.py` | `canary_trading_engine.py` |
| `ghost_trading_engine.py` | `ghost_trading_engine.py` |
| `capital_manager.py` | `capital_manager.py` |
| `scripts/monitor_ghost_session.py` | `scripts/monitor_ghost_session.py` |
| `scripts/oanda_paper.py` | `scripts/oanda_paper.py` |
| `scripts/start_ghost_trading.sh` | `start_ghost_trading.sh` |

---

## BACKTEST ENGINE

**`FROZEN-V2`** — Canonical research backtest engine (November 2025). Verified with CI/GitHub Actions. Bar-by-bar simulation with partial TPs, trailing stop, fees, and slippage.

GitHub: https://github.com/rfingerlin9284/FROZEN-V2

| Final File | Source Path in Repo |
|---|---|
| `backtest/` (whole directory) | `backtest/` |
| `backtest/systems/momentum_signals.py` | `systems/momentum_signals.py` |
| `backtest/wolf_packs/` | `wolf_packs/` |
| `backtest/run_pack_backtest.py` | `run_pack_backtest.py` (if present) |
| `backtest/demo_pack_backtest.py` | `demo_pack_backtest.py` (if present) |

**Backtest engine safety flags:**
- `MAX_SL_PIPS = 15` — Maximum stop loss in pips before trade is immediately closed
- `WINNER_RR_THRESHOLD = 2.5` — R:R level that moves stop loss to breakeven

---

## HIVE AGENT / AUTONOMOUS AGENT FILES

**`multi_broker_rbtz`** — Production v2.0 deployment package (January 7, 2026). Contains 128 essential production files in the deployment tarball.

GitHub: https://github.com/rfingerlin9284/multi_broker_rbtz

The deployment tarball is:
`MULTI_BROKER_PHOENIX_DEPLOYMENT_20260107_095025.tar.gz`

Key files inside the tarball (located at `MULTI_BROKER_PHOENIX/multi_broker_phoenix/`):

| Final File | Source Path Inside Tarball |
|---|---|
| `swarm/autonomous_hive_agent.py` | `multi_broker_phoenix/autonomous_hive_agent.py` |
| `swarm/engine_startup_bootstrap.py` | `multi_broker_phoenix/engine_startup_bootstrap.py` |
| `swarm/live_extreme_autonomous_integration.py` | `multi_broker_phoenix/live_extreme_autonomous_integration.py` |
| `swarm/startup_autonomous_hive.py` | `multi_broker_phoenix/startup_autonomous_hive.py` |
| `swarm/unified_hive_scanner.py` | `multi_broker_phoenix/unified_hive_scanner.py` |
| `swarm/hive_cost_control.py` | `multi_broker_phoenix/hive_cost_control.py` |
| `swarm/ai_setup_hunter.py` | `multi_broker_phoenix/ai_setup_hunter.py` |
| `swarm/strategy_quality_profiles.py` | `multi_broker_phoenix/strategy_quality_profiles.py` |

---

## BUILD AND VERIFICATION TOOLS

**`MULTIBROKER_ESSENTIALS_ONLY`** — Cleaned-up bare minimum essential files (February 1, 2026). Contains build tools, verification scripts, and deployment tooling.

GitHub: https://github.com/rfingerlin9284/MULTIBROKER_ESSENTIALS_ONLY

| Final File | Source Path in Repo |
|---|---|
| `tools/build_deployment.py` | `tools/build_deployment.py` |
| `tools/verify_configs.py` | `tools/verify_configs.py` |
| `tools/installer.py` | `tools/installer.py` |
| `tools/task_menu.py` | `tools/task_menu.py` |
| `DEPLOYMENT_STANDALONE.md` | `DEPLOYMENT_STANDALONE.md` |

---

## ADDITIONAL COINBASE AND STOCHASTIC FILES

**`R_H_UNI`** — UNIBOT with both Coinbase and OANDA (updated February 22, 2026).

GitHub: https://github.com/rfingerlin9284/R_H_UNI

| Final File | Source Path in Repo |
|---|---|
| `stochastic.py` | `stochastic.py` (fallback if not in rick_clean_live) |

---

## GOLDEN FROZEN VERSION

**`RICK_LIVE_CLEAN_FROZEN`** — Golden frozen version (November 21, 2025). Fallback source for files not found elsewhere.

GitHub: https://github.com/rfingerlin9284/RICK_LIVE_CLEAN_FROZEN

Use files from this repo as fallback only if they are not found in `rick_clean_live` or `RBOTZILLA_FINAL_v001`.

---

## WHICH REPO IS THE AUTHORITY FOR WHAT

| System Component | Primary Source | Fallback Source |
|---|---|---|
| OANDA broker connector | `rick_clean_live` | `RBOTZILLA_FINAL_v001` |
| Coinbase broker connector | `rick_clean_live` | `R_H_UNI` |
| IBKR broker connector | `rick_clean_live` | `Rbotzilla_pheonix_v1` |
| Wolf pack strategies | `rick_clean_live` (regime files) | `Rbotzilla_pheonix_v1` |
| Five main strategies | `Rbotzilla_pheonix_v1` | `rick_clean_live` |
| Trading charter (rick_charter) | `RBOTZILLA_FINAL_v001` | `FROZEN-V2` |
| Risk management | `RBOTZILLA_FINAL_v001` | `rick_clean_live` |
| Swarm / hive agent | `multi_broker_rbtz` tarball | `rick_clean_live` |
| Backtest engine | `FROZEN-V2` | none |
| Utility modules | `RBOTZILLA_FINAL_v001` | `rick_clean_live` |
| Main engine files | `RBOTZILLA_FINAL_v001` | `rick_clean_live` |
| ML stack | `rick_clean_live` | `RBOTZILLA_FINAL_v001` |
| Dashboard | `rick_clean_live` | `RBOTZILLA_FINAL_v001` |
| Build / verification tools | `MULTIBROKER_ESSENTIALS_ONLY` | `multi_broker_rbtz` |
| .env template | `Rbotzilla_pheonix_v1` | `rick_clean_live` |
| Requirements | `rick_clean_live` | `RBOTZILLA_FINAL_v001` |
| Position monitoring | `rick_clean_live` | `RBOTZILLA_FINAL_v001` |

---

## REPOS NOT USED (WHY)

| Repo | Reason Not Used |
|---|---|
| `rbotzilla_n_team` | Only contains README.md — no code |
| `rick_pheonix_gemini_v1` | Only README.md — no code |
| `MUILTIBROKER_OANDA_REPO` | Superseded by `multi_broker_rbtz` v2.0 |
| `multibroker_oanda_deployment_v1` | Earlier version of multi_broker_rbtz |
| `OANDA_CBA_UNIBOT` | First prototype — superseded by all later versions |
| `R_BOTzilla_live_prototype-` | Early prototype — superseded |
| `rick_live_prototype` | Early prototype — superseded |
| `new_RCL_rebuild` | Superseded by `rick_clean_live` |
| `RBOTZILLA_FINAL_v001` | Used for specific components (charter, risk, swarm) |

---

*Last updated: February 2026. Source repos verified active as of that date.*
