# Purchased SFX libraries (Micro BOOM "Hot Rod - Rev Ups", Sound Ideas
# "Speed"): royalty-free to USE in productions, never redistributable —
# this bucket stays private, no exceptions. Master copies live here;
# the local working copy is Documents/GitHub/music/sfx on Eli's PC.
# Sharing with Jack = short-lived presigned URLs (aws s3 presign),
# never public objects.

resource "aws_s3_bucket" "sfx_library" {
  bucket = "vapor-sfx-library"
}

resource "aws_s3_bucket_public_access_block" "sfx_library" {
  bucket                  = aws_s3_bucket.sfx_library.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
