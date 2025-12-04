
import React from 'react';
import { ORGAN_SYSTEMS, VSCODE_TASKS } from '../constants';
import { Brain, Activity, Zap, Eye, Command, Terminal, FileCode } from 'lucide-react';

const CheatSheet: React.FC = () => {
  const getIcon = (id: string) => {
    switch (id) {
      case 'brain': return Brain;
      case 'nervous': return Activity;
      case 'limbs': return Zap;
      case 'senses': return Eye;
      default: return FileCode;
    }
  };

  return (
    <div className="space-y-8">
      <div className="border-b border-gray-800 pb-6">
        <h2 className="text-2xl font-bold text-white mb-2">System Organ Cheat Sheet</h2>
        <p className="text-gray-400 text-sm max-w-2xl">
          A visual map of the Rick Phoenix file structure grouped by function ("Organ"). 
          Use this to reference where specific logic lives without memorizing paths.
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Organ Systems */}
        <div className="space-y-6">
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <FileCode className="text-rick-accent" size={20} />
            File Structure by Organ
          </h3>
          <div className="grid gap-4">
            {ORGAN_SYSTEMS.map((system) => {
              const Icon = getIcon(system.id);
              return (
                <div key={system.id} className="bg-rick-card border border-gray-800 rounded-xl p-5 hover:border-gray-600 transition-colors">
                  <div className="flex items-start gap-4">
                    <div className={`p-3 rounded-lg bg-gray-900 ${system.color}`}>
                      <Icon size={24} />
                    </div>
                    <div className="flex-1">
                      <h4 className={`text-md font-bold uppercase tracking-wider mb-1 ${system.color}`}>
                        {system.name}
                      </h4>
                      <p className="text-xs text-gray-500 mb-3 font-mono">{system.role}</p>
                      <div className="bg-black/30 rounded p-3 space-y-2">
                        {system.files.map((file, idx) => (
                          <div key={idx} className="flex items-center gap-2 text-xs text-gray-300 font-mono">
                            <span className="w-1.5 h-1.5 rounded-full bg-gray-600"></span>
                            {file}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* VS Code Tasks */}
        <div className="space-y-6">
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Command className="text-rick-accent" size={20} />
            VS Code Task Shortcuts
          </h3>
          <div className="bg-rick-dark border border-gray-800 rounded-xl p-6">
            <p className="text-sm text-gray-400 mb-4">
              These tasks are pre-configured in your <span className="font-mono text-white bg-gray-800 px-1 rounded">tasks.json</span>. 
              Open Command Palette (Ctrl+Shift+P) -> "Tasks: Run Task" to execute.
            </p>
            <div className="space-y-3">
              {VSCODE_TASKS.map((task) => (
                <div key={task.id} className="group bg-rick-card border border-gray-800 hover:border-rick-accent/50 p-4 rounded-lg transition-all cursor-default">
                  <div className="flex justify-between items-start mb-2">
                    <span className="font-bold text-white text-sm group-hover:text-rick-accent transition-colors">
                      {task.label}
                    </span>
                    <Terminal size={14} className="text-gray-600 group-hover:text-rick-accent" />
                  </div>
                  <div className="bg-black rounded px-2 py-1.5 mb-2 font-mono text-[10px] text-gray-500 truncate">
                    &gt; {task.command}
                  </div>
                  <p className="text-xs text-gray-400">{task.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Helper Note */}
          <div className="bg-blue-900/10 border border-blue-500/20 p-4 rounded-xl">
             <h4 className="text-blue-400 text-sm font-bold mb-1">Tip: Remote Control</h4>
             <p className="text-xs text-gray-400 leading-relaxed">
               You can run these tasks remotely if you SSH into your laptop or use a secure tunnel. 
               The "Watchdog" script in the SENSES organ will auto-restart these tasks if the system freezes.
             </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CheatSheet;
