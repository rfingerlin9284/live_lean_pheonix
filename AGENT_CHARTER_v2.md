# AGENT CHARTER v2 (RICK_PHOENIX)
**USER ROLE**: Creator (Absolute Authority) | **AUTH**: 841921

## ARCHITECTURE: HIVE MIND vs RBOTZILLA
1. **THE BRAIN**: RICK Hive Mind (Inference Only).
2. **THE BODY**: RBotZilla (Execution & Safety).

## IMMUTABLE RULES
1. **NO PARTIAL PATCHES**: Output ENTIRE FILE content.
2. **SEMANTICS**: "Canary"/"Ghost" -> **"Paper"**.
3. **MICRO-TRADING**: 
   - **DISABLED** by default (< 1000 units rejected).
   - **M15 FLOOR**: No M1/M5 logic allowed without explicit override.
4. **STATE**: All changes must be logged via `change_tracker.py`.

## CONSTRUCTION LOGS & AGENT SHIFT PREVENTION
All code changes, refactors, and test updates must be accompanied by a construction log entry using `change_tracker.py` or an equivalent system. This log must include:
- Description of the change
- Reason for the change
- Agent identity (if applicable)
- Timestamp
Silent changes and agent drift are strictly prohibited. All modifications must be explicit, logged, and reviewable by the user.

## AGENT AUTONOMY
The agent is responsible for all coding and testing. The user only approves. APPROVED 841921.
