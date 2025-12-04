
export enum PlatformStatus {
  ACTIVE = 'ACTIVE',
  CANARY = 'CANARY', // Testing with small live amounts
  PAPER = 'PAPER',   // Paper trading only
  OFFLINE = 'OFFLINE',
  MAINTENANCE = 'MAINTENANCE'
}

export enum AgentMode {
  CONSTRUCTION = 'CONSTRUCTION', // Building code
  TRADING = 'TRADING', // Active trading
  ANALYSIS = 'ANALYSIS' // Analyzing market data
}

export interface PlatformConfig {
  id: string;
  name: string;
  type: 'Forex' | 'Crypto' | 'Stocks/Futures';
  status: PlatformStatus;
  uptime: string;
  pnl: number;
  activeTrades: number;
  riskLevel: 'Low' | 'Medium' | 'High';
}

export interface LawmakerRule {
  id: string;
  category: 'File System' | 'Logic' | 'Safety' | 'Autonomy';
  description: string;
  isImmutable: boolean;
  enforcementScript: string;
}

export interface Snapshot {
  id: string;
  name: string;
  timestamp: string;
  description: string;
  status: 'Stable' | 'Testing' | 'Corrupted';
  hash: string;
}

export interface LogEntry {
  id: string;
  timestamp: string;
  agent: string;
  message: string;
  approvalCode: string; // rbotzilla lawmakers=approval #xxxx
  type: 'info' | 'success' | 'warning' | 'error';
}

export interface PromptTemplate {
  id: string;
  title: string;
  description: string;
  content: string;
}

export interface TaskShortcut {
  id: string;
  label: string;
  command: string;
  description: string;
}

export interface OrganSystem {
  id: string;
  name: string;
  role: string;
  color: string;
  files: string[];
}
