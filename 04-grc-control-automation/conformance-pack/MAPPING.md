# CIS AWS Foundations baseline mapping

This is a small, deployable CIS AWS Foundations-aligned baseline. It is not a claim of full CIS certification.

| Config rule | CIS intent | ISO 27001:2022 | SOC 2 |
|---|---|---|---|
| Root MFA enabled | Protect root access | A.5.17, A.8.5 | CC6.1, CC6.2 |
| IAM user MFA enabled | Strong user authentication | A.5.17, A.8.5 | CC6.1 |
| Access keys rotated | Credential lifecycle management | A.5.17 | CC6.2 |
| S3 public read prohibited | Restrict data exposure | A.8.3, A.8.12 | CC6.6, CC6.7 |
| S3 public write prohibited | Prevent unauthorized data change | A.8.3, A.8.12 | CC6.6, CC7.2 |
