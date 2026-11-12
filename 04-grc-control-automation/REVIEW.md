# Review and test sheet

Use PowerShell from this folder. No credentials belong in project files. The commands use the AWS identity already configured on your machine.

## 1. S3 Block Public Access evidence

Runs a read-only bucket-level check and writes JSON proof.

```powershell
python scripts\check_s3_public_access.py
Get-Content evidence\s3_public_access_report.json
```

Good result: every finding says `COMPLIANT`; exit code `0`. A `NON_COMPLIANT` bucket is a real finding, not a script failure. Cost and cleanup: none.

## 2. IAM inventory evidence

Exports one row per IAM user/access key, including MFA state and key age. It is read-only.

```powershell
python scripts\export_iam_inventory.py
Get-Content evidence\iam_inventory.csv
```

Good result: JSON and CSV files exist and contain users visible to your identity. Cost and cleanup: none.

## 3. AWS Config rules

Requires AWS Config recording to already be enabled in the chosen region. Deploys the managed `S3_BUCKET_PUBLIC_READ_PROHIBITED` rule and a custom Lambda rule that requires all four Block Public Access settings.

```powershell
terraform -chdir=terraform\config-rules init
terraform -chdir=terraform\config-rules plan
terraform -chdir=terraform\config-rules apply
```

Good result: two Config rules named `grc-demo-*` appear. **Cost:** AWS Config configuration-item recording and rule evaluations, plus small Lambda/logging charges. Cleanup:

```powershell
terraform -chdir=terraform\config-rules destroy
```

## 4. SSM remediation

Creates only an SSM Automation document. A dry run does not change the bucket.

```powershell
terraform -chdir=terraform\ssm-remediation init
terraform -chdir=terraform\ssm-remediation apply
aws ssm start-automation-execution --document-name grc-demo-reapply-s3-public-access-block --parameters BucketName=YOUR_EXISTING_TEST_BUCKET,DryRun=true
```

Good result: the execution output says `WOULD_REMEDIATE`. To actually fix a test bucket only, rerun the last command with `DryRun=false` after reviewing it. **Cost:** normally no material cost for the document; Automation execution and API activity may be billed. Cleanup:

```powershell
terraform -chdir=terraform\ssm-remediation destroy
```

## 5. CIS-aligned conformance pack

The pack maps root MFA, IAM-user MFA, key rotation, and S3 public read/write protection to ISO 27001 and SOC 2. See `conformance-pack/MAPPING.md`.

```powershell
terraform -chdir=terraform\conformance-pack init
terraform -chdir=terraform\conformance-pack apply -var="deploy_conformance_pack=true"
```

Good result: `grc-demo-cis-foundations-mapped` appears under AWS Config conformance packs. **Cost:** AWS Config recording and rule evaluations. Cleanup:

```powershell
terraform -chdir=terraform\conformance-pack destroy -var="deploy_conformance_pack=true"
```

## 6. Secure-by-default S3 Terraform module

Creates a test bucket with encryption, versioning, and all public access blocked. Use a globally unique name.

```powershell
$bucket = "grc-demo-secure-s3-$((Get-Random -Minimum 100000 -Maximum 999999))"
terraform -chdir=examples\secure_s3_bucket init
terraform -chdir=examples\secure_s3_bucket apply -var="bucket_name=$bucket"
aws s3api get-public-access-block --bucket $bucket
aws s3api get-bucket-versioning --bucket $bucket
```

Good result: all four public-access values are `true` and versioning is `Enabled`. **Cost:** S3 storage/API requests; an empty bucket is normally negligible. Cleanup:

```powershell
terraform -chdir=examples\secure_s3_bucket destroy -var="bucket_name=$bucket"
```

## 7. Control coverage

Detect: scripts and Config rules identify public S3 exposure and IAM credential gaps. Prevent: the Terraform module builds hardened S3 buckets. Fix: the SSM document restores S3 Block Public Access only after a dry run is deliberately changed to `false`.
