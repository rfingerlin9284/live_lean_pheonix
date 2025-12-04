import { useEffect } from 'react';
import { useDashboardStore } from '../store/useDashboardStore';
import { fetchOandaStatus } from '../services/api';

export const useOandaTelemetry = (intervalMs = 8000) => {
  const setPlatformStatus = useDashboardStore((s) => s.setPlatformStatus);

  useEffect(() => {
    let mounted = true;
    const poll = async () => {
      try {
        const data = await fetchOandaStatus();
        if (!mounted || !data) return;
        // Determine status and message
        const status = data.trading_enabled ? 'online' : 'paper';
        let message = `${data.environment?.toUpperCase() || 'PRACTICE'} - `;
        const acct = data.account_summary?.account_id || data.account_id || '';
        if (acct) message += `Acct: ${acct}`;
        if (data.account_summary?.balance !== undefined) {
          message += ` | Bal: ${data.account_summary.balance} ${data.account_summary.currency || 'USD'}`;
        }

        setPlatformStatus({
          oanda: {
            status: status as any,
            lastHeartbeat: new Date().toISOString(),
            message,
            tradingEnabled: !!data.trading_enabled,
            balance: data.account_summary?.balance
          }
        } as any);
      } catch (e) {
        // Report offline on errors
        setPlatformStatus({ oanda: { status: 'offline', message: 'Telemetry unavailable' } } as any);
      }
    };

    // Fire immediately, then poll
    poll();
    const id = setInterval(poll, intervalMs);
    return () => {
      mounted = false;
      clearInterval(id);
    };
  }, [setPlatformStatus, intervalMs]);
};

export default useOandaTelemetry;
