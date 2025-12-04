import { useEffect } from 'react';
import { useOandaTelemetry } from '../hooks/useOandaTelemetry';
import { useQuery } from '@tanstack/react-query';
import { fetchMarketOverview, tradingSocket } from '../services/api';
import { PLATFORM_HEARTBEAT_EVENT, PLATFORM_NAMES, OANDA_HEARTBEAT_MESSAGE } from '../services/constants';
import { AgentStatusGrid } from '../components/dashboard/AgentStatusGrid';
import PlatformStatusGrid from '../components/dashboard/PlatformStatusGrid';
import { MarketOverview } from '../components/dashboard/MarketOverview';
import { RecentSignals } from '../components/dashboard/RecentSignals';
import { ActiveTrades } from '../components/dashboard/ActiveTrades';
import { PerformanceMetrics } from '../components/dashboard/PerformanceMetrics';
import { useDashboardStore } from '../store/useDashboardStore';

export function DashboardPage() {
  const { data: marketData, isLoading } = useQuery({
    queryKey: ['market-overview'],
    queryFn: fetchMarketOverview,
    refetchInterval: 30000,
  });

  const addMarketEvent = useDashboardStore((state) => state.addMarketEvent);
  const addAgentSignal = useDashboardStore((state) => state.addAgentSignal);
  const updateTrade = useDashboardStore((state) => state.updateTrade);
  const setAgentStatus = useDashboardStore((state) => state.setAgentStatus);
  const setPlatformStatus = useDashboardStore((state) => state.setPlatformStatus);
  const platformStatus = useDashboardStore((state) => state.platformStatus);
  // Start telemetry polling for OANDA
  useOandaTelemetry(8000);

  useEffect(() => {
    const unsubscribeMarket = tradingSocket.onMarketEvent((event) => {
      console.log('Market update:', event);
      addMarketEvent(event);
    });

    const unsubscribeSignals = tradingSocket.onAgentSignal((signal) => {
      console.log(`${signal.agent} signal:`, signal);
      addAgentSignal(signal);
    });

    const unsubscribeTrades = tradingSocket.onTradeUpdate((trade) => {
      console.log('Trade update:', trade);
      updateTrade(trade);
    });

    const unsubscribeAgentStatus = tradingSocket.onAgentStatus((status) => {
      console.log('Agent status update:', status);
      setAgentStatus(status);
    });

    const unsubscribeSystemEvents = tradingSocket.onSystemEvent((ev) => {
      // Example event: { type: 'MACHINE_HEARTBEAT', venue: 'oanda', details: { status: 'SCANNING' } }
      try {
        if (!ev || !ev.type) return;
        if (ev.type === PLATFORM_HEARTBEAT_EVENT || ev.type === 'HEARTBEAT') {
          const venue = ev.venue || ev.details?.venue || ev.details?.platform;
          if (!venue) return;
          const platformKey = (venue || '').toLowerCase();

          // Map backend heartbeat values to frontend friendly statuses
          let platformState = 'offline';
          if (ev.details?.status) {
            const s = String(ev.details.status).toLowerCase();
            if (s === 'scanning' || s === 'online' || s === 'active') platformState = 'online';
            else if (s.includes('canary')) platformState = 'canary';
            else if (s.includes('paper')) platformState = 'paper';
          }

          setPlatformStatus({
            ...platformStatus,
            [platformKey]: {
              status: platformState,
              lastHeartbeat: new Date().toISOString(),
              message: platformKey === PLATFORM_NAMES.OANDA ? OANDA_HEARTBEAT_MESSAGE : ev.details?.message || ev.details?.summary || ''
            }
          });

          // Add a market/system event to the feed so it appears in the Live Neural Feed
          if (platformKey === PLATFORM_NAMES.OANDA) {
            addMarketEvent({
              type: 'SYSTEM',
              symbol: 'OANDA',
              price: 0,
              timestamp: new Date().toISOString(),
              news: OANDA_HEARTBEAT_MESSAGE,
              source: 'system'
            });
          }
        }
      } catch (err) {
        console.error('Error handling system event', err);
      }
    });

    tradingSocket.onConnectionFailed(() => {
      console.error('Connection to trading system lost');
      // Optionally update a global connection status in store
    });

    return () => {
      unsubscribeMarket();
      unsubscribeSignals();
      unsubscribeTrades();
      unsubscribeAgentStatus();
      unsubscribeSystemEvents();
      // Do not close the socket here if it's meant to be persistent across the app
      // tradingSocket.close(); 
    };
  }, [addMarketEvent, addAgentSignal, updateTrade, setAgentStatus]);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <MarketOverview data={marketData} loading={isLoading} />
        </div>
        <div>
          <PerformanceMetrics />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-4">
          <AgentStatusGrid />
          <PlatformStatusGrid />
        </div>
        <div className="lg:col-span-2">
          <RecentSignals />
        </div>
      </div>

      <div>
        <ActiveTrades />
      </div>
    </div>
  );
}