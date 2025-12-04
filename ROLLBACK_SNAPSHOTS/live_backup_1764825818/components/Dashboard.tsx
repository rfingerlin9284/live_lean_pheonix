
import React, { useState, useEffect } from 'react';
import { PLATFORMS, RECENT_LOGS, INTEGRITY_FILES } from '../constants';
import { Activity, Zap, Globe, Cpu, Watch, Shield, Terminal, CheckCircle2, FileCode, TrendingUp, TrendingDown, Wifi, ClipboardCopy } from 'lucide-react';
import PlatformStatusGrid from './dashboard/PlatformStatusGrid';

const Dashboard: React.FC = () => {
  // Simulate Live Market Data for OANDA
  const [eurUsdPrice, setEurUsdPrice] = useState(1.0845);
  const [priceDirection, setPriceDirection] = useState<'up' | 'down'>('up');
  const [floatingPnL, setFloatingPnL] = useState(0.00);
  const [copySuccess, setCopySuccess] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      // Random walk for price simulation
      const move = (Math.random() - 0.5) * 0.0005;
      setEurUsdPrice(prev => {
        const newPrice = prev + move;
        setPriceDirection(newPrice > prev ? 'up' : 'down');
        return newPrice;
      });
      
      // Random walk for PnL simulation based on "Open Positions"
      setFloatingPnL(prev => prev + (move * 10000)); // 1 lot equivalent
    }, 1500);

    return () => clearInterval(interval);
  }, []);

  const quickStartCommand = `export RICK_ENV=practice
export ALLOW_PRACTICE_ORDERS=1
export CONFIRM_PRACTICE_ORDER=1
export PRACTICE_PIN=841921
export OANDA_FORCE_ENV=practice
export OANDA_LOAD_ENV_FILE=1
python3 oanda/oanda_trading_engine.py`;

  const handleCopyCommand = () => {
    navigator.clipboard.writeText(quickStartCommand);
    setCopySuccess(true);
    setTimeout(() => setCopySuccess(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Header Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-rick-card p-4 rounded-xl border border-gray-800 relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-2 opacity-5 group-hover:opacity-10 transition-opacity">
            <Cpu size={48} />
          </div>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-blue-500/10 rounded-lg">
              <Cpu className="text-blue-500" size={20} />
            </div>
            <span className="text-sm text-gray-400">Rick Hive Status</span>
          </div>
          <div className="text-2xl font-bold text-white">ONLINE</div>
          <div className="text-xs text-blue-500 mt-1">Listening to 3 markets</div>
        </div>

        <div className="bg-rick-card p-4 rounded-xl border border-gray-800 relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-2 opacity-5 group-hover:opacity-10 transition-opacity">
            <Shield size={48} />
          </div>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-green-500/10 rounded-lg">
              <Shield className="text-green-500" size={20} />
            </div>
            <span className="text-sm text-gray-400">Active Profile</span>
          </div>
          <div className="text-xl font-bold text-white">BALANCED</div>
          <div className="text-xs text-green-500 mt-1">PnL $35 | 175% Cap</div>
        </div>

        <div className="bg-rick-card p-4 rounded-xl border border-gray-800 relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-2 opacity-5 group-hover:opacity-10 transition-opacity">
            <Globe size={48} />
          </div>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-purple-500/10 rounded-lg">
              <Globe className="text-purple-500" size={20} />
            </div>
            <span className="text-sm text-gray-400">Global Latency</span>
          </div>
          <div className="text-2xl font-bold text-white">12ms</div>
          <div className="text-xs text-gray-500 mt-1">Oanda/IBKR Sync</div>
        </div>

        <div className="bg-rick-card p-4 rounded-xl border border-gray-800 relative overflow-hidden group">
           <div className="absolute top-0 right-0 p-2 opacity-5 group-hover:opacity-10 transition-opacity">
            <Watch size={48} />
          </div>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-orange-500/10 rounded-lg">
              <Watch className="text-orange-500" size={20} />
            </div>
            <span className="text-sm text-gray-400">Watchdog Service</span>
          </div>
          <div className="text-xl font-bold text-white">AWAITING FINAL EVOLUTION</div>
          <div className="text-xs text-orange-500 mt-1 animate-pulse">Running Final Batch Job</div>
        </div>
      </div>

      {/* Main Content Split */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Live Neural Feed (Narration) */}
        <div className="lg:col-span-2 space-y-6">
            
            {/* Quick Start Command Box */}
            <div className="bg-gradient-to-r from-red-900/20 to-black border border-red-500/30 rounded-xl p-4 flex flex-col gap-2">
                <div className="flex justify-between items-center">
                    <h3 className="text-red-400 font-bold text-sm uppercase flex items-center gap-2">
                        <Zap size={14} /> Quick Start: Force OANDA Practice
                    </h3>
                    {copySuccess && <span className="text-green-500 text-xs font-bold animate-pulse">COPIED!</span>}
                </div>
                <div className="bg-black/50 p-3 rounded text-xs font-mono text-gray-300 border border-red-900/30 relative">
                    <pre>{quickStartCommand}</pre>
                    <button 
                        onClick={handleCopyCommand}
                        className="absolute top-2 right-2 p-1.5 bg-red-900/50 hover:bg-red-800 text-white rounded transition-colors"
                        title="Copy Command"
                    >
                        <ClipboardCopy size={14} />
                    </button>
                </div>
            </div>

            <div className="bg-rick-card rounded-xl border border-gray-800 flex flex-col overflow-hidden h-[400px]">
                <div className="p-4 border-b border-gray-800 bg-rick-dark flex items-center justify-between">
                    <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-rick-accent animate-pulse" />
                    <h3 className="text-sm font-bold text-white font-mono uppercase tracking-wider">Live Neural Feed</h3>
                    </div>
                    <div className="text-[10px] text-gray-500 font-mono">STREAM: ACTIVE</div>
                </div>
                
                <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-black/50 font-mono scrollbar-hide">
                    {RECENT_LOGS.map((log) => (
                    <div key={log.id} className="flex gap-3 group animate-in slide-in-from-left-2 duration-300">
                        <div className="text-xs text-gray-600 w-24 shrink-0 pt-1">{log.timestamp.split(' ')[1]}</div>
                        <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                            <span className={`text-xs font-bold ${
                                log.agent === 'Raptor' ? 'text-rick-accent' : 
                                log.agent === 'System' ? 'text-blue-400' : 
                                log.type === 'error' ? 'text-red-500' : 'text-gray-400'
                            }`}>
                                {log.agent} &gt;
                            </span>
                            {log.type === 'success' && <span className="text-[10px] text-green-500 border border-green-900 bg-green-900/20 px-1 rounded">PASS</span>}
                            {log.type === 'warning' && <span className="text-[10px] text-yellow-500 border border-yellow-900 bg-yellow-900/20 px-1 rounded">ALERT</span>}
                            {log.type === 'error' && <span className="text-[10px] text-red-500 border border-red-900 bg-red-900/20 px-1 rounded">CRITICAL</span>}
                        </div>
                        <p className="text-sm text-gray-300 leading-relaxed border-l-2 border-gray-800 pl-3 group-hover:border-rick-accent/50 transition-colors">
                            {log.message}
                        </p>
                        </div>
                    </div>
                    ))}
                </div>
                
                <div className="p-2 bg-rick-dark border-t border-gray-800 text-[10px] text-gray-500 flex justify-center items-center gap-2">
                    <Terminal size={10} />
                    <span>Awaiting next input...</span>
                </div>
            </div>

            {/* System Integrity Monitor */}
            <div className="bg-rick-card rounded-xl border border-gray-800 p-4">
                <div className="flex items-center justify-between mb-4">
                     <h3 className="text-sm font-bold text-white flex items-center gap-2">
                        <FileCode size={16} className="text-purple-400" />
                        System Integrity Monitor
                     </h3>
                     <span className="text-[10px] text-gray-500">{INTEGRITY_FILES.length} Modules Active</span>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-2 h-40 overflow-y-auto pr-2 scrollbar-hide">
                    {INTEGRITY_FILES.map((file, idx) => (
                        <div key={idx} className="bg-black/40 border border-gray-800 rounded p-2 flex items-center gap-2 group hover:border-gray-600 transition-colors">
                            <CheckCircle2 size={12} className="text-green-500 shrink-0" />
                            <span className="text-[10px] font-mono text-gray-400 truncate group-hover:text-gray-200" title={file}>
                                {file.split('/').pop()}
                            </span>
                        </div>
                    ))}
                </div>
            </div>
        </div>

        {/* Platform List */}
        <div className="space-y-4">
          <h3 className="text-lg font-bold text-white">Platform Control</h3>
          {PLATFORMS.map((platform) => (
            <div key={platform.id} className="bg-rick-dark p-4 rounded-lg border border-gray-800 hover:border-rick-accent/50 transition-colors relative overflow-hidden">
               {/* Heartbeat Pulse for Active Platforms */}
               {platform.status === 'ACTIVE' && (
                  <div className="absolute top-3 right-3 flex h-3 w-3">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
                  </div>
               )}

              <div className="flex justify-between items-start mb-3">
                <div>
                  <h4 className="font-bold text-white">{platform.name}</h4>
                  <p className="text-xs text-gray-500">{platform.type}</p>
                </div>
                <div className={`px-2 py-1 rounded text-[10px] font-bold uppercase ${
                  platform.id === 'oanda' ? 'bg-red-500/20 text-red-500 animate-pulse' :
                  platform.status === 'ACTIVE' ? 'bg-green-500/20 text-green-500' :
                  platform.status === 'CANARY' ? 'bg-yellow-500/20 text-yellow-500' :
                  'bg-blue-500/20 text-blue-500'
                }`}>
                  {platform.id === 'oanda' ? 'PROTOCOL UNCHAINED' : platform.status}
                </div>
              </div>
              
              {/* OANDA Live Data Viz */}
              {platform.id === 'oanda' ? (
                <div className="my-3 p-2 bg-black/40 rounded border border-gray-700">
                    <div className="flex justify-between items-center text-xs font-mono mb-1">
                        <span className="text-gray-400">EUR/USD</span>
                        <div className="flex items-center gap-1">
                            <Wifi size={10} className="text-green-500" />
                            <span className="text-green-500">LIVE</span>
                        </div>
                    </div>
                    <div className="flex items-baseline gap-2">
                        <span className={`text-lg font-bold ${priceDirection === 'up' ? 'text-green-400' : 'text-red-400'}`}>
                            {eurUsdPrice.toFixed(5)}
                        </span>
                        {priceDirection === 'up' ? <TrendingUp size={12} className="text-green-500"/> : <TrendingDown size={12} className="text-red-500"/>}
                    </div>
                </div>
              ) : null}

              <div className="flex justify-between items-center text-xs mt-2">
                <div className="text-gray-400">
                  Risk: <span className={
                    platform.riskLevel === 'High' ? 'text-red-400' : 'text-green-400'
                  }>{platform.riskLevel}</span>
                </div>
                <div className="text-gray-400">
                    {/* Dynamic PnL for Oanda */}
                    PnL: <span className={`${platform.id === 'oanda' ? (floatingPnL >= 0 ? 'text-green-400' : 'text-red-400') : 'text-white'} font-mono`}>
                        {platform.id === 'oanda' ? `$${floatingPnL.toFixed(2)}` : `$${platform.pnl}`}
                    </span>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-gray-800 flex gap-2">
                <button className="flex-1 bg-gray-800 hover:bg-gray-700 text-xs text-white py-1.5 rounded transition-colors">
                  Logs
                </button>
                <button className="flex-1 bg-gray-800 hover:bg-gray-700 text-xs text-white py-1.5 rounded transition-colors">
                  Config
                </button>
              </div>
            </div>
          ))}

          {/* Master Control */}
           <div className="bg-red-900/10 border border-red-900/30 p-4 rounded-lg mt-6">
                <h4 className="text-red-400 text-sm font-bold mb-3 flex items-center gap-2">
                    <Zap size={16} /> Master Process Control
                </h4>
                <div className="space-y-2">
                    <button className="w-full bg-rick-accent/10 hover:bg-rick-accent hover:text-black border border-rick-accent/50 text-rick-accent py-2 rounded text-xs font-bold transition-all uppercase">
                        INIT: Sequence 0 (Start All)
                    </button>
                     <button className="w-full bg-red-900/20 hover:bg-red-900 text-red-500 hover:text-white border border-red-900/50 py-2 rounded text-xs font-bold transition-all uppercase">
                        Emergency: Safe Shutdown
                    </button>
                </div>
           </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
