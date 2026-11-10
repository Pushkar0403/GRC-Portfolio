# TalentMatch EU AI Act / NIST AI RMF / ISO 42001 crosswalk

Assessment `6916bc7d-9aaa-4d1a-be0e-127b02b522fe`; educational case study; 10 November 2026. This crosswalk adds traceability only. The EU AI Act is legislation, NIST AI RMF 1.0 is voluntary, and ISO/IEC 42001:2023 is an AI management-system standard. A mapping is not evidence of legal compliance, certification, or effective control operation.

NIST baseline: AI RMF 1.0. NIST states a revision is in progress; no finalized replacement was used. ISO identifiers below were verified from the newly installed CISO Assistant ISO 42001 library. **D** = direct shared objective, **P** = partial, **S** = supporting only.

| EU Article | Existing finding/result | NIST AI RMF 1.0 | ISO 42001:2023 | map, evidence, risk/treatment |
|---|---|---|---|---|
| 6 | Employment ranking is Annex III 4(a) high-risk; formal provider classification record unavailable / Not assessed | GOVERN 1.1; MAP 1.1; MAP 2.1 | 4, 6, 8 | D; classification/intended-use record; AI-R003/R004; PROP-AI-R003/R004. Neither framework decides the legal classification. |
| 9 | Seven risks exist; lifecycle process effectiveness unverified / Not assessed | GOVERN 1.3, 1.4; MAP 5.1; MEASURE 1.1; MANAGE 1.2, 1.3 | 6, 8, 9, 10 | D; risk register, reviews, test reports; AI-R001–R007; all PROP controls. |
| 10 | Historic labels/proxies known; representativeness and subgroup testing absent / Partially compliant | GOVERN 1.6; MAP 2.3; MEASURE 1.1, 1.2 | 6, 8, 9; A.6.2.3 | D; lineage, data sheet, subgroup selection/error/calibration results; R001/R002/R004/R007; PROP-R001/R002/R004/R007. |
| 11 | Required technical documentation/version evidence absent / Not assessed | GOVERN 1.6; MAP 1.1, 1.6; MEASURE 2.7 | 7, 8, 9; A.6.2.3 | P; model card, design/version/change record; R007; PROP-R007. |
| 12 | Decision, override and monitoring logs not evidenced / Not assessed | GOVERN 1.6; MEASURE 2.5; MANAGE 2.2 | 7, 8, 9 | P; schema, retention and access evidence; R003/R005/R006/R007; PROP-R003/R005/R006/R007. |
| 13 | SHAP exists, but deployer instructions and usable explanations unverified / Partially compliant | MAP 1.1, 2.2; GOVERN 1.6 | 7, 8 | P; instructions, limits and explanation usability test; R003/R005; PROP-R003/R005. |
| 14 | Final recruiter decision stated; top-20 focus, 45 seconds and override effectiveness unverified / Partially compliant | MAP 2.2; MEASURE 2.5; MANAGE 1.1 | 7, 8, 9 | D; review protocol, lower-ranked sampling, override/training records; R003; PROP-R003. |
| 15 | 78% human agreement is not demonstrated validity/fairness/security evidence / Partially compliant | MEASURE 1.1, 2.1, 2.5; MANAGE 2.2 | 6, 8, 9 | D; calibration, error, robustness and security results; R001/R002/R004/R006/R007; PROP-R001/R002/R004/R006/R007. |
| 16 | Provider obligations process not evidenced / Not assessed | GOVERN 1.1, 1.4; MANAGE 1.1 | 5, 6, 8 | P; accountability/release-gate records; R007; PROP-R007. |
| 17 | No demonstrated quality/AIMS process / Not assessed | GOVERN 1.4, 1.5; MANAGE 3.2 | 4–10 | P; policy, objectives, audit/review/CAPA records; R007; PROP-R007. |
| 18 | Documentation retention not evidenced / Not assessed | GOVERN 1.6; MEASURE 2.5 | 7.5, 8 | P; retention schedule/archive evidence; R007; PROP-R007. |
| 19 | Automated logging/retention unverified / Not assessed | MEASURE 2.5; MANAGE 2.2 | 8, 9 | P; log configuration/test; R003/R005/R006/R007; PROP-R003/R005/R006/R007. |
| 20 | Corrective action/cooperation process absent / Not assessed | MANAGE 2.2, 3.1; GOVERN 1.5 | 9, 10 | P; incident/CAPA procedure and exercise; R007; PROP-R007. |
| 27 | Private-provider scenario does not establish statutory FRIA trigger / Not applicable | MAP 5.1, 5.2 | 4, 6, 8 | S; voluntary rights-impact record remains good governance; R001–R005; PROP-R001–R005. |
| 43 | Conformity-assessment evidence absent; future readiness issue / Not assessed | GOVERN 1.1; MANAGE 1.1 | 8, 9 | P; technical file/QMS/test pack; R007; PROP-R007. |
| 61 | Post-market monitoring plan/evidence absent / Not assessed | GOVERN 1.5; MEASURE 2.1, 2.5; MANAGE 3.2 | 8, 9, 10 | D; drift/fairness monitoring/review; R001/R002/R004/R007; PROP-R001/R002/R004/R007. |
| 72 | Serious-incident process absent / Not assessed | MANAGE 2.2, 3.2; GOVERN 1.5 | 8, 10 | P; triage/escalation/exercise; R006/R007; PROP-R006/R007. |
| 73 | Corrective-action evidence absent / Not assessed | MANAGE 2.2, 3.2 | 10 | D; CAPA register/owner/effectiveness review; R007; PROP-R007. |
| 86 | SHAP alone is not candidate explanation or recourse / Not assessed | MAP 2.2; MEASURE 2.5; GOVERN 1.6 | 7, 8, 9 | P; notice, explanation/appeal workflow and QA; R005; PROP-R005. |

Limitations: legal duties not captured by voluntary/management-system frameworks remain independent; the crosswalk does not alter the Article 27 reasoning, results, risk ratings, or To-do status of treatments.
