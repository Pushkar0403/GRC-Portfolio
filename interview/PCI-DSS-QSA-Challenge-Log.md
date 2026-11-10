# PCI DSS QSA Challenge Log — MidTech Retail Solutions

| Challenge | Current answer | Required closure evidence |
|---|---|---|
| “Prove corporate systems cannot reach the CDE.” | The architecture alone cannot prove this. Shared AD and a jump host can affect CDE security. | Approved firewall rules, flow evidence and segmentation-test results. |
| “Why is the management SIEM out of scope?” | It is not defensibly out of scope until log content, access and security impact are assessed. | Log samples, PAN masking proof, access records and route validation. |
| “Why is backup infrastructure out of scope?” | It is not defensibly out of scope if CDE backups contain CHD. | Backup inventory, encryption, restore path and retention evidence. |
| “How is CDE access administered?” | Jump-host use is claimed; MFA, hardening, session logging and least privilege are unverified. | Jump-host configuration, access approvals and session records. |

No penetration or segmentation test was performed by this educational review. MidTech must not use this document as proof of PCI DSS compliance.
