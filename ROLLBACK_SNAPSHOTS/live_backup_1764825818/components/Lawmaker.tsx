
import React from 'react';
import { LAWMAKER_RULES, SNAPSHOTS } from '../constants';
import { Lock, ShieldCheck, AlertTriangle, History, Save, RotateCcw, Scale, FileCode, CheckCircle2, Siren } from 'lucide-react';

const Lawmaker: React.FC = () => {
  return (
    <div className="space-y-8">
      {/* Header Section */}
      <div className="flex justify-between items-end border-b border-gray-800 pb-6">
        <div>
          <h2 className="text-2xl font-bold text-white mb-2">Lawmaker Charter & State Control</h2>
          <p className="text-gray-400 text-sm max-w-2xl">
            Manage immutable system constraints and control system state. 
            Use Snapshots to "save game" before allowing agents to modify core logic.
          </p>
        </div>
        <div className="flex items-center gap-2 bg-rick-card px-4 py-2 rounded-full border border-rick-accent/30">
          <ShieldCheck size={16} className="text-rick-accent" />
          <span className="text-xs font-mono text-rick-accent font-bold">ENFORCEMENT ACTIVE</span>
        </div>
      </div>

      {/* Constitutional Constants (New) */}
      <div className="bg-rick-card border border-gray-800 rounded-xl overflow-hidden">
        <div className="p-4 border-b border-gray-800 bg-rick-dark/50 flex items-center justify-between">
           <h3 className="text-sm font-bold text-white flex items-center gap-2">
             <Scale className="text-purple-400" size={16} />
             Constitutional Constants (Balanced Profile)
           </h3>
           <span className="text-[10px] text-green-500 font-mono flex items-center gap-1">
             <CheckCircle2 size={10} /> SYNCED
           </span>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 divide-x divide-gray-800 border-b border-gray-800">
           <div className="p-4 text-center">
             <div className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Min Expected PnL</div>
             <div className="text-xl font-bold text-white font-mono">$35.00</div>
           </div>
           <div className="p-4 text-center">
             <div className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Min Notional</div>
             <div className="text-xl font-bold text-white font-mono">$10,000</div>
           </div>
           <div className="p-4 text-center">
             <div className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Max Margin Cap</div>
             <div className="text-xl font-bold text-rick-accent font-mono">175%</div>
           </div>
           <div className="p-4 text-center">
             <div className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Max Positions</div>
             <div className="text-xl font-bold text-white font-mono">3</div>
           </div>
        </div>
        <div className="p-3 bg-black/40 text-[10px] text-gray-500 font-mono text-center">
           Source Truth: <span className="text-gray-300">foundation/rick_charter.py</span> && <span className="text-gray-300">oanda/foundation/rick_charter.py</span>
        </div>
      </div>

      {/* Snapshots Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
           <h3 className="text-lg font-bold text-white flex items-center gap-2">
             <History className="text-blue-400" size={20} />
             System Restore Points
           </h3>
           <div className="flex gap-2">
              <span className="text-[10px] bg-red-900/30 text-red-400 px-3 py-1 rounded flex items-center gap-1 border border-red-900/50">
                <Siren size={12} />
                AGENT MANDATE: SNAPSHOT REQUIRED BEFORE CODE CHANGES
              </span>
              <button className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded text-xs font-bold transition-colors">
                <Save size={14} />
                CREATE NEW SNAPSHOT
              </button>
           </div>
        </div>
        
        <div className="grid gap-3">
          {SNAPSHOTS.map((snap) => (
            <div key={snap.id} className="bg-rick-card border border-gray-800 p-4 rounded-lg flex items-center justify-between group hover:border-gray-600 transition-colors">
              <div className="flex items-start gap-4">
                <div className={`w-2 h-2 mt-2 rounded-full ${snap.status === 'Stable' ? 'bg-green-500' : 'bg-yellow-500'}`} />
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-sm font-bold text-white">{snap.name}</span>
                    <span className="text-[10px] bg-gray-800 text-gray-400 px-1.5 py-0.5 rounded font-mono">{snap.hash}</span>
                  </div>
                  <div className="text-xs text-gray-500 mt-1">{snap.timestamp}</div>
                  <p className="text-xs text-gray-400 mt-1 max-w-xl">{snap.description}</p>
                </div>
              </div>
              
              <button className="opacity-0 group-hover:opacity-100 flex items-center gap-2 bg-gray-800 hover:bg-red-900/50 hover:text-red-400 text-gray-300 px-3 py-1.5 rounded text-xs font-bold transition-all border border-transparent hover:border-red-500/30">
                <RotateCcw size={14} />
                ROLLBACK
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Rules Section */}
      <div className="space-y-4 pt-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
             <Lock className="text-rick-warn" size={20} />
             Active Constraints
        </h3>
        <div className="grid gap-4">
          {LAWMAKER_RULES.map((rule) => (
            <div key={rule.id} className="bg-rick-card border border-gray-800 p-6 rounded-xl hover:border-gray-700 transition-colors relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                 <Lock size={64} />
              </div>
              
              <div className="flex items-start justify-between relative z-10">
                <div className="space-y-3">
                  <div className="flex items-center gap-3">
                    <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider ${
                      rule.category === 'Safety' ? 'bg-red-900/30 text-red-400' :
                      rule.category === 'File System' ? 'bg-blue-900/30 text-blue-400' :
                      'bg-yellow-900/30 text-yellow-400'
                    }`}>
                      {rule.category}
                    </span>
                    {rule.isImmutable && (
                      <span className="flex items-center gap-1 text-[10px] text-gray-500 uppercase">
                        <Lock size={10} /> Immutable
                      </span>
                    )}
                  </div>
                  <h3 className="text-lg font-semibold text-white">{rule.description}</h3>
                  <div className="flex items-center gap-2 text-xs font-mono text-gray-500 bg-black/30 w-fit px-3 py-1.5 rounded">
                    <span className="text-purple-400">$</span>
                    {rule.enforcementScript}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Lawmaker;
