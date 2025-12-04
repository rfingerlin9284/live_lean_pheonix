import asyncio
import os
import json
import time

import os

# Delay import of engine until after we set environment override in tests


class DummyConnector:
    def get_live_prices(self, symbols):
        return None


async def _run_emitter_for_seconds(engine, seconds=3.5):
    engine.oanda = DummyConnector()
    engine.running = True
    task = asyncio.create_task(engine._market_tick_emitter())
    await asyncio.sleep(seconds)
    engine.running = False
    try:
        task.cancel()
    except Exception:
        pass


def test_market_tick_emitter_writes_events(tmp_path):
    # Ensure narration file is isolated for the test
    env_file = tmp_path / "narration_test.jsonl"
    os.environ['NARRATION_FILE_OVERRIDE'] = str(env_file)
    if env_file.exists():
        env_file.unlink()

    # import engine after setting environment override to ensure narration logger picks up the override
    # By default, the telemetry emitter should NOT be started by OandaTradingEngine.run()
    from oanda.oanda_trading_engine import OandaTradingEngine
    # Ensure opt-in is disabled
    os.environ.pop('ENABLE_TELEM_EMITTER', None)
    engine = OandaTradingEngine(environment='practice')
    # Ensure the engine does not auto-start the emitter task when not enabled
    assert engine.market_tick_task is None

    # Now opt-in via env var and call run() to start background tasks
    os.environ['ENABLE_TELEM_EMITTER'] = 'true'
    env_file = tmp_path / "narration_test.jsonl"
    os.environ['NARRATION_FILE_OVERRIDE'] = str(env_file)
    if env_file.exists():
        env_file.unlink()

    # Run the engine's run() in a task for a few seconds to ensure market tick emitter spawns
    async def run_engine_for(seconds=6.5):
        rtask = asyncio.create_task(engine.run())
        await asyncio.sleep(seconds)
        engine.running = False
        try:
            await rtask
        except Exception:
            pass

    asyncio.run(run_engine_for())

    # Read events
    assert env_file.exists(), "narration file not created"
    with open(env_file, 'r') as f:
        lines = [json.loads(l) for l in f if l.strip()]
    # There should be at least one MARKET_TICK event.
        assert any(e.get('event_type') == 'MARKET_TICK' for e in lines), 'No MARKET_TICK events found'
