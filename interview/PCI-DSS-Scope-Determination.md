# PCI DSS Scope Determination — MidTech Retail Solutions

**Assessment date:** 10 November 2026  
**Assessor:** Educational case-study assessor  
**Version:** 1.0

## Executive summary

The CDE is not limited to subnet `10.3.0.0/24`. It includes the payment application (`10.3.0.10`), card database (`10.3.0.20`), HSM (`10.3.0.30`), tokenization service (`10.3.0.40`) and CDE log collector (`10.3.0.50`). Systems outside that subnet which connect to, administer, authenticate, back up, patch, log or can otherwise affect CDE security must remain in scope unless segmentation is evidenced and tested. Overall risk: **High**.

| Finding | Why it matters |
|---|---|
| Shared AD and jump host | Compromise can create a route into the CDE. |
| Backup/SIEM/WSUS outside CDE | May store CHD or alter CDE security. |
| Segmentation claim unproven | Architecture diagram is not firewall-rule or test evidence. |

## CDE and connected systems

| System | Role / data | Scope conclusion |
|---|---|---|
| Web servers / load balancer | Receive HTTPS payment traffic; transmit PAN to payment application | In scope pending proof that PAN cannot persist or traverse unapproved paths. |
| Payment application | Processes PAN | CDE. |
| Card database | Stores CHD | CDE. |
| HSM | Protects payment cryptographic operations | CDE/security-impacting. |
| Tokenization service | Processes/transforms payment data | CDE. |
| CDE log collector | Receives payment-system logs; PAN content unknown | In scope pending log-content review. |
| AD domain controllers | Authentication dependency | In scope as security-impacting. |
| Jump host | Administrative path to CDE | In scope as security-impacting. |
| SIEM, backup server, WSUS | Log, backup and patch paths | In scope unless CHD absence and inability to affect CDE are evidenced. |

## Trust and segmentation analysis

| Dependency | Risk | Evidence required | Recommendation |
|---|---|---|---|
| AD | Corporate compromise may yield CDE credentials | CDE authentication design and AD privilege paths | Isolate CDE identities; restrict trust and privileged administration. |
| Jump host | Single compromise point for CDE administration | MFA, hardening, session logs, permitted routes | Use a dedicated hardened administration tier. |
| Logging | SIEM may receive PAN or affect evidence | Log samples, masking and routing rules | Verify no PAN; otherwise keep all log chain in scope. |
| Backups | Backups may contain CHD | Backup inventory, encryption, access and restore paths | Treat backup chain as CDE until proven otherwise. |
| Patching/DNS | Shared management can alter CDE availability/security | Firewall rules and management access records | Segment management services and allow-list required flows. |

## QSA challenge preparation

| QSA question | Defensible answer today | Evidence still needed |
|---|---|---|
| “Show me systems excluded from scope.” | No exclusion is defensible for shared AD, jump host, SIEM, backup or WSUS from architecture alone. | Rulesets, flow inventory, system hardening and segmentation tests. |
| “Can corporate AD affect CDE?” | Yes, if CDE authentication or privileged access relies on it. | AD/CDE trust and privilege analysis. |
| “Are logs and backups in scope?” | They are potentially in scope until CHD content and security impact are assessed. | Log samples, backup catalogue and restore testing. |

## Remediation roadmap

1. **0–30 days:** inventory all CHD flows; review firewall rules; classify log and backup contents; restrict jump-host paths.
2. **30–90 days:** create dedicated CDE identity/administration controls; segment shared services; document allowed flows.
3. **90+ days:** perform and retain independent segmentation validation after material changes.

No technical segmentation test was performed in this educational assessment. Residual risk remains high until evidence proves that non-CDE systems cannot access or affect the CDE.
