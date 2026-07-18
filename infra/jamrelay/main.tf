# Jam-parcel relay: the postmaster Lambda + its function URL.
#
# The bucket itself is NOT managed here (the spike created it by hand;
# see README.md for what a bucket must have). Cutover to a company AWS
# account = change the profile/bucket variables and re-apply; the app
# only ever knows the function URL.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region  = var.region
  profile = var.profile

  default_tags {
    tags = {
      ManagedBy     = "Terraform"
      Project       = "jamrelay"
      TerraformRepo = "github.com/TeamVapor/vapor.engineering"
    }
  }
}

variable "profile" {
  description = "AWS CLI profile (dev: Eli's personal 'terraform'; later: the company account's)"
  type        = string
  default     = "terraform"
}

variable "region" {
  type    = string
  default = "us-west-2"
}

variable "bucket_name" {
  description = "Relay bucket (must exist, with 30-day lifecycle + public access blocked)"
  type        = string
  default     = "teamvapor-jam-drops"
}

variable "max_parcel_mb" {
  type    = number
  default = 200
}

variable "quota_mb" {
  description = "Per-mailbox quota"
  type        = number
  default     = 1024
}

data "aws_s3_bucket" "relay" {
  bucket = var.bucket_name
}

data "archive_file" "postmaster" {
  type        = "zip"
  source_file = "${path.module}/postmaster.py"
  output_path = "${path.module}/.build/postmaster.zip"
}

resource "aws_iam_role" "postmaster" {
  name = "jamrelay-postmaster"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "postmaster" {
  name = "jamrelay-postmaster-s3"
  role = aws_iam_role.postmaster.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:ListBucket"]
        Resource = data.aws_s3_bucket.relay.arn
        Condition = { StringLike = { "s3:prefix" = "mail/*" } }
      },
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"]
        Resource = "${data.aws_s3_bucket.relay.arn}/mail/*"
      },
      {
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "arn:aws:logs:*:*:*"
      },
    ]
  })
}

resource "aws_lambda_function" "postmaster" {
  function_name    = "jamrelay-postmaster"
  role             = aws_iam_role.postmaster.arn
  runtime          = "python3.12"
  handler          = "postmaster.handler"
  filename         = data.archive_file.postmaster.output_path
  source_code_hash = data.archive_file.postmaster.output_base64sha256
  timeout          = 10
  memory_size      = 128

  # cost fuse: at most 2 concurrent invocations
  reserved_concurrent_executions = 2

  environment {
    variables = {
      BUCKET        = var.bucket_name
      MAX_PARCEL_MB = tostring(var.max_parcel_mb)
      QUOTA_MB      = tostring(var.quota_mb)
    }
  }
}

resource "aws_lambda_function_url" "postmaster" {
  function_name      = aws_lambda_function.postmaster.function_name
  authorization_type = "NONE"
}

# auth NONE still requires explicit public-invoke grants (BOTH actions,
# per current Lambda docs: InvokeFunctionUrl alone 403s at the front door)
resource "aws_lambda_permission" "public_url" {
  statement_id           = "AllowPublicFunctionUrl"
  action                 = "lambda:InvokeFunctionUrl"
  function_name          = aws_lambda_function.postmaster.function_name
  principal              = "*"
  function_url_auth_type = "NONE"
}

# NOTE: no function_url_auth_type here — the provider only allows that
# argument on InvokeFunctionUrl. Principal * on InvokeFunction sounds scary
# but exposes nothing the public URL doesn't already: same function, same
# three presign ops. (Anonymous callers still can't hit the Invoke API —
# it requires SigV4 — so this grants signed-in strangers the same access
# the URL gives everyone.)
resource "aws_lambda_permission" "public_invoke" {
  statement_id  = "AllowPublicInvokeForUrl"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.postmaster.function_name
  principal     = "*"
}

output "relay_url" {
  description = "The postmaster endpoint — the ONLY thing the app needs to know"
  value       = aws_lambda_function_url.postmaster.function_url
}
