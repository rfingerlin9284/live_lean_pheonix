#!/usr/bin/env python3
"""
Strategy Advisor & Performance Tracker for RBOTzilla
PIN: 841921

- Defines normalized strategy families (mean_reversion, fvg, scalping, trend, other)
- Tracks realized performance per family (R, winrate, count)
- Provides preferred family ordering for the engine
- Feeds Rick/Hive with a clean snapshot of current "best edges"
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import time


class StrategyFamily(str, Enum):
    MEAN_REVERSION = "mean_reversion"
    FVG = "fvg"
    SCALPING = "scalping"
    TREND = "trend"
    OTHER = "other"


@dataclass
class FamilyStats:
    name: str
    trades: int = 0
    wins: int = 0
    losses: int = 0
    total_r: float = 0.0  # sum of R-multiples
    last_updated: float = field(default_factory=time.time)

    @property
    def win_rate(self) -> float:
        if self.trades == 0:
            return 0.0
        return self.wins / self.trades

    @property
    def avg_r(self) -> float:
        if self.trades == 0:
            return 0.0
        return self.total_r / self.trades


class StrategyAdvisor:
    """
    Central place to:
    - Normalize strategy family labels
    - Track realized performance per family
    - Provide preferred family list to the engine
    """

    def __init__(self, preferred_families: Optional[List[str]] = None):
        # Default structural preference (can be overridden by env)
        # These reflect your stated edge priorities.
        base_order = [
            StrategyFamily.MEAN_REVERSION.value,
            StrategyFamily.FVG.value,
            StrategyFamily.SCALPING.value,
            StrategyFamily.TREND.value,
            StrategyFamily.OTHER.value,
        ]

        if preferred_families:
            # Sanitize and overlay
            cleaned = [f.strip().lower() for f in preferred_families if f.strip()]
            # Keep custom order but ensure all families are present
            seen = set()
            merged = []
            for f in cleaned + base_order:
                fl = f.lower()
                if fl not in seen:
                    merged.append(fl)
                    seen.add(fl)
            self._base_order = merged
        else:
            self._base_order = [f.lower() for f in base_order]

        self.family_stats: Dict[str, FamilyStats] = {
            fam: FamilyStats(name=fam) for fam in self._base_order
        }

    # ------------------------------------------------------------------
    # Normalization and labeling
    # ------------------------------------------------------------------
    def normalize_family(self, family: Optional[str]) -> str:
        if not family:
            return StrategyFamily.OTHER.value
        f = family.lower()
        if "bollinger" in f or "rsi" in f or "sideways" in f or "range" in f:
            return StrategyFamily.MEAN_REVERSION.value
        if "fvg" in f or "gap" in f or "liquidity" in f:
            return StrategyFamily.FVG.value
        if "scalp" in f or "scalping" in f or "momentum" in f:
            return StrategyFamily.SCALPING.value
        if "trend" in f or "breakout" in f or "trend_follow" in f:
            return StrategyFamily.TREND.value
        # Already one of the enum values?
        if f in [x.value for x in StrategyFamily]:
            return f
        return StrategyFamily.OTHER.value

    # ------------------------------------------------------------------
    # Performance tracking
    # ------------------------------------------------------------------
    def record_closed_trade(
        self,
        family: Optional[str],
        r_multiple: float,
        pnl_pips: float,
        meta: Optional[Dict] = None,
    ):
        fam = self.normalize_family(family)
        fs = self.family_stats.get(fam)
        if not fs:
            fs = FamilyStats(name=fam)
            self.family_stats[fam] = fs

        fs.trades += 1
        if r_multiple > 0:
            fs.wins += 1
        elif r_multiple < 0:
            fs.losses += 1
        fs.total_r += r_multiple
        fs.last_updated = time.time()

    # ------------------------------------------------------------------
    # Preferred families for engine
    # ------------------------------------------------------------------
    def get_preferred_families(self) -> List[str]:
        """
        Return families in order of preference.
        For now this blends base preference with basic performance;
        you can make this more dynamic later.
        """
        scored = []
        for fam, fs in self.family_stats.items():
            # base index: how early in base order
            base_idx = self._base_order.index(fam) if fam in self._base_order else 99
            # simple performance adjustment: avg_r + winrate bump
            perf_score = fs.avg_r + fs.win_rate
            # lower sort key = higher priority; invert perf as negative
            scored.append((base_idx, -perf_score, fam))

        scored.sort()
        return [fam for _, __, fam in scored]

    def get_snapshot(self) -> Dict:
        """Return a compact snapshot for Rick/Hive narration."""
        out = {
            "families": [],
            "preferred_order": self.get_preferred_families(),
        }
        for fam, fs in self.family_stats.items():
            out["families"].append(
                {
                    "family": fam,
                    "trades": fs.trades,
                    "wins": fs.wins,
                    "losses": fs.losses,
                    "win_rate": fs.win_rate,
                    "avg_r": fs.avg_r,
                    "last_updated": fs.last_updated,
                }
            )
        return out
