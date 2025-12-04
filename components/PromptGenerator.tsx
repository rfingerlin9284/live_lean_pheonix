
import React, { useState } from 'react';
import { PROMPT_TEMPLATES } from '../constants';
import { Copy, Check, Terminal, PlayCircle, FileSearch, ArrowRight, Zap } from 'lucide-react';

const PromptGenerator: React.FC = () => {
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const handleCopy = (content: string, id: string) => {
    navigator.clipboard.writeText(content);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Transmission Protocol Guide */}
      <div className="bg-gradient-to-r from-blue-900/20 to-purple-900/20 border border-blue-500/30 rounded-xl p-6">
        <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Zap className="text-blue-400" size={24} />
          Transmission Protocol: The Air Gap
        </h2>
        <div className="flex items-center gap-4 text-sm">
          <div className="flex-1 bg-black/40 p-3 rounded border border-gray-700 text-center">
            <div className="font-bold text-white mb-1">1. COMMAND NODE</div>
            <div className="text-xs text-gray-500">(This Web App)</div>
            <div className="mt-2 text-xs text-blue-400">Generates Strategy</div>
          </div>
          <ArrowRight className="text-gray-600" />
          <div className="flex-1 bg-rick-accent/10 p-3 rounded border border-rick-accent/50 text-center relative overflow-hidden">
            <div className="absolute inset-0 bg-rick-accent/5 animate-pulse" />
            <div className="font-bold text-white mb-1">2. YOU (THE BRIDGE)</div>
            <div className="text-xs text-gray-500">(Copy & Paste)</div>
            <div className="mt-2 text-xs text-rick-accent font-bold">Transfer Orders</div>
          </div>
          <ArrowRight className="text-gray-600" />
          <div className="flex-1 bg-black/40 p-3 rounded border border-gray-700 text-center">
            <div className="font-bold text-white mb-1">3. RAPTOR AGENT</div>
            <div className="text-xs text-gray-500">(Your VS Code)</div>
            <div className="mt-2 text-xs text-green-400">Executes Code</div>
          </div>
        </div>
      </div>

      <div className="mb-4">
        <h2 className="text-2xl font-bold text-white mb-2">Agent Prompt Generator</h2>
        <p className="text-gray-400 text-sm">
          Select a rigorous, pre-constructed "Mega Prompt". Copy the content and paste it into your local VS Code agent to execute the directives.
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {PROMPT_TEMPLATES.map((template) => (
          <div key={template.id} className="bg-rick-card border border-gray-800 rounded-xl flex flex-col h-full hover:border-rick-accent/30 transition-colors">
            <div className="p-6 border-b border-gray-800">
              <div className="flex items-center gap-2 mb-3">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    template.title.includes('Ingestion') ? 'bg-purple-500/10 text-purple-400' : 
                    template.title.includes('FORCE') ? 'bg-red-500/10 text-red-500' :
                    'bg-rick-accent/10 text-rick-accent'
                }`}>
                   {template.title.includes('Ingestion') ? <FileSearch size={16} /> : <Terminal size={16} />}
                </div>
                <h3 className="text-lg font-bold text-white">{template.title}</h3>
              </div>
              <p className="text-gray-400 text-sm">{template.description}</p>
            </div>

            <div className="p-4 bg-black/40 flex-1 relative group">
              <pre className="text-xs text-gray-300 font-mono whitespace-pre-wrap overflow-y-auto max-h-[300px] p-2">
                {template.content}
              </pre>
              
              <div className="absolute inset-0 bg-gradient-to-t from-rick-card via-transparent to-transparent opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity" />
            </div>

            <div className="p-4 border-t border-gray-800 flex justify-between items-center bg-rick-dark/50">
               <div className="flex items-center gap-2">
                  <span className={`w-2 h-2 rounded-full animate-pulse ${
                      template.title.includes('Ingestion') ? 'bg-purple-500' : 'bg-rick-accent'
                  }`}></span>
                  <span className="text-[10px] text-gray-500 uppercase font-bold tracking-wider">Ready for VS Code</span>
               </div>
              <button
                onClick={() => handleCopy(template.content, template.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded text-sm font-bold transition-all ${
                  copiedId === template.id
                    ? 'bg-green-500 text-white'
                    : 'bg-rick-accent text-rick-black hover:bg-white'
                }`}
              >
                {copiedId === template.id ? (
                  <>
                    <Check size={16} /> Copied
                  </>
                ) : (
                  <>
                    <Copy size={16} /> Copy Prompt
                  </>
                )}
              </button>
            </div>
          </div>
        ))}
        
        {/* Custom Builder Card */}
        <div className="bg-rick-card border border-dashed border-gray-700 rounded-xl p-8 flex flex-col items-center justify-center text-center space-y-4 hover:border-gray-500 transition-colors cursor-pointer opacity-75 hover:opacity-100">
            <div className="w-12 h-12 rounded-full bg-gray-800 flex items-center justify-center text-gray-400">
                <PlayCircle size={24} />
            </div>
            <div>
                <h3 className="text-lg font-bold text-white">Generate Custom Directive</h3>
                <p className="text-gray-400 text-xs mt-1 max-w-xs mx-auto">
                    Combine specific Lawmaker modules with a new task (e.g., "Add new indicator to Oanda").
                    Includes automatic safety wrapper.
                </p>
            </div>
        </div>
      </div>
    </div>
  );
};

export default PromptGenerator;
