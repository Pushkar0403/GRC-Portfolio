# TalentMatch AI risk cross-framework mapping

Risk assessment `eb7da7ff-16a4-44c1-99e3-8057885399f8`. The ratings are existing 5x5 ISO-27005 current ratings; they were not recalculated. Residual risk is unknown. Each PROP control is **To do**, with no evidenced effectiveness or approval.

| Risk/rating | EU AI Act | NIST AI RMF | ISO 42001 | treatment, verification and gap |
|---|---|---|---|---|
| AI-R001 Historical hiring bias / Very high | 9,10,15,61 | GOVERN 1.2,1.6; MAP 5.1; MEASURE 1.1,1.2; MANAGE 1.2 | 6,8,9 | PROP-AI-R001; provenance, subgroup selection-rate/error/calibration testing and independent review. No outcome data evidence. |
| AI-R002 Proxy discrimination / High | 10,15,61 | MAP 2.3,5.1; MEASURE 1.1,1.2; MANAGE 1.3 | 6,8,9 | PROP-AI-R002; feature inventory/effect tests for education, employer, geography and career gaps. No proxy analysis supplied. |
| AI-R003 Top-20 automation bias / Very high | 9,12–14,19 | MAP 2.2; MEASURE 2.5; MANAGE 1.1,1.3 | 7,8,9 | PROP-AI-R003; override/lower-rank review logs, training, escalation and effectiveness tests. Override capability is not proven use. |
| AI-R004 Inaccurate scoring / High | 9,10,15,61 | MAP 1.1; MEASURE 1.1,2.1; MANAGE 1.2 | 6,8,9 | PROP-AI-R004; outcome labels, calibration/threshold and subgroup error report. 78% agreement is insufficient. |
| AI-R005 Explanation/recourse / High | 12,13,19,86 | GOVERN 1.6; MAP 2.2; MEASURE 2.5 | 7,8,9 | PROP-AI-R005; candidate notice, explanation UX/appeal records and samples. SHAP is not demonstrated comprehension. |
| AI-R006 Applicant-data exposure / High | 12,15,72 | GOVERN 1.1,1.6; MEASURE 2.5; MANAGE 2.2 | 6,7,8,9 | PROP-AI-R006; access/security testing, log and incident evidence. No effective safeguard asserted. |
| AI-R007 Drift/lifecycle governance / High | 9,11,16–20,43,61,72,73 | GOVERN 1.4–1.6; MEASURE 2.1,2.5; MANAGE 2.2,3.2 | 4–10; A.6.2.3 | PROP-AI-R007; version registry, monitoring, incident/CAPA/review records. No residual score/approval. |

NIST outcomes guide voluntary practice; ISO clauses organize an AIMS. Neither proves EU legal compliance.
