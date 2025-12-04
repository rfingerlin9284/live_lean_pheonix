
import React from 'react';
import { LayoutDashboard, Scale, ShieldAlert, Terminal, Activity, FileText, BookOpen } from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    { id: 'dashboard', icon: LayoutDashboard, label: 'Command Node' },
    { id: 'cheat-sheet', icon: BookOpen, label: 'System Organs' },
    { id: 'platforms', icon: Activity, label: 'Platforms' },
    { id: 'lawmaker', icon: Scale, label: 'Lawmaker Rules' },
    { id: 'prompts', icon: Terminal, label: 'Agent Prompts' },
    { id: 'logs', icon: FileText, label: 'System Logs' },
  ];

  return (
    <div className="w-64 bg-rick-black border-r border-rick-card h-screen flex flex-col fixed left-0 top-0 z-20">
      <div className="p-6 border-b border-rick-card">
        <h1 className="text-xl font-bold font-mono tracking-tighter text-white">
          RICK<span className="text-rick-accent">PHOENIX</span>
        </h1>
        <p className="text-xs text-gray-500 mt-1 font-mono">AUTONOMOUS HIVE v2.4</p>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 group ${
                isActive 
                  ? 'bg-rick-card text-rick-accent border border-rick-accent/20' 
                  : 'text-gray-400 hover:bg-rick-card hover:text-white'
              }`}
            >
              <Icon size={20} className={`${isActive ? 'text-rick-accent' : 'text-gray-500 group-hover:text-white'}`} />
              <span className="font-medium text-sm">{item.label}</span>
              {isActive && (
                <div className="ml-auto w-1.5 h-1.5 rounded-full bg-rick-accent shadow-[0_0_8px_#00ff9d]" />
              )}
            </button>
          );
        })}
      </nav>

      <div className="p-4 border-t border-rick-card">
        <div className="bg-rick-dark p-3 rounded border border-red-900/30">
          <div className="flex items-center gap-2 mb-2 text-red-500">
            <ShieldAlert size={16} />
            <span className="text-xs font-bold uppercase tracking-wider">Helper Script</span>
          </div>
          <p className="text-[10px] text-gray-400 font-mono leading-relaxed">
            Monitoring active directory for unauthorized mutations.
            <br />
            <span className="text-green-500">System Secure.</span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
