# Site feedback box: one Lambda ("the scribe") behind a Function URL,
# writing small JSON objects to S3. No accounts, no database, no expiry —
# feedback is kept forever (unlike the jam relay's 30-day mailbox).
#
# Abuse posture, same spirit as jamrelay: the URL is public by design;
# the caps (8KB body, 4000-char message, reserved concurrency 1) bound
# worst-case abuse to a trickle of tiny objects.

resource "aws_s3_bucket" "feedback" {
  bucket = "vapor-engineering-feedback"
}

resource "aws_s3_bucket_public_access_block" "feedback" {
  bucket                  = aws_s3_bucket.feedback.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# every submission gets published here with the full message text;
# email subscription -> hello@ (ImprovMX fans it out to both members).
# NOTE: the subscription stays "pending" until someone clicks the
# confirmation link SNS emails to hello@.
resource "aws_sns_topic" "feedback" {
  name = "vapor-site-feedback"
}

resource "aws_sns_topic_subscription" "feedback_email" {
  topic_arn = aws_sns_topic.feedback.arn
  protocol  = "email"
  endpoint  = "hello@vapor.engineering"
}

data "archive_file" "feedback" {
  type        = "zip"
  source_file = "${path.module}/feedback.py"
  output_path = "${path.module}/.build/feedback.zip"
}

resource "aws_iam_role" "feedback" {
  name = "vapor-site-feedback"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "feedback" {
  name = "vapor-site-feedback-s3"
  role = aws_iam_role.feedback.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:PutObject"]
        Resource = "${aws_s3_bucket.feedback.arn}/feedback/*"
      },
      {
        Effect   = "Allow"
        Action   = ["sns:Publish"]
        Resource = aws_sns_topic.feedback.arn
      },
      {
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "arn:aws:logs:*:*:*"
      },
    ]
  })
}

resource "aws_lambda_function" "feedback" {
  function_name    = "vapor-site-feedback"
  role             = aws_iam_role.feedback.arn
  runtime          = "python3.12"
  handler          = "feedback.handler"
  filename         = data.archive_file.feedback.output_path
  source_code_hash = data.archive_file.feedback.output_base64sha256
  timeout          = 5
  memory_size      = 128

  # cost fuse: feedback volume is human-scale; 1 is plenty
  reserved_concurrent_executions = 1

  environment {
    variables = {
      BUCKET    = aws_s3_bucket.feedback.bucket
      TOPIC_ARN = aws_sns_topic.feedback.arn
    }
  }
}

resource "aws_lambda_function_url" "feedback" {
  function_name      = aws_lambda_function.feedback.function_name
  authorization_type = "NONE"

  cors {
    allow_origins = ["https://vapor.engineering", "https://www.vapor.engineering"]
    allow_methods = ["POST"]
    allow_headers = ["content-type"]
  }
}

# both grants required for a public Function URL (see jamrelay/main.tf)
resource "aws_lambda_permission" "feedback_url" {
  statement_id           = "AllowPublicFunctionUrl"
  action                 = "lambda:InvokeFunctionUrl"
  function_name          = aws_lambda_function.feedback.function_name
  principal              = "*"
  function_url_auth_type = "NONE"
}

resource "aws_lambda_permission" "feedback_invoke" {
  statement_id  = "AllowPublicInvokeForUrl"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.feedback.function_name
  principal     = "*"
}

output "feedback_url" {
  description = "POST {message, name?} here — baked into index.html (public by nature)"
  value       = aws_lambda_function_url.feedback.function_url
}
