# Proposed Risk Acceptance Memorandum — FinanceFlow Inc.

**Risk ID:** RA-2026-017  
**System:** PaymentReconciler v3.2 / Oracle 12c payment database  
**Business risk owner:** CFO (proposed; approval pending)  
**Assessment date:** 10 November 2026

## Executive summary

PaymentReconciler uses one shared database-administrator account in the PCI CDE. Its static password has not been rotated for 18 months and is known by 15 people. Database query logging is absent. A person who obtains that password could read cardholder and transaction data or alter reconciliation records, and FinanceFlow may be unable to determine what occurred. The system supports approximately $2B in annual transactions.

**Recommendation:** Do not approve a permanent acceptance. Request only a time-bound, conditional acceptance after immediate safeguards are implemented and before the replacement project is funded. No CFO approval has been obtained or recorded.

## Assessment

| Factor | Assessment | Basis |
|---|---|---|
| Likelihood | High | Broad password knowledge, 18-month non-rotation, static credential in configuration, no query logging. |
| Impact | Very high | PCI cardholder data, transaction integrity, customer, regulatory and operational consequences. The exercise suggests $10–15M likely loss; this is a scenario estimate, not verified analysis. |
| Existing safeguards | Limited/unverified | CDE location is stated; no database activity monitoring, MFA, individual accountability or rotation evidence is supplied. |
| Residual risk | Unknown until safeguards are tested | No treatment effectiveness evidence exists. |

## Options considered

| Option | Cost/timeline from scenario | Result |
|---|---|---|
| Replace system | $800K–$1.2M; 12–18 months | Preferred long-term solution. |
| Partial remediation | $150K; 3 months | Adds monitoring, reduced access, IP restriction and rotation. |
| Accept current state | No direct cost | Not recommended; leaves high, poorly detectable risk. |
| Conditional interim acceptance | $20K plus staff time; 2 weeks | Recommended only if safeguards and replacement commitment are evidenced. |

## Conditions for a pending acceptance

1. Rotate the shared password immediately and quarterly thereafter.
2. Reduce password knowledge to named minimum personnel and retain an access register.
3. Implement IP restrictions and database activity monitoring.
4. Fund and initiate the replacement plan in FY2027.
5. Review in six months and immediately after any access, logging, incident or budget-condition failure.

## Approval status

This is a decision memorandum and pending request. It is **not** a signed acceptance, security approval, or statement that the risk is tolerable. The CFO must make and record the business decision.
