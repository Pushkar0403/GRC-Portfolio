# GRC control automation

This project turns manual AWS checks into repeatable evidence, detection, prevention, and safe remediation. It follows the project scenario's core idea: automation produces current evidence and highlights exceptions; people still decide whether an access or business exception is appropriate.

## What is included

1. `scripts/check_s3_public_access.py` checks each S3 bucket's four bucket-level Block Public Access settings and writes JSON evidence.
2. `scripts/export_iam_inventory.py` exports IAM users, MFA state, and access-key age to JSON and CSV.
3. `terraform/config-recorder` creates the S3-only AWS Config recorder and protected evidence-delivery bucket. Deploy it before any Config rules.
4. `terraform/config-rules` deploys the AWS managed S3 public-read rule and a custom Lambda rule for the four Block Public Access settings.
5. `terraform/ssm-remediation` deploys an SSM Automation document. Its default is `DryRun=true`; it changes a bucket only when explicitly run with `DryRun=false`.
6. `conformance-pack` contains a small CIS AWS Foundations-aligned Config baseline and its ISO 27001/SOC 2 mapping. `terraform/conformance-pack` keeps deployment off by default.
7. `modules/secure_s3_bucket` creates an encrypted, versioned S3 bucket with all public access blocked.
8. `REVIEW.md` explains each part and how to verify it.

## Local checks

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
terraform -chdir=terraform/config-rules init -backend=false
terraform -chdir=terraform/config-rules validate
```

Run the AWS steps in `REVIEW.md` only when ready. The Python evidence scripts are read-only. AWS Config rules and conformance packs can incur AWS charges. Generated evidence, Terraform state, and credentials are ignored by Git.

## Safety

Do not put credentials in this repository. Use your normal AWS CLI profile or an IAM role. All demonstration resources use the `grc-demo-` prefix. Run `terraform destroy` in the same folder after each Terraform test when you no longer need the resource.
