# SOC 2 Readiness Conclusion — CloudNative Analytics

**Scope:** Security, Availability and Confidentiality; educational readiness review, not an AICPA attestation.

CloudNative is an 85-person remote AWS SaaS provider processing enterprise customer data in `eu-west-1`. The review selected governance, access, monitoring, change, incident, availability, confidentiality and vendor-risk points of focus relevant to the AWS/managed-laptop environment.

## Conclusion

The organization is **not ready to support an operating-effectiveness SOC 2 conclusion from the supplied scenario**. The scenario identifies the intended environment and six material risks, but does not provide evidence of AWS IAM review, endpoint posture, logging, incident exercises, change approvals, backup/recovery tests, supplier review, or data lifecycle operation.

| Priority | Readiness action | Evidence to obtain |
|---|---|---|
| P1 | AWS IAM, privileged-access and CDE/customer-data access governance | IAM exports, MFA settings, access reviews, approvals. |
| P1 | AWS configuration/change monitoring | CloudTrail/configuration history, alerting and change tickets. |
| P1 | Incident and continuity validation | Incident plan, exercise, recovery and customer communication records. |
| P2 | AWS supplier and confidentiality governance | AWS assurance review, contracts, data retention/deletion records. |

All CISO Assistant SOC 2 entries retain `Not assessed`; Done refers to the readiness review, not control effectiveness.
