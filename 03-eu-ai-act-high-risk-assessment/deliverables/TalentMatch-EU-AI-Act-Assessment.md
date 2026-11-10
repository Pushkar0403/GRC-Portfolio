# EU AI Act High-Risk Assessment — TalentMatch AI

Assessment date: 10 November 2026. This is an educational case study based only on the supplied scenario; it is not legal advice, a certification, a regulator review, or a live-system audit.

## Executive decision

**Do not approve deployment until remediation is objectively verified.** This is a governance decision, not a legal prohibition. TalentMatch scores, ranks and highlights candidates for recruitment, materially shaping access to employment. The supplied facts support serious bias, proxy-discrimination, oversight, performance, transparency and data-security risks.

## System and role scope

TalentMatch, headquartered in Amsterdam, is the provider of a SaaS used by more than 150 enterprise customers. It ingests job descriptions and resumes; transformer NLP extracts information; XGBoost assigns a 0–100 fit score; a ranking engine highlights the top 20. About 5 million historical applications with hiring outcomes train the model. Features include skills, experience, education, job titles and company names. Recruiter customers are deployers and formally decide; candidates are affected persons. SHAP is said to be available for individual scores. No scenario evidence establishes bias testing, version control, logs, override analysis, candidate appeals or operational security controls.

## Legal position and classification

Legal source: Regulation (EU) 2024/1689 consolidated on 27 July 2026, including the 2026 Omnibus amendment: https://eur-lex.europa.eu/eli/reg/2024/1689. The Commission identifies CV-sorting recruitment tools as high-risk: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai.

The system is high-risk under Article 6(2) and Annex III, section 4(a): it analyses/filters applications and evaluates candidates. Article 6(3) does not apply on the facts. Scoring and ranking profile natural persons and materially influence interview access; rare review beyond the top 20 means human final decision-making does not neutralise that influence. Removing names/photos does not remove proxy variables. Article 6(3) is a classification mechanism, not an independent violation.

| Timing | Conclusion |
|---|---|
| 10 Nov 2026 | The Act is in force and GDPR remains applicable. Missing high-risk evidence is not, by itself, a current Annex III breach. |
| From 2 Dec 2027 | Articles 9–26 high-risk requirements, provider lifecycle duties and pre-market readiness apply to Annex III systems. |
| Governance recommendations | Voluntary FRIA, fairness testing, meaningful oversight and candidate recourse are required deployment safeguards in this assessment; not every item is an independent current legal duty. |

Article 27 is not triggered by the established facts: TalentMatch is a private provider and no customer is shown to be a public body or private provider of public services. A voluntary fundamental-rights analysis is nevertheless completed. Article 86 and GDPR require provider/deployer contractual role allocation and legal review.

## Requirements and gaps

| Requirement | Role | Result | Finding and evidence needed |
|---|---|---|---|
| Articles 9, 11, 12, 16–20, 43, 61, 72–73 | Provider | Not assessed | No lifecycle risk management, technical file, logs, QMS, conformity, corrective-action or monitoring evidence. |
| Article 10 | Provider | Partially compliant | Historical outcomes and proxy-capable features are known; no provenance, representativeness, subgroup, proxy or bias-test evidence. |
| Article 13 | Provider | Partially compliant | SHAP availability is stated; no tested instructions on intended use, limitations, top-20 effects or oversight. |
| Article 14 | Provider/deployer support | Partially compliant | Top-20 emphasis, rare review outside it and 45-second decisions show only partially meaningful oversight. |
| Article 15 | Provider | Partially compliant | 78% human agreement does not demonstrate job-fit validity, calibration, fairness, subgroup error, robustness or cybersecurity. |
| Article 26 | Deployer | Outside provider scope | Customers need usable instructions, oversight and monitoring support. |
| Article 27 | Deployer | Not applicable | No statutory trigger established; voluntary rights assessment performed. |
| Article 86 | Deployer/provider instructions | Not assessed | No candidate explanation, notice, appeal or allocation evidence. |

## Fundamental rights, bias and oversight

Equal treatment, access to employment, privacy, dignity and effective remedy are materially affected. Education, university, employers, job titles, career gaps and geography can proxy protected characteristics or socioeconomic disadvantage. Historic hiring labels may encode earlier discrimination. Deleting names/photos is not a fairness test. The 78% agreement statistic can reproduce human bias; SHAP explains contributions but does not prove fairness or comprehension.

Required tests: data provenance and representativeness; lawful subgroup and proxy analysis; selection-rate, false-negative and calibration analysis; intersectional review where lawful; independent validation; drift monitoring; accessibility review. No outcomes were supplied.

Oversight is partially meaningful in design but unverified in operation. Require review beyond top 20, reason-recorded override, lower-rank explanations, uncertainty display, recruiter training, override/outside-top-20 metrics, appeal/escalation and accountability logs.

## CISO risk register

Matrix: 5x5 ISO-27005. Scores are inherent/current estimates; no residual score, risk acceptance, effective safeguard or formal owner approval is recorded.

| Risk | CISO ID | Level | Proposed treatment |
|---|---|---|---|
| AI-R001 Historical hiring bias | edc3d433-21e0-43f7-b973-9a163301e0a6 | Very high | Dataset fairness testing |
| AI-R002 Proxy discrimination | 3e5215ba-f7f6-4727-a82e-fb377172e686 | High | Proxy-feature assessment |
| AI-R003 Top-20 automation bias | ee410c29-aec2-47e4-b5d8-ae8987beefdf | Very high | Meaningful oversight |
| AI-R004 Inaccurate scoring | 7fb0e9a2-afc5-4e8a-872b-80394b73ebfe | High | Performance validation |
| AI-R005 Explanation/recourse gap | 7e2055ca-3af2-41f3-a885-129fd690a536 | High | Explanation and appeal |
| AI-R006 Applicant-data exposure | 2ede2fef-2467-4abc-8f3c-dfb0ba5d763a | High | Data security |
| AI-R007 Drift/lifecycle weakness | fc320cc4-d1aa-435f-8265-ceb975c24b9d | High | Monitoring and governance |

Seven CISO controls are To do and linked to their risks and relevant selected obligations. They are proposed controls only; management ownership and approval are pending.

## Evidence index and roadmap

1. Data sheets, provenance, lawful-use/retention evidence, subgroup and proxy testing.
2. Validation: job-fit performance, calibration, false-negative, robustness and security results.
3. Technical documentation, model/version/change register, rank/score/override audit logs.
4. Deployer instruction, oversight training, candidate notice, explanation, appeal and complaint records.
5. QMS, post-market monitoring, drift, incident and corrective-action procedures.

Approval requires independently reviewed fairness and performance results; a redesigned and measured oversight workflow; complete documentation/logging; verified security controls; and provider/deployer lifecycle arrangements ready for the 2 December 2027 deadline.

## Auditor challenges and walkthrough

- Humans decide: the top-20 shortlist still shapes who receives consideration.
- No protected fields: proxy pathways and historic labels can still discriminate.
- SHAP: it does not prove accuracy, fairness, candidate remedy or recruiter comprehension.
- Prohibition: none is established; the recommendation is conditional non-deployment.

Five-minute walkthrough: describe lifecycle and affected candidates; classify under Article 6/Annex III; distinguish current and 2027 duties; explain bias and top-20 risk; explain limits of 78%/SHAP; show seven risks and To do treatments; conclude with objective approval conditions.

## Complementary governance crosswalk

The [EU AI Act / NIST AI RMF / ISO 42001 crosswalk](EU-AI-Act-NIST-ISO42001-Crosswalk.md) connects the 19 scoped legal records to the voluntary NIST AI RMF 1.0 and ISO/IEC 42001:2023 AIMS requirements. It does not make a NIST or ISO compliance claim: the EU AI Act remains the legal assessment, NIST provides risk-management outcomes, and ISO 42001 provides a management-system model. The related risk mapping and governance-gap analysis preserve all seven proposed controls as **To do** and preserve the non-approval deployment recommendation.
