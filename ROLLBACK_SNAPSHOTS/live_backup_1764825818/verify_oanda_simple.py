import sys
import os
sys.path.append(os.getcwd())
from oanda.brokers.oanda_connector import OandaConnector

def main():
    print("--- OANDA CONNECTIVITY CHECK ---")
    try:
        connector = OandaConnector(pin=841921, environment="practice")
        print(f"Environment: {connector.environment}")
        print(f"Account ID: {connector.account_id}")
        
        # Check account summary
        print("\nFetching Account Summary...")
        resp = connector._make_request("GET", f"/v3/accounts/{connector.account_id}/summary")
        if resp['success']:
            data = resp['data']['account']
            print(f"✅ Connection Successful!")
            print(f"Balance: {data['balance']} {data['currency']}")
            print(f"NAV: {data['NAV']}")
            print(f"Open Trades: {data['openTradeCount']}")
            print(f"Open Positions: {data['openPositionCount']}")
        else:
            print(f"❌ Failed to get summary: {resp.get('error')}")

        # Check open orders
        print("\nFetching Open Orders...")
        orders = connector.get_orders()
        print(f"Pending Orders: {len(orders)}")
        for o in orders:
            print(f" - {o['id']}: {o['instrument']} {o['type']} {o.get('units')} units")

    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    main()
