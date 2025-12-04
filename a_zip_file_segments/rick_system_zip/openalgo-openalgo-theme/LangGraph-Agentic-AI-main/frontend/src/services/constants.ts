// Shared constants for the frontend dashboard
export const OANDA_HEARTBEAT_MESSAGE = "OANDA Engine > Detected file system changes... Ignoring... Strategy Execution Unaffected.";
export const PLATFORM_HEARTBEAT_EVENT = 'MACHINE_HEARTBEAT';

export const PLATFORM_NAMES = {
  OANDA: 'oanda',
  COINBASE: 'coinbase',
  IBKR: 'ibkr',
};

// (Default export moved to the end of the file where PROMPT_TEMPLATES is included)

/*
  Phase 4 Mega Prompt (Fortress Rick)
  Directive: NEGATIVE on telemetry/dashboard moves. Focus on hardening tasks only (Docker, Systemd, Secrets).
*/
export const PROMPT_TEMPLATES = [
  {
    id: 'mega-phase-4',
    title: 'Supreme Commander: Phase 4 (Fortress Rick)',
    description: 'Production Hardening. Systemd services, Docker containerization, and Secrets lockdown. No telemetry/dashboard feature changes in Phase 4.',
    content: `OBJECTIVE: Phase 4 - Fortress Rick. Focus only on production hardening tasks: Dockerization, systemd auto-start, and Secrets lockdown. Telemetry/emitter/dashboard changes are out-of-scope and must not be implemented as part of this phase.`
  }
];

export default {
  OANDA_HEARTBEAT_MESSAGE,
  PLATFORM_HEARTBEAT_EVENT,
  PLATFORM_NAMES,
  PROMPT_TEMPLATES
};
