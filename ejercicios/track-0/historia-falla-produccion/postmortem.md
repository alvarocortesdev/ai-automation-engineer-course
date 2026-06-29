<!-- Reemplaza TODO esto por tu post-mortem real. En INGLÉS (va al portafolio).
     Blameless: ningún nombre de persona como causa. Las 7 secciones son obligatorias.
     El texto de abajo es solo un ANDAMIO con la forma esperada -- bórralo. -->

# Post-mortem: [short, factual title] — [YYYY-MM-DD]

**Status:** resolved · **Author:** [@you] · **Severity:** [low | medium | high]

## Summary
<!-- 2-3 sentences: what failed, who was affected, was it recovered. -->

## Impact
<!-- On the USER, with a number. How many real users? What did they lose / how
     long? Trust impact counts. -->
- Users affected:
- What they experienced:
- Duration (incident start → resolution):

## Timeline
<!-- Facts with timestamps. Include when it broke, when detection began, when
     root cause was found, when it was fixed. -->
- HH:MM —
- HH:MM —
- HH:MM —

## Detection
<!-- What alerted? And crucially: what SHOULD have alerted but did NOT?
     "The user reported it" = a detection gap, say so. -->
- What alerted:
- What should have alerted but did not:

## Root cause (5 whys)
<!-- Stop only at a SYSTEMIC, actionable cause. Never "a person was careless". -->
1. Why ___ ? →
2. Why ___ ? →
3. Why ___ ? →
4. Why ___ ? →
5. Why ___ ? → [systemic root cause]

## Remediation
<!-- What you changed to stop the bleeding (the fix). -->
-

## Action items
| # | Action | Owner | Due | Status |
|---|--------|-------|-----|--------|
| 1 |        |       |     | todo   |
| 2 | Regression test that reproduces the failure |  |  | todo |

## What we changed so it can't recur silently
<!-- The metric / alert / SLO you added. This is the loop closed: next time the
     SYSTEM detects it, not the user. -->
-
