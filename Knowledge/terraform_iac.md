# Terraform and Infrastructure as Code Reference


---

# CHAPTER 1: TERRAFORM BASICS


## Remarks

Infrastructure as Code (IaC) means defining servers, databases, and networks in code files instead of clicking buttons in cloud dashboards. Terraform by HashiCorp is the most popular IaC tool. It works with AWS, Azure, GCP, Cloudflare, and 3000+ providers.


## Core Concepts

```hcl
# main.tf — Terraform configuration

# Provider: which cloud to use
provider "aws" {
  region = "eu-central-1"
}

# Resource: what to create
resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"  # Ubuntu 24.04
  instance_type = "t3.micro"
  
  tags = {
    Name = "grg-ai-server"
  }
}

# Variables: reusable values
variable "environment" {
  type    = string
  default = "production"
}

variable "instance_count" {
  type    = number
  default = 2
}

# Output: display after apply
output "server_ip" {
  value = aws_instance.web_server.public_ip
}
```


## Common Commands

```bash
# Initialize (download providers)
terraform init

# Preview changes (dry run)
terraform plan

# Apply changes (create/update infrastructure)
terraform apply

# Destroy everything
terraform destroy

# Format code
terraform fmt

# Validate syntax
terraform validate

# Show current state
terraform show

# Import existing resource into Terraform
terraform import aws_instance.web_server i-1234567890
```


## Real-World Example: Full Stack

```hcl
# VPC (Virtual Private Cloud)
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = { Name = "grg-ai-vpc" }
}

# Subnet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  tags = { Name = "grg-ai-public" }
}

# Security Group (firewall)
resource "aws_security_group" "web" {
  vpc_id = aws_vpc.main.id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance
resource "aws_instance" "app" {
  count         = var.instance_count
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.small"
  subnet_id     = aws_subnet.public.id
  
  vpc_security_group_ids = [aws_security_group.web.id]
  
  user_data = <<-EOF
    #!/bin/bash
    apt update && apt install -y docker.io
    docker run -d -p 80:8000 myapp:latest
  EOF
  
  tags = { Name = "grg-ai-${count.index}" }
}

# RDS Database
resource "aws_db_instance" "postgres" {
  identifier        = "grg-ai-db"
  engine            = "postgres"
  engine_version    = "16"
  instance_class    = "db.t3.micro"
  allocated_storage = 20
  
  db_name  = "grgai"
  username = var.db_username
  password = var.db_password
  
  skip_final_snapshot = true
}
```


---

# CHAPTER 2: COMMON PITFALLS

```
PITFALL 1: Storing state file locally
  State file contains all infrastructure details. Losing it = chaos.
  Fix: use remote backend (S3 + DynamoDB for locking).

PITFALL 2: Hardcoding secrets
  password = "mypassword123" in .tf file → committed to git.
  Fix: use variables + terraform.tfvars (in .gitignore) or vault.

PITFALL 3: Not using plan before apply
  terraform apply without plan → unexpected changes/deletions.
  Fix: always terraform plan first, review changes.

PITFALL 4: Modifying infrastructure manually
  Changing things in AWS console → Terraform state drift.
  Fix: ALL changes through Terraform. Never touch console.

PITFALL 5: One giant main.tf
  1000-line config file → unmaintainable.
  Fix: split into modules: network.tf, compute.tf, database.tf.
```