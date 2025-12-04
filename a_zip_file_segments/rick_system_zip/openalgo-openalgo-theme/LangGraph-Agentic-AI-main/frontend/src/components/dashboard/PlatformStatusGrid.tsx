import React, { useState } from 'react';
import { useDashboardStore } from '../../store/useDashboardStore';
import { Badge, Modal } from '@mantine/core';
import { Wifi, WifiOff, Database } from 'lucide-react';
import { PLATFORM_NAMES } from '../../services/constants';

export function PlatformStatusGrid() {
  const platformStatus = useDashboardStore((state) => state.platformStatus);
  const [verifyOpen, setVerifyOpen] = useState(false);
  const [verifyBody, setVerifyBody] = useState<any>(null);
  const [testOpen, setTestOpen] = useState(false);
  const [testOrder, setTestOrder] = useState({ instrument: 'EUR_USD', entry_price: 1.08, stop_loss: 1.075, take_profit: 1.095, units: 100 });
  const [testResult, setTestResult] = useState<any>(null);

  const platforms = [
    { id: PLATFORM_NAMES.OANDA, label: 'OANDA' },
    { id: PLATFORM_NAMES.COINBASE, label: 'Coinbase' },
    { id: PLATFORM_NAMES.IBKR, label: 'IBKR' },
  ];

  const statusBadge = (status?: string) => {
    switch (status) {
      case 'online':
        return <Badge color="teal" variant="light">Online</Badge>;
      case 'canary':
        return <Badge color="yellow" variant="light">Canary</Badge>;
      case 'paper':
        return <Badge color="gray" variant="light">Paper</Badge>;
      default:
        return <Badge color="red" variant="light">Offline</Badge>;
    }
  };

  return (
    <div className="bg-dark-700 rounded-xl p-6">
      <h2 className="text-xl font-bold text-neon-primary mb-4">Platform Status</h2>
      <div className="grid grid-cols-1 gap-4">
        {platforms.map((p) => {
          const status = platformStatus[p.id];
          const isLive = status?.status === 'online';
          return (
            <div
              key={p.id}
              className={`p-4 rounded-lg border ${isLive ? 'border-green-500' : 'border-gray-700'} bg-dark-800 flex items-center justify-between`}
            >
              <div className="flex items-center space-x-3">
                <div className={`p-2 rounded-full ${isLive ? 'bg-green-500/10' : 'bg-gray-700/10'}`}>
                  {isLive ? <Wifi className="text-green-400" /> : <WifiOff className="text-gray-400" />}
                </div>
                <div>
                  <h3 className="font-medium">{p.label}</h3>
                  <p className="text-sm text-gray-400">{status?.message ?? ''}</p>
                  {p.id === PLATFORM_NAMES.OANDA && status?.tradingEnabled !== undefined && (
                    <div className="text-xs text-gray-400 mt-1">
                      Trade Enabled: <span className={`${status.tradingEnabled ? 'text-green-400' : 'text-yellow-400'} font-bold`}>{String(status.tradingEnabled)}</span>
                      {status.balance !== undefined && (` | Bal: $${Number(status.balance).toFixed(2)}`)}
                    </div>
                  )}
                </div>
              </div>
              <div className="flex items-center space-x-3">
                {statusBadge(status?.status)}
                {isLive && (
                  <span className="inline-block w-3 h-3 rounded-full bg-green-400 animate-pulse" aria-hidden></span>
                )}
              </div>
              <div className="ml-4 flex items-center gap-2">
                  {p.id === PLATFORM_NAMES.OANDA && (
                  <button
                    onClick={async () => {
                      try {
                        const res = await fetch('/api/broker/oanda/account');
                        const body = await res.json();
                        console.log('OANDA verify response', body);
                        setVerifyBody(body);
                        setVerifyOpen(true);
                      } catch (e) {
                        console.error('OANDA verify failed', e);
                        setVerifyBody({ error: 'Failed to verify OANDA account' });
                        setVerifyOpen(true);
                      }
                    }}
                    className="bg-blue-800 hover:bg-blue-700 text-xs text-white px-2 py-1 rounded transition-colors"
                    >
                    Verify
                  </button>
                )}
                {p.id === PLATFORM_NAMES.OANDA && (
                  <button
                    className="bg-green-800 hover:bg-green-700 text-xs text-white px-2 py-1 rounded transition-colors"
                    onClick={() => { setTestOpen(true); setTestResult(null); }}
                  >
                    Test OCO
                  </button>
                )}
              </div>
              {/* Verification Modal */}
              <Modal opened={verifyOpen} onClose={() => setVerifyOpen(false)} title="OANDA Account Verification" size="lg">
                {verifyBody ? (
                  <div className="font-mono text-sm">
                    <pre>{JSON.stringify(verifyBody, null, 2)}</pre>
                  </div>
                ) : (
                  <div>Loading...</div>
                )}
              </Modal>

              <Modal opened={testOpen} onClose={() => setTestOpen(false)} title="Test Practice OCO (Practice only)" size="lg">
                <div className="space-y-2">
                  <label className="text-xs font-bold">Instrument</label>
                  <input className="w-full p-2 bg-dark-900 rounded" value={testOrder.instrument} onChange={(e)=>setTestOrder({...testOrder, instrument:e.target.value})} />
                  <div className="grid grid-cols-3 gap-2">
                    <div>
                      <label className="text-xs">Entry</label>
                      <input className="w-full p-2 bg-dark-900 rounded" value={String(testOrder.entry_price)} onChange={(e)=>setTestOrder({...testOrder, entry_price: parseFloat(e.target.value)})} />
                    </div>
                    <div>
                      <label className="text-xs">SL</label>
                      <input className="w-full p-2 bg-dark-900 rounded" value={String(testOrder.stop_loss)} onChange={(e)=>setTestOrder({...testOrder, stop_loss: parseFloat(e.target.value)})} />
                    </div>
                    <div>
                      <label className="text-xs">TP</label>
                      <input className="w-full p-2 bg-dark-900 rounded" value={String(testOrder.take_profit)} onChange={(e)=>setTestOrder({...testOrder, take_profit: parseFloat(e.target.value)})} />
                    </div>
                  </div>
                  <label className="text-xs">Units</label>
                  <input className="w-full p-2 bg-dark-900 rounded" value={String(testOrder.units)} onChange={(e)=>setTestOrder({...testOrder, units: parseInt(e.target.value)})} />
                  <div className="flex gap-2 mt-3">
                    <button
                      className="bg-red-800 hover:bg-red-700 text-xs text-white px-3 py-2 rounded"
                      onClick={() => setTestOpen(false)}
                    >Cancel</button>
                    <button
                      className="bg-rick-accent hover:bg-rick-accent/90 text-xs text-white px-3 py-2 rounded"
                      onClick={async ()=>{
                        // Confirm explicit user consent prior to calling the endpoint
                        if(!confirm('This will place a PRACTICE order on OANDA practice account. Continue?')) return;
                        try{
                          const res = await fetch('/api/broker/oanda/place_practice_oco', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...testOrder, confirm:true }) });
                          const body = await res.json();
                          setTestResult({ status: res.status, body });
                        }catch(e){ setTestResult({ error: String(e) }); }
                      }}
                    >Place Practice OCO</button>
                  </div>
                  {testResult && (
                    <div className="mt-3 font-mono text-xs text-gray-300">
                      <pre>{JSON.stringify(testResult, null, 2)}</pre>
                    </div>
                  )}
                </div>
              </Modal>
            </div>
          );
        })}
          <div className="mt-4 pt-3 border-t border-gray-800 flex gap-2">
            {p.id === PLATFORM_NAMES.OANDA && (
              <button
                onClick={async () => {
                  try {
                    const res = await fetch('/api/broker/oanda/account');
                    const body = await res.json();
                    console.log('OANDA verify response', body);
                    alert(`OANDA verify: ${JSON.stringify(body)}`);
                  } catch (e) {
                    console.error('OANDA verify failed', e);
                    alert('Failed to verify OANDA account');
                  }
                }}
                className="flex-1 bg-blue-800 hover:bg-blue-700 text-xs text-white py-1.5 rounded transition-colors"
              >
                Verify
              </button>
            )}
          </div>
      </div>
    </div>
  );
}

export default PlatformStatusGrid;
