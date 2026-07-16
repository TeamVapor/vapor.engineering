terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region  = "us-west-2"
  profile = "terraform"

  default_tags {
    tags = {
      ManagedBy     = "Terraform"
      Project       = "vapor-engineering"
      TerraformRepo = "github.com/TeamVapor/vapor.engineering"
    }
  }
}
