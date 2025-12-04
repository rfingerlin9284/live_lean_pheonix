
import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import Lawmaker from './components/Lawmaker';
import PromptGenerator from './components/PromptGenerator';
import CheatSheet from './components/CheatSheet';
import { Activity, FileText } from 'lucide-react';
import { RECENT_LOGS } from './constants';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'lawmaker':
        return <Lawmaker />;
      case 'prompts':
        return <PromptGenerator />;
      case 'cheat-sheet':
        return <CheatSheet />;
      case 'logs':
        return <LogsView />;
      case 'platforms':
        return <PlatformsPlaceholder />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-black text-gray-100 font-sans">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="ml-64 p-8">
        <header className="mb-8 flex justify-between items-center">
           <div>
             <h2 className="text-gray-500 text-sm font-mono uppercase tracking-widest">System Interface</h2>
             <div className="flex items-center gap-2 mt-1">
               <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
               <span className="text-xs text-green-500 font-bold">WSL // UBUNTU // RICK_PHOENIX_ROOT</span>
             </div>
           </div>
           
           <div className="flex items-center gap-4">
              <div className="text-right">
                <div className="text-xs text-gray-500">Global Lawmaker Approval</div>
                <div className="text-sm font-mono text-rick-accent">#RBOT-9922-BALANCED</div>
              </div>
           </div>
        </header>

        {renderContent()}
      </main>
    </div>
  );
}

const LogsView = () => (
  <div className="space-y-4">
    <h2 className="text-2xl font-bold text-white mb-6">Immutable System Logs</h2>
    <div className="bg-rick-dark border border-gray-800 rounded-xl overflow-hidden font-mono text-sm">
      <div className="bg-gray-900 px-4 py-2 border-b border-gray-800 flex gap-4 text-xs text-gray-500 uppercase tracking-wider">
        <div className="w-40">Timestamp</div>
        <div className="w-32">Agent</div>
        <div className="flex-1">Message</div>
        <div className="w-48 text-right">Approval Sig</div>
      </div>
      {RECENT_LOGS.map((log) => (
        <div key={log.id} className="px-4 py-3 border-b border-gray-800/50 flex gap-4 hover:bg-gray-800/30 transition-colors">
          <div className="w-40 text-gray-500 text-xs">{log.timestamp}</div>
          <div className={`w-32 font-bold ${
            log.agent === 'Rick Hive' ? 'text-blue-400' : 
            log.agent === 'Helper Script' ? 'text-red-400' : 
            log.agent === 'System' ? 'text-green-400' : 'text-rick-accent'
          }`}>{log.agent}</div>
          <div className="flex-1 text-gray-300">{log.message}</div>
          <div className="w-48 text-right text-xs text-gray-600 truncate">{log.approvalCode}</div>
        </div>
      ))}
    </div>
  </div>
);

const PlatformsPlaceholder = () => (
  <div className="flex flex-col items-center justify-center h-[50vh] text-center space-y-4">
    <Activity size={48} className="text-gray-700" />
    <h3 className="text-xl font-bold text-gray-500">Platform Management Console</h3>
    <p className="text-gray-600 max-w-md">
      Detailed configuration for Oanda, Coinbase, and IBKR. 
      Use the Dashboard for high-level metrics or the "Prompts" tab to generate agent commands for specific platform tuning.
    </p>
  </div>
);

export default App;
