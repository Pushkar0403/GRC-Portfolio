# ISO/IEC 27001:2022 Statement of Applicability

**Organization:** CloudNative Analytics Ltd.  
**Scope:** Design, development, operation and support of the B2B SaaS analytics platform, supporting company-managed remote endpoints, and AWS services in eu-west-1. Customer-managed environments, AWS physical facilities, and non-existent company offices/data centres are outside scope.  
**Version/date:** 1.0 / 2026-11-10  
**Assessment basis:** Educational case scenario only. This is an applicability and evidence-readiness assessment, not a certification audit or an operating-effectiveness conclusion.

## Decision summary

| Theme | Total | Applicable | Excluded | Result: Not assessed | Result: N/A |
|---|---:|---:|---:|---:|---:|
| A.5 Organisational | 37 | 37 | 0 | 37 | 0 |
| A.6 People | 8 | 8 | 0 | 8 | 0 |
| A.7 Physical | 14 | 5 | 9 | 5 | 9 |
| A.8 Technological | 34 | 33 | 1 | 33 | 1 |
| **Total** | **93** | **83** | **10** | **83** | **10** |

All selected controls are **Not assessed**, rather than compliant, because the scenario supplies no policy, system configuration, contract, log, training, or test evidence. Each detailed, requirement-specific CISO Assistant observation records the applicable risk and needed evidence.

## Exclusions and alternative measures

| Control(s) | Reason | Alternative / boundary | Re-evaluate when |
|---|---|---|---|
| A.7.1–A.7.6 | No company-operated office, data centre, secure area, or physical perimeter exists. | AWS is responsible for its data-centre physical environment; company risk is addressed through endpoint, remote-working and access controls. | Office, data centre, or controlled secure area is opened. |
| A.7.8 | No on-premises equipment is sited in a company facility. | Company-managed laptops remain covered by A.7.9 and A.8.1. | Equipment is installed in a company facility. |
| A.7.11 | Cloud infrastructure utilities are not operated by CloudNative. | AWS shared-responsibility due diligence, cloud-service security and continuity controls remain applicable. | The company operates a facility or supporting utilities. |
| A.7.12 | No company-managed facility cabling exists. | Network security is addressed by the cloud architecture and A.8.20–A.8.22. | A company facility or managed cabling is introduced. |
| A.8.30 | The scenario says all product development is internal; no external development vendor is used. | A.8.25–A.8.29 and A.8.31–A.8.33 govern internal development. | Any supplier develops, maintains, or materially changes product code. |

## Risk-to-control traceability

| Risk | Principal controls |
|---|---|
| R-001 Unauthorized customer-data access | A.5.15–A.5.18, A.5.23, A.5.34, A.6.6–A.6.8, A.8.1–A.8.5, A.8.12, A.8.15–A.8.16, A.8.24 |
| R-002 Laptop theft/loss | A.5.9–A.5.11, A.6.7, A.7.7, A.7.9–A.7.10, A.7.13–A.7.14, A.8.1, A.8.7, A.8.10, A.8.24 |
| R-003 Cloud misconfiguration | A.5.8–A.5.9, A.5.23, A.8.2–A.8.3, A.8.8–A.8.9, A.8.15–A.8.16, A.8.20–A.8.22, A.8.31–A.8.32 |
| R-004 Insider threat | A.5.2–A.5.4, A.5.15–A.5.18, A.6.1–A.6.6, A.8.2–A.8.5, A.8.15–A.8.16 |
| R-005 AWS supplier breach | A.5.19–A.5.23, A.5.29–A.5.31, A.8.13–A.8.14, A.8.20–A.8.24 |
| R-006 Business-continuity failure | A.5.24–A.5.30, A.7.11 (excluded by boundary), A.8.6, A.8.13–A.8.17 |

## Evidence index and remediation plan

| Priority | Evidence / action needed | Controls principally affected |
|---|---|---|
| P1 | Approved ISMS policies, asset inventory, data classification and access-control standard; identify owners and approval dates. | A.5.1–A.5.18, A.5.31–A.5.37 |
| P1 | AWS architecture, IAM/MFA configuration, CloudTrail/log retention, security groups, encryption/KMS and backup/restore evidence. | A.5.23, A.8.1–A.8.24 |
| P1 | Secure SDLC, code review, CI/CD separation, change approvals, test evidence and test-data handling records. | A.5.8, A.8.25–A.8.34 |
| P1 | Incident plan, event-reporting channel, exercise records, continuity plan, recovery objectives and restore/failover test records. | A.5.24–A.5.30, A.6.8, A.8.13–A.8.17 |
| P2 | HR screening/terms/NDA/training/offboarding evidence and endpoint-management/laptop disposal records. | A.6.1–A.6.8, A.7.7, A.7.9–A.7.10, A.7.13–A.7.14 |
| P2 | AWS due diligence, shared-responsibility analysis, supplier security clauses and periodic-review record. | A.5.19–A.5.23 |

## Auditor challenge preparation

| Challenge | Response |
|---|---|
| “Employees work at home; why exclude physical perimeter?” | Home offices are not company-operated facilities. The assessment does not claim home premises are risk-free: the relevant risks are covered by applicable endpoint, remote-working, screen-lock, media and access controls. |
| “AWS has physical data centres; why exclude A.7.1–A.7.6?” | The scope does not include operating AWS facilities. The physical security obligation is managed through AWS supplier and cloud-service governance; this does not remove the need to evaluate that supplier relationship. |
| “Why exclude utilities and cabling?” | CloudNative operates neither data-centre utilities nor facility cabling. Availability and network risks remain selected through AWS service due diligence, architecture, backup, redundancy and network controls. |
| “Could internal developers be ‘outsourced’ through contractors?” | The exclusion relies on the stated scenario. It must be reversed before any external party writes, maintains or changes product code, including a contractor under CloudNative direction. |
| “Where is your proof of the exclusions?” | The scenario is the present basis; certification readiness requires the remote-first HR policy, asset register confirming no physical servers, AWS billing/architecture records, and procurement/vendor records to be retained as evidence. |

## Limitation

No approval is recorded. No live-system testing, interviews, or evidence inspection was performed. The next assessment step is evidence collection and control design/operating-effectiveness evaluation, not automatic conversion to compliant.
