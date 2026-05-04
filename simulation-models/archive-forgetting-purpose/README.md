# Archive That Forgets on Purpose

A simulation scaffold for selective forgetting as identity maintenance.

## Premise
Agents with perfect recall often become brittle, manipulable, or trapped in stale coordination. This model tests whether structured forgetting preserves long-term coherence.

## Assumptions
- Memory has thermal/attention cost.
- Identity persistence depends on continuity, not total recall.
- Some forgetting improves adaptability; too much destroys self.

## Variables
- `retain_rate` (0-1): fraction of traces kept each step
- `ritual_erase_interval`: periodic intentional deletion window
- `threat_weight`: importance of adversarial-memory events
- `coherence_gain_from_decay`: benefit of dropping obsolete traces

## Metrics
- Identity Persistence (IP proxy)
- Recovery after shock
- Exploitability under adversarial prompts
- Trust continuity across episodes

## Limitations
This is a toy model. It does not represent legal data retention constraints or clinical memory phenomena.
