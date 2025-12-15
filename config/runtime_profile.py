"""
Config Loader for RICK_PHOENIX Strategy Toggles
Reads config/strategy_toggles.yaml and exposes helper functions.
"""
import yaml
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "strategy_toggles.yaml")

class RuntimeProfile:
    def __init__(self):
        with open(CONFIG_PATH, "r") as f:
            self.config = yaml.safe_load(f)
        self.profile = self.config.get("active_profile", "balanced")
        self.profile_settings = self.config["profiles"].get(self.profile, {})

    def is_enabled(self, key_path):
        keys = key_path.split(".")
        node = self.config
        for k in keys:
            node = node.get(k, {})
        return bool(node) if isinstance(node, bool) else node == "true"

    def get_profile_param(self, param):
        return self.profile_settings.get(param)

    def get_session_strategies(self, venue, session):
        return self.config.get("sessions", {}).get(venue, {}).get(session, {}).get("strategies", [])

    def is_session_active(self, venue, session):
        return self.config.get("sessions", {}).get(venue, {}).get(session, {}).get("active", False)

profile = RuntimeProfile()

# Example usage:
# profile.is_enabled("oanda.enable_strategic_flip_hedge")
# profile.get_profile_param("risk_per_trade_pct")
# profile.get_session_strategies("oanda", "london")
# profile.is_session_active("oanda", "london")
