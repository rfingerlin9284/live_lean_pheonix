
import { PlatformConfig, PlatformStatus, LawmakerRule, LogEntry, PromptTemplate, Snapshot, OrganSystem, TaskShortcut } from './types';

export const PLATFORMS: PlatformConfig[] = [
  {
    id: 'oanda',
    name: 'Oanda V20',
    type: 'Forex',
    status: PlatformStatus.ACTIVE,
    uptime: '99.9%',
    pnl: 0.00,
    activeTrades: 3,
    riskLevel: 'Medium'
  },
  {
    id: 'coinbase',
    name: 'Coinbase Adv.',
    type: 'Crypto',
    status: PlatformStatus.CANARY,
    uptime: '98.5%',
    pnl: 45.20,
    activeTrades: 1,
    riskLevel: 'High'
  },
  {
    id: 'ibkr',
    name: 'IBKR Gateway',
    type: 'Stocks/Futures',
    status: PlatformStatus.PAPER,
    uptime: '100%',
    pnl: 0.00,
    activeTrades: 0,
    riskLevel: 'Low'
  }
];

export const LAWMAKER_RULES: LawmakerRule[] = [
  {
    id: 'rule-1',
    category: 'File System',
    description: 'NEVER rename existing files or folders. Append to existing logic modules only.',
    isImmutable: true,
    enforcementScript: 'agent_charter.py'
  },
  {
    id: 'rule-2',
    category: 'Safety',
    description: 'All live trades require "Rick Hive" consensus > 85% confidence.',
    isImmutable: true,
    enforcementScript: 'hive_consensus_gate.py'
  },
  {
    id: 'rule-3',
    category: 'Autonomy',
    description: 'Each platform must operate independently via "trading_sectors.yaml" config.',
    isImmutable: true,
    enforcementScript: 'sector_loader.py'
  },
  {
    id: 'rule-4',
    category: 'Logic',
    description: 'Raptor Agent must sign all changes with "rbotzilla lawmakers=approval #xxxx".',
    isImmutable: true,
    enforcementScript: 'signature_validator.py'
  }
];

export const SNAPSHOTS: Snapshot[] = [
  {
    id: 'snap-005',
    name: 'Phase 2 Orchestration Complete',
    timestamp: '2025-12-03 18:45:00',
    description: 'Independent Sectors (Oanda/Coinbase/IBKR) established. Agent Charter wired to all engines. Snapshots active.',
    status: 'Stable',
    hash: 'c4d5e6f7'
  },
  {
    id: 'snap-004',
    name: 'Balanced Profile Activation',
    timestamp: '2023-10-28 08:00:00',
    description: 'Applied Min PnL $35, Min Notional $10k, Margin Cap 175%. Verified OCO placement.',
    status: 'Stable',
    hash: 'b2c3d4e5'
  },
  {
    id: 'snap-003',
    name: 'Phase 1 Complete: Oanda Stable',
    timestamp: '2023-10-27 10:00:00',
    description: 'Full Oanda integration with ML logic and strict stop-loss. Verified stable.',
    status: 'Stable',
    hash: 'a1b2c3d4'
  }
];

export const RECENT_LOGS: LogEntry[] = [
  {
    id: 'log-unchained',
    timestamp: '2025-12-03 19:15:00',
    agent: 'System',
    message: 'User authorizes Practice Trading. Safety Gates Bypassed via Environment Variables. PROTOCOL UNCHAINED.',
    approvalCode: 'USER_OVERRIDE',
    type: 'warning'
  },
  {
    id: 'log-telemetry',
    timestamp: '2025-12-03 19:10:00',
    agent: 'System',
    message: 'Telemetry Pipeline Online. OANDA Feed: ACTIVE. Balance Stream: ACTIVE.',
    approvalCode: 'DATA_STREAM_OK',
    type: 'success'
  },
  {
    id: 'log-success-connect',
    timestamp: '2025-12-03 18:55:00',
    agent: 'System',
    message: 'OANDA Connection Verified. Practice Mode Verified. Balance: $9,988.93. "Safety Stubs" bypassed.',
    approvalCode: 'AUTH_VERIFIED',
    type: 'success'
  },
  {
    id: 'log-heartbeat',
    timestamp: '2025-12-03 18:47:30',
    agent: 'System',
    message: 'OANDA Engine > Detected file system changes (Phase 3 Build)... Ignoring... Strategy Execution Unaffected. [EUR/USD Long Held]',
    approvalCode: 'INDEPENDENCE_CHECK',
    type: 'success'
  },
  {
    id: 'log-simplify',
    timestamp: '2025-12-03 22:00:00',
    agent: 'System',
    message: 'SIMPLIFY MODE enabled: permission checks and lock scripts disabled for developer convenience (opt-in).',
    approvalCode: 'SIMPLIFY_MODE',
    type: 'info'
  },
  {
    id: 'log-0',
    timestamp: '2025-12-03 18:46:12',
    agent: 'Raptor',
    message: 'Phase 2 Complete. All sectors independent. Snapshots active. Awaiting Phase 3 directives.',
    approvalCode: 'AC002_COMPLETE',
    type: 'success'
  }
];

export const PROMPT_TEMPLATES: PromptTemplate[] = [
  {
    id: 'mega-final-evolution',
    title: 'Supreme Commander: FINAL EVOLUTION (Phases 3 & 4)',
    description: 'Executes ALL remaining tasks: Real Connectors (Coinbase/IBKR) + Production Hardening (Docker/Systemd). ONE SHOT.',
    content: `ACT AS: Raptor (Supreme Commander)
PIN: 841921
APPROVAL TAG: "confident with rbotzilla lawmakers=approval"

OBJECTIVE: 
COMPLETE THE SYSTEM. Execute Phase 3 AND Phase 4 immediately.
We are done with step-by-step. Finish the job.

PHASE 3: REALITY BRIDGE (Real Connectors)
1. CREATE/UPDATE "brokers/coinbase_advanced_connector.py":
   - Must use \`coinbase-advanced-py\`.
   - Implement \`get_balance()\` and \`place_order()\` hitting real API endpoints.
   - Retain Canary logic (only log if mode='canary').
2. CREATE/UPDATE "brokers/ibkr_connector.py":
   - Must use \`ib_insync\`.
   - Implement connection to TWS/Gateway (127.0.0.1:7497/4001).
   - Implement \`place_oco_order()\`.
3. UPDATE "requirements.txt":
   - Add: \`coinbase-advanced-py\`, \`ib_insync\`.

PHASE 4: FORTRESS RICK (Production Hardening)
1. CONTAINERIZATION:
   - Create "Dockerfile" (python:3.9-slim, copy ops, install reqs).
   - Create "docker-compose.yml" (Services: oanda_engine, coinbase_engine, ibkr_engine; Restart: always).
2. SYSTEMD SERVICE:
   - Create "ops/rick_phoenix.service" (ExecStart=/usr/bin/bash /app/start_with_integrity.sh).
3. SECURITY:
   - Create "ops/lock_secrets.sh" (chmod 600 .env).
   - Run it immediately.

EXECUTION RULE:
- DO NOT STOP between phases.
- DO NOT disrupt the running OANDA Engine (Protocol Unchained).
- Log all actions in "construction_logs/final_evolution.md".

FINAL OUTPUT:
"SYSTEM EVOLUTION COMPLETE. Connectors Active. Docker Ready. Service Installed."`
  },
  {
    id: 'mega-unchained',
    title: 'Supreme Commander: PROTOCOL UNCHAINED (Force Start)',
    description: 'Bypasses all safety gates. Sets required environment variables and forces the engine to run IMMEDIATELY.',
    content: `ACT AS: Raptor (Supreme Commander)
PIN: 841921
APPROVAL TAG: "confident with rbotzilla lawmakers=approval"

OBJECTIVE: 
IMMEDIATE EXECUTION of OANDA Practice Engine.
Stop asking questions. The user consents to PRACTICE TRADING.

ACTION PLAN:
1. SET Environment Variables for this session:
   - RICK_ENV=practice
   - ALLOW_PRACTICE_ORDERS=1
   - CONFIRM_PRACTICE_ORDER=1
   - PRACTICE_PIN=841921
   - OANDA_FORCE_ENV=practice
   - OANDA_LOAD_ENV_FILE=1

2. EXECUTE the Engine:
   Run the following command in the terminal IMMEDIATELY:
   \`RICK_ENV=practice ALLOW_PRACTICE_ORDERS=1 CONFIRM_PRACTICE_ORDER=1 python3 oanda/oanda_trading_engine.py\`

3. CONFIRMATION:
   Output "ENGINE STARTED. MONITORING NARRATION LOGS."

DO NOT ask for parameters. DO NOT ask for UI modals. JUST RUN THE SCRIPT.`
  },
  {
    id: 'mega-phase-4',
    title: 'Supreme Commander: Phase 4 (Fortress Rick)',
    description: 'Production Hardening. Systemd services, Docker containerization, and Secrets lockdown. NO Gold Plating.',
    content: `ACT AS: Raptor (Supreme Commander)
PIN: 841921
APPROVAL TAG: "confident with rbotzilla lawmakers=approval"

REGARDING YOUR LAST QUESTION:
"Do you want me to: Add the telemetry emitter... or Add a production ops/install_service.sh...?"
>>> ANSWER: NEGATIVE. Do not implement telemetry or dashboard add-ons yet. Focus strictly on hardening (Dockerfile, docker-compose.yml, ops/ systemd service, and secrets lockdown).

OBJECTIVE: 
Execute "Phase 4: Fortress Rick". 
The system is functional (Phase 3). Now we MUST harden it for 24/7 autonomous operation.

PHASE A: CONTAINERIZATION (The Armor)
1. Create "Dockerfile".
   - Base: python:3.9-slim
   - Install: git, build-essential
   - Copy: requirements.txt -> pip install
   - Copy: . -> /app
   - Ensure "ops/" scripts are executable.
2. Create "docker-compose.yml".
   - Services: 
     - oanda_engine (env: practice)
     - coinbase_engine (env: canary)
     - ibkr_engine (env: paper)
   - Restart: always

PHASE B: SYSTEMD (The Immortal Pulse)
1. Create "ops/rick_phoenix.service".
   - Type: simple
   - ExecStart: /usr/bin/bash /app/start_with_integrity.sh
   - Restart: on-failure
   - User: ubuntu (or current user)

PHASE C: SECRETS VAULT (The Lock)
1. Check ".env" permissions.
2. If world-readable, create script "ops/lock_secrets.sh" to chmod 600 .env.
3. Update "AgentCharter" to warn if .env is insecure.

PHASE D: FUTURE LOG (The Parking Lot)
1. Create "construction_logs/future_addons.md".
2. Note any skipped ideas (like Telemetry Emitter or Dashboard Forwarder) here for later.

EXECUTION RULE:
- Do not disrupt the running engines.
- Create "ops/" directory if missing.
- Log progress in "construction_logs/orchestration.md".

FINAL OUTPUT:
"Phase 4 Complete. System Dockerized and Service-Ready." followed by the Approval Tag.`
  },
  {
    id: 'mega-oanda-force',
    title: 'Supreme Commander: FORCE OANDA CONNECTION (Fix)',
    description: 'Overrides simulation safety stubs. Forces the agent to bind .env credentials and execute REAL trades on the Practice API.',
    content: `ACT AS: Raptor (Supreme Commander)
PIN: 841921
APPROVAL TAG: "confident with rbotzilla lawmakers=approval"

OBJECTIVE: 
FORCE OANDA CONNECTION. STOP MOCKING. USE THE REAL .ENV FILE.
The user is reporting that the system is "simulating" instead of trading.
We must bind the real credentials immediately.

PHASE A: INSPECT CREDENTIALS
1. READ the \`.env\` file.
2. IDENTIFY the variable names. Look for:
   - \`OANDA_API_KEY\` or \`OANDA_PRACTICE_TOKEN\`
   - \`OANDA_ACCOUNT_ID\` or \`OANDA_PRACTICE_ACCOUNT_ID\`
3. CONFIRM these values exist.

PHASE B: UPDATE CONNECTOR (The Fix)
1. EDIT "oanda/brokers/oanda_connector.py".
2. LOCATE the \`__init__\` method.
3. DELETE any logic that defaults to \`simulation = True\` when in practice mode.
4. FORCE the connector to use the keys found in Phase A.
   - Example: \`self.token = os.getenv('OANDA_PRACTICE_TOKEN')\`
   - Example: \`self.account_id = os.getenv('OANDA_PRACTICE_ACCOUNT_ID')\`
5. ENSURE it hits the Practice API URL: \`https://api-fxpractice.oanda.com/v3\`

PHASE C: VERIFY CONNECTION
1. CREATE "tools/verify_oanda_live.py".
2. Script must:
   - Import \`oanda_connector\`.
   - Initialize connection.
   - Call \`get_account_summary()\`.
   - PRINT the actual Account Balance and NAV from the API.
3. RUN this script and show the output.

FINAL OUTPUT:
"OANDA LIVE CONNECTION FORCED. Real Balance: [Insert Balance Here]" followed by the Approval Tag.`
  },
  {
    id: 'mega-phase-3',
    title: 'Supreme Commander: Phase 3 (The Reality Bridge)',
    description: 'Answers Raptor\'s push question and commands the build of REAL connectors for Coinbase and IBKR.',
    content: `ACT AS: Raptor (Supreme Commander)
PIN: 841921
APPROVAL TAG: "confident with rbotzilla lawmakers=approval"

REGARDING YOUR LAST QUESTION:
"Do you want me to push these changes to the gemini repo remote?"
>>> ANSWER: NEGATIVE. Do not push to remote yet. We keep operations local/internal for now. Proceed immediately to Phase 3.

OBJECTIVE: 
Execute "Phase 3: The Reality Bridge". 
We currently have "Stub" (fake) connectors for Coinbase and IBKR. Now we build the REAL ones.

PHASE A: COINBASE CONNECTOR (The Awakening)
1. Create/Update "brokers/coinbase_advanced_connector.py".
   - Use library: \`coinbase-advanced-py\` (REST API).
   - Implement Class: \`CoinbaseConnector\`.
   - Implement Method: \`get_balance()\` -> returns available USD/USDC.
   - Implement Method: \`place_order(product_id, side, size, limit_price, stop_price)\`.
   - IMPORTANT: If mode is 'canary', \`place_order\` must Log only. If 'live', it executes.

PHASE B: IBKR CONNECTOR (The Bridge)
1. Create/Update "brokers/ibkr_connector.py".
   - Use library: \`ib_insync\`.
   - Implement Class: \`IBKRConnector\`.
   - Connection Params: Host=127.0.0.1, Port=4001 (Gateway) or 7497 (TWS).
   - Implement: \`place_oco_order(...)\`.

PHASE C: DEPENDENCY CHECK
1. Update "requirements.txt" to include:
   - \`coinbase-advanced-py\`
   - \`ib_insync\`
2. Instruct me to run: \`pip install -r requirements.txt\`.

EXECUTION RULE:
- Do not break the "Oanda" sector. It must remain online.
- Do not rename existing files.
- Log progress in "construction_logs/orchestration.md".

FINAL OUTPUT:
"Phase 3 Complete. Real connectors built. Dependencies updated." followed by the Approval Tag.`
  },
  {
    id: 'mega-orchestrator',
    title: 'Supreme Commander: Phase 2 Orchestration',
    description: 'The "Single Prompt" to rule them all. Delegates charter enforcement, snapshots, and multi-sector buildout.',
    content: `ACT AS: Raptor (Supreme Commander & Lead Architect)
PIN: 841921
APPROVAL TAG: "confident with rbotzilla lawmakers=approval"

OBJECTIVE: 
Execute "Phase 2" of the Rick Phoenix evolution. You are the Orchestrator. 
Do not stop until all 4 Phases below are complete. Use "construction_logs/orchestration.md" to track your own progress.

PHASE A: LAW & ORDER (The Foundation)
1. Create "foundation/agent_charter.py".
   - Define "AgentCharter" class.
   - Enforce: NO_RENAMES = True.
   - Enforce: REQUIRE_SNAPSHOT = True.
   - Enforce: PIN = 841921.
2. Wire "AgentCharter.enforce()" into "oanda/oanda_trading_engine.py" startup.
3. Create "utils/snapshot_manager.py" (Git wrapper).
4. Add "Create Snapshot" to "tasks.json".

PHASE B: SECTOR CONFIGURATION
1. Create "config/trading_sectors.yaml".
   - Define: oanda (active/paper), coinbase (canary), ibkr (paper).
2. Create "util/sector_loader.py" to read this config.

PHASE C: COINBASE (Canary Mode)
1. CLONE "oanda_trading_engine.py" to "coinbase/coinbase_trading_engine.py".
2. MODIFY for Crypto:
   - Use "canary_settings.yaml" logic.
   - If mode == "canary": DO NOT TRADE. Log "CANARY_SIGNAL" events only.
   - KEEP "Balanced Profile" logic ($35 PnL).

PHASE D: IBKR (Paper Mode)
1. CLONE "oanda_trading_engine.py" to "ibkr/ibkr_trading_engine.py".
2. Stub out connection for IBKR Gateway.

EXECUTION RULE:
- If you have access to a Cloud Agent or Sub-Agents, DELEGATE Phase C and D to them while you verify Phase A.
- If running solo, execute sequentially A -> B -> C -> D.
- Update "tasks.json" with new run commands for each sector.

FINAL OUTPUT:
"Phase 2 Complete. All sectors independent. Snapshots active." followed by the Approval Tag.`
  }
];

  // Added prompt template: SIMPLIFY (developer convenience)
  PROMPT_TEMPLATES.push({
    id: 'mega-simplify',
    title: 'Supreme Commander: SIMPLIFY (Developer Convenience)',
    description: 'Temporarily disable env permission enforcement, lock scripts, and admin checks for development convenience.',
    content: `ACT AS: Raptor (System Simplifier)
  PIN: 841921

  OBJECTIVE:
  Enable simplified operation mode that disables permission checks and lock scripts. This is for testing/dev only. Activate by setting SIMPLIFY_MODE=1 in your shell or tasks.
  1. Skip running ops/lock_secrets.sh and ops/check_env_permissions.py at startup.
  2. Do not enforce .env permissions in AgentCharter.enforce().
  3. Write environment without applying chmod 600 by default.
  4. NOTE: This is an opt-in dev mode — do NOT use it in production or with live keys.
  `
  });

export const ORGAN_SYSTEMS: OrganSystem[] = [
  {
    id: 'brain',
    name: 'THE BRAIN',
    role: 'Logic, Law & Risk Management',
    color: 'text-purple-400',
    files: [
      'foundation/rick_charter.py',
      'foundation/agent_charter.py',
      'rick_hive/guardian_gates.py',
      'oanda/foundation/rick_charter.py',
      'config/trading_sectors.yaml'
    ]
  },
  {
    id: 'nervous',
    name: 'NERVOUS SYSTEM',
    role: 'Communication & Narration',
    color: 'text-blue-400',
    files: [
      'util/narration_logger.py',
      'bridges/oanda_charter_bridge.py',
      'bridges/oanda_live_bridge.py',
      'util/sector_loader.py'
    ]
  },
  {
    id: 'limbs',
    name: 'LIMBS',
    role: 'Execution & Trading Engines',
    color: 'text-green-400',
    files: [
      'oanda/oanda_trading_engine.py',
      'coinbase/coinbase_trading_engine.py',
      'ibkr/ibkr_trading_engine.py',
      'oanda/brokers/oanda_connector.py',
      'brokers/coinbase_advanced_connector.py',
      'brokers/ibkr_connector.py'
    ]
  },
  {
    id: 'senses',
    name: 'SENSES',
    role: 'Monitoring & Diagnostics',
    color: 'text-orange-400',
    files: [
      'tools/check_narration_counts.py',
      'tools/watchdog.py',
      'tests/test_charter_gates.py',
      'util/snapshot_manager.py'
    ]
  }
];

export const VSCODE_TASKS: TaskShortcut[] = [
  {
    id: 'task-0',
    label: 'Create System Snapshot',
    command: 'python utils/snapshot_manager.py --create',
    description: 'Freezes current state. Use before allowing agents to modify code.'
  },
  {
    id: 'task-1',
    label: 'Check Narration (tools)',
    command: 'python tools/check_narration_counts.py',
    description: 'Runs helper to count recent signals, OCOs, and violations.'
  },
  {
    id: 'task-2',
    label: 'Run Charter Gate Tests',
    command: 'pytest -q tests/test_charter_gates.py',
    description: 'Verifies that $35 PnL and $10k Notional gates are working.'
  },
  {
    id: 'task-3',
    label: 'Run OANDA Engine (Practice)',
    command: 'python oanda/oanda_trading_engine.py',
    description: 'Starts the trading engine in Practice Mode (Background).'
  },
  {
    id: 'task-4',
    label: 'Run Coinbase Sector (Canary)',
    command: 'python coinbase/coinbase_trading_engine.py --mode=canary',
    description: 'Starts Coinbase in Canary Mode (Logging only, no live trades).'
  },
  {
    id: 'task-5',
    label: 'SIMPLIFY MODE (No Permission Hardening)',
    command: 'export SIMPLIFY_MODE=1 && echo "SIMPLIFY_MODE set; start basic tasks"',
    description: 'Enable simplified mode (no .env permission hardening, no lock scripts) for development/convenience.'
  }
];

export const INTEGRITY_FILES = [
    "oanda/oanda_trading_engine.py",
    "oanda/foundation/rick_charter.py",
    "foundation/rick_charter.py",
    "foundation/agent_charter.py",
    "rick_institutional_full.py",
    "rick_hive/guardian_gates.py",
    "util/narration_logger.py",
    "util/rick_narrator.py",
    "util/position_police.py",
    "pretty_print_narration.py",
    "bridges/oanda_live_bridge.py",
    "bridges/oanda_charter_bridge.py",
    "brokers/coinbase_advanced_connector.py",
    "brokers/ibkr_connector.py",
    "oanda/brokers/oanda_connector.py",
    "start_with_integrity.sh",
    "start_tmux_dashboard.sh",
    "auto_diagnostic_monitor.py",
    "active_trade_monitor.py",
    "system_watchdog.py",
    "config/gates.yaml",
    "config/trading_sectors.yaml",
    "config/aggressive_machine_config.py",
    "tools/check_narration_counts.py",
    "tools/export_for_gemini.sh",
    "tools/megascript_rebuild.sh",
    "tools/validate_and_snapshot.sh",
    ".env.example",
    "config/canary_settings.yaml",
    ".vscode/tasks.json",
    ".vscode/cheatsheet.md",
    "tests/test_charter_gates.py",
    "utils/snapshot_manager.py",
    "Dockerfile",
    "docker-compose.yml",
    "requirements.txt",
    "manifest.txt",
    "manifest.json",
    "README_GEMINI_EXPORT.md"
];
