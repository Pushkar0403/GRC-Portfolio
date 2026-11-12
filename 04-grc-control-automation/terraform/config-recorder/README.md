# AWS Config S3-only recorder

This module establishes the shared AWS Config recording foundation for the `grc-demo` S3 compliance exercise. It is intentionally separate from `../config-rules`: enable recording first, then deploy Config rules. Neither module references the other, so there is no Terraform dependency cycle.

## Resources and design

- An AWS Config recorder using `INCLUSION_BY_RESOURCE_TYPES` for only `AWS::S3::Bucket`. It does not record all supported resources or global IAM resource types.
- A delivery channel writing to a dedicated `grc-demo-config-evidence-<account-id>-us-east-1` bucket under `aws-config/`.
- The evidence bucket has versioning, AES-256 server-side encryption, all four S3 Block Public Access settings, an HTTPS-only deny policy, and policy permissions limited to the AWS Config service from this account and Region.
- An AWS Config service role with the AWS-managed `AWS_ConfigRole` policy, required for recording. The bucket policy is separate because AWS Config delivers evidence directly.

`prevent_destroy = true` and `force_destroy = false` are deliberate: normal `terraform destroy` will not delete the evidence bucket or its contents.

## Costs and controls

AWS Config charges for configuration-item recording and delivered/snapshotted data, and S3 charges for stored/versioned evidence. Costs depend on AWS pricing, retained evidence, and configuration changes. This demo controls cost by recording just one resource type, omitting SNS notifications and conformance packs, and using a dedicated bucket. Review current regional pricing before deployment and delete only sanitized, no-longer-required evidence under an approved retention process.

## Deployment sequence

Authenticate using the existing SSO profile first:

```powershell
aws sso login --profile grc-lab
terraform -chdir=terraform/config-recorder init
terraform -chdir=terraform/config-recorder plan
```

Review the plan, then apply this module only when approved. Once the recorder status is enabled, deploy `../config-rules` in a separate state/workflow. Do not deploy the conformance pack for this demonstration.

Terraform uses the `grc-lab` profile by default; override only with `-var 'aws_profile=<approved-profile>'`. It never stores credentials in source.

## Read-only verification

```powershell
aws configservice describe-configuration-recorders --profile grc-lab --region us-east-1
aws configservice describe-configuration-recorder-status --profile grc-lab --region us-east-1
aws configservice describe-delivery-channels --profile grc-lab --region us-east-1
aws s3api get-public-access-block --bucket <evidence-bucket-name> --profile grc-lab
aws s3api get-bucket-encryption --bucket <evidence-bucket-name> --profile grc-lab
aws s3api get-bucket-versioning --bucket <evidence-bucket-name> --profile grc-lab
```

## Stop recording and cleanup

To stop recording without deleting evidence, run:

```powershell
aws configservice stop-configuration-recorder --configuration-recorder-name grc-demo-s3-only --profile grc-lab --region us-east-1
```

For lab cleanup, first stop recording and preserve a sanitized export of evidence according to the retention decision. Then remove the Config rules before recorder infrastructure. `terraform destroy` will intentionally fail at the protected evidence bucket. After explicit approval to remove evidence, remove `prevent_destroy` in this module, run a reviewed plan, empty all object versions and delete markers with an approved process, and then destroy. Deleting audit evidence can invalidate investigations, retention obligations, and the ability to prove control operation; never make it an automatic cleanup step.
