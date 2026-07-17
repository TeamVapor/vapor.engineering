# vapor.engineering DNS -> GitHub Pages.
#
# The hosted zone itself is NOT managed here: Route 53 Domains created it at
# registration and keeps it tied to the domain, so Terraform only manages the
# records inside it (a destroy can never take the zone or the domain down).
# Currently on Eli's personal AWS account; migrate to a company account
# someday (tracked in docs/business-todo.md).

data "aws_route53_zone" "vapor" {
  name = "vapor.engineering."
}

# GitHub Pages apex IPs (docs.github.com/pages -> custom domains)
resource "aws_route53_record" "apex_a" {
  zone_id = data.aws_route53_zone.vapor.zone_id
  name    = "vapor.engineering"
  type    = "A"
  ttl     = 300
  records = [
    "185.199.108.153",
    "185.199.109.153",
    "185.199.110.153",
    "185.199.111.153",
  ]
}

resource "aws_route53_record" "apex_aaaa" {
  zone_id = data.aws_route53_zone.vapor.zone_id
  name    = "vapor.engineering"
  type    = "AAAA"
  ttl     = 300
  records = [
    "2606:50c0:8000::153",
    "2606:50c0:8001::153",
    "2606:50c0:8002::153",
    "2606:50c0:8003::153",
  ]
}

# Email forwarding via ImprovMX (free tier): support@/hello@ -> personal
# inboxes. Aliases are managed in the ImprovMX dashboard, not here.
# SPF authorizes ImprovMX to send (forwarded mail + optional send-as SMTP).
resource "aws_route53_record" "mx" {
  zone_id = data.aws_route53_zone.vapor.zone_id
  name    = "vapor.engineering"
  type    = "MX"
  ttl     = 300
  records = [
    "10 mx1.improvmx.com",
    "20 mx2.improvmx.com",
  ]
}

resource "aws_route53_record" "spf" {
  zone_id = data.aws_route53_zone.vapor.zone_id
  name    = "vapor.engineering"
  type    = "TXT"
  ttl     = 300
  records = ["v=spf1 include:spf.improvmx.com ~all"]
}

resource "aws_route53_record" "www" {
  zone_id = data.aws_route53_zone.vapor.zone_id
  name    = "www.vapor.engineering"
  type    = "CNAME"
  ttl     = 300
  records = ["teamvapor.github.io"]
}
