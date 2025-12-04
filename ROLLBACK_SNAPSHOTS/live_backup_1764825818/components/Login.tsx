
import React, { useState } from 'react';
import { Shield, Lock, Terminal } from 'lucide-react';

interface LoginProps {
  onLogin: () => void;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [pin, setPin] = useState('');
  const [error, setError] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Default PIN matching the log ID mentioned in user prompts
    if (pin === '9922') {
      onLogin();
    } else {
      setError(true);
      setPin('');
      setTimeout(() => setError(false), 2000);
    }
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center font-mono">
      <div className="w-full max-w-md p-8 bg-rick-dark border border-gray-800 rounded-2xl relative overflow-hidden">
        {/* Decorative Grid Background */}
        <div className="absolute inset-0 bg-[linear-gradient(rgba(0,255,157,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(0,255,157,0.03)_1px,transparent_1px)] bg-[size:20px_20px]" />

        <div className="relative z-10 text-center space-y-6">
          <div className="flex justify-center mb-6">
             <div className={`p-4 rounded-full bg-gray-900 border-2 ${error ? 'border-red-500 animate-bounce' : 'border-rick-accent'}`}>
               {error ? <Lock className="text-red-500" size={32} /> : <Shield className="text-rick-accent" size={32} />}
             </div>
          </div>

          <div>
            <h1 className="text-2xl font-bold text-white tracking-tighter">RICK<span className="text-rick-accent">PHOENIX</span></h1>
            <p className="text-xs text-gray-500 mt-2 uppercase tracking-widest">Secure Command Node Access</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="bg-black/50 p-4 rounded border border-gray-700">
               <div className="flex justify-between text-[10px] text-gray-500 mb-2">
                 <span>GATEWAY</span>
                 <span>WSL-UBUNTU-TUNNEL</span>
               </div>
               <div className="flex gap-2 justify-center">
                 <input 
                   type="password" 
                   maxLength={4}
                   value={pin}
                   onChange={(e) => setPin(e.target.value)}
                   className="bg-transparent border-b-2 border-rick-accent/50 text-center text-2xl font-bold text-white w-32 focus:outline-none focus:border-rick-accent tracking-[1em]"
                   autoFocus
                   placeholder="____"
                 />
               </div>
            </div>

            {error && (
              <div className="text-xs text-red-500 flex items-center justify-center gap-2">
                <Terminal size={12} /> ACCESS DENIED. RETRY.
              </div>
            )}

            <button 
              type="submit"
              className="w-full bg-rick-card hover:bg-gray-800 border border-gray-700 hover:border-rick-accent text-rick-accent py-3 rounded-lg font-bold text-sm transition-all"
            >
              AUTHENTICATE
            </button>
          </form>

          <p className="text-[10px] text-gray-600">
             Log ID Ref: #RBOT-9922-BALANCED
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
