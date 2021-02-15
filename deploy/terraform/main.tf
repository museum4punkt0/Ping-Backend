variable "aws_access_key" {
  description = "Access key to your AWS account "
}

variable "aws_secret_key" {
  description = "Secret key to your AWS account "
}

variable "aws_region" {
  default     = "eu-central-1"
  description = "AWS region"
}

provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

resource "aws_s3_bucket" "tensorflow" {
  bucket = "mein-object-tensorflow"
  acl    = "private"
}

resource "aws_iam_user" "default" {
  name = "mein-object-bucket-rw"
}
#
resource "aws_s3_bucket_policy" "full_access" {
  bucket = aws_s3_bucket.tensorflow.id

  policy = <<POLICY
{
   "Version": "2012-10-17",
   "Statement": [
      {
         "Sid": "FullAccess",
         "Effect": "Allow",
         "Principal": {
            "AWS": ["${aws_iam_user.default.arn}"]
         },
         "Action": ["s3:*"],
         "Resource": [
            "${aws_s3_bucket.tensorflow.arn}",
            "${aws_s3_bucket.tensorflow.arn}/*"
         ]
      }
  ]
}
POLICY
}


output "user" {
  value = aws_iam_user.default.arn
}

output "bucket" {
  value = aws_s3_bucket.tensorflow.arn
}
