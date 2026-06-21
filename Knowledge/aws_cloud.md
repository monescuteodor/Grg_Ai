# AWS Cloud Services Complete Reference


---

# CHAPTER 1: AWS FUNDAMENTALS


## Remarks

Amazon Web Services (AWS) is the world's largest cloud platform, launched in 2006 with S3 and EC2. It offers 200+ services across compute, storage, databases, networking, AI/ML, security, and more. AWS controls roughly 31% of the cloud market (2025), followed by Azure (~25%) and GCP (~11%).

Key concepts: **Regions** (geographic areas with multiple data centers), **Availability Zones** (isolated data centers within a region), **IAM** (Identity and Access Management), **VPC** (Virtual Private Cloud — your network), **Pay-as-you-go** (no upfront cost, pay per use), **Shared Responsibility Model** (AWS secures infrastructure, you secure your apps/data).

Used by: Netflix, Airbnb, NASA, Samsung, BMW, Stripe, Slack — millions of companies.

Tools: **AWS Console** (web UI), **AWS CLI** (command line), **AWS SDK** (programmatic: boto3 for Python, aws-sdk for JS), **CloudFormation / CDK** (Infrastructure as Code), **Terraform** (multi-cloud IaC).


## Core Concepts

```
REGIONS AND AVAILABILITY ZONES:

  Region: geographic area (eu-central-1 = Frankfurt, us-east-1 = Virginia)
  AZ: isolated data center within region (eu-central-1a, eu-central-1b, eu-central-1c)
  
  Best practice: deploy across multiple AZs for high availability.
  Some services are GLOBAL (IAM, CloudFront, Route 53).
  Most services are REGIONAL (EC2, S3, RDS).

CHOOSING A REGION:
  1. Latency:    closest to your users
  2. Compliance: data residency laws (GDPR → EU region)
  3. Services:   not all services in all regions
  4. Cost:       prices vary by region (us-east-1 usually cheapest)

PRICING MODEL:
  On-Demand:     pay per hour/second, no commitment (most flexible)
  Reserved:      1-3 year commitment, 30-72% discount (predictable workloads)
  Spot:          bid on spare capacity, 60-90% discount (can be interrupted!)
  Savings Plans: commit to $/hr spend, flexible across services

FREE TIER (first 12 months):
  EC2:     750 hours/month t2.micro or t3.micro
  S3:      5 GB storage
  RDS:     750 hours/month db.t2.micro
  Lambda:  1M requests/month (always free!)
  DynamoDB: 25 GB storage (always free!)
```


## AWS CLI Basics

```bash
# Install
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure credentials
aws configure
# AWS Access Key ID: AKIAIOSFODNN7EXAMPLE
# AWS Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
# Default region name: eu-central-1
# Default output format: json

# Test
aws sts get-caller-identity
# Returns your account ID, user ARN

# Common patterns
aws <service> <command> --option value
aws s3 ls                              # List S3 buckets
aws ec2 describe-instances             # List EC2 instances
aws iam list-users                     # List IAM users

# Output formats
aws ec2 describe-instances --output table
aws ec2 describe-instances --output json
aws ec2 describe-instances --query 'Reservations[].Instances[].InstanceId'

# Profiles (multiple accounts)
aws configure --profile staging
aws s3 ls --profile staging
export AWS_PROFILE=staging             # Set default
```


---

# CHAPTER 2: IAM (Identity and Access Management)


## IAM Concepts

```
USERS:      Individual people/services with credentials
GROUPS:     Collection of users (attach policies to group)
ROLES:      Temporary credentials for services/apps (PREFERRED over users for apps)
POLICIES:   JSON documents defining permissions

BEST PRACTICES:
  ✅ NEVER use root account for daily work
  ✅ Enable MFA on root and all users
  ✅ Use roles for applications (not access keys)
  ✅ Least privilege: give minimum permissions needed
  ✅ Use groups, not individual user policies
  ✅ Rotate access keys regularly
  ✅ Use IAM Access Analyzer to find unused permissions
```


## IAM Policy

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowS3ReadOnly",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::my-bucket",
                "arn:aws:s3:::my-bucket/*"
            ]
        },
        {
            "Sid": "DenyDeleteProduction",
            "Effect": "Deny",
            "Action": "s3:DeleteObject",
            "Resource": "arn:aws:s3:::prod-*/*"
        }
    ]
}
```

```bash
# CLI: create user, group, attach policy
aws iam create-user --user-name developer
aws iam create-group --group-name developers
aws iam add-user-to-group --user-name developer --group-name developers
aws iam attach-group-policy --group-name developers \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# Create custom policy
aws iam create-policy --policy-name MyAppPolicy \
    --policy-document file://policy.json

# Create role for EC2
aws iam create-role --role-name MyAppRole \
    --assume-role-policy-document file://trust-policy.json
aws iam attach-role-policy --role-name MyAppRole \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```


---

# CHAPTER 3: EC2 (Elastic Compute Cloud)


## EC2 Basics

```
WHAT: Virtual servers in the cloud.
USE: Web servers, application servers, batch processing, anything.

INSTANCE TYPES (naming: family.size):
  t3.micro    — 2 vCPU, 1 GB RAM (free tier, burstable)
  t3.medium   — 2 vCPU, 4 GB RAM (dev/small apps)
  m5.large    — 2 vCPU, 8 GB RAM (general purpose)
  c5.xlarge   — 4 vCPU, 8 GB RAM (compute-optimized: encoding, ML)
  r5.large    — 2 vCPU, 16 GB RAM (memory-optimized: databases, caches)
  p3.2xlarge  — 8 vCPU, 61 GB, 1x V100 GPU (ML training)
  
FAMILIES:
  t = burstable (saves credits, bursts when needed)
  m = general purpose (balanced)
  c = compute (CPU-heavy: compilation, encoding)
  r = memory (RAM-heavy: databases, caches)
  p/g = GPU (ML, graphics)
  i = storage (high IOPS: databases)

AMI (Amazon Machine Image):
  Template for the OS + software on the instance.
  Amazon Linux 2023, Ubuntu 22.04, Windows Server, custom AMIs.
```


## Launch and Connect

```bash
# Create key pair (for SSH)
aws ec2 create-key-pair --key-name mykey --query 'KeyMaterial' --output text > mykey.pem
chmod 400 mykey.pem

# Create security group (firewall)
aws ec2 create-security-group --group-name web-sg \
    --description "Web server security group"

# Allow SSH and HTTP
aws ec2 authorize-security-group-ingress --group-name web-sg \
    --protocol tcp --port 22 --cidr 0.0.0.0/0      # SSH (restrict to your IP!)
aws ec2 authorize-security-group-ingress --group-name web-sg \
    --protocol tcp --port 80 --cidr 0.0.0.0/0       # HTTP
aws ec2 authorize-security-group-ingress --group-name web-sg \
    --protocol tcp --port 443 --cidr 0.0.0.0/0      # HTTPS

# Launch instance
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t3.micro \
    --key-name mykey \
    --security-groups web-sg \
    --count 1 \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=WebServer}]' \
    --user-data file://setup.sh       # Bootstrap script

# setup.sh (runs on first boot)
#!/bin/bash
yum update -y
yum install -y docker
systemctl start docker
systemctl enable docker
docker run -d -p 80:3000 myapp:latest

# Connect via SSH
ssh -i mykey.pem ec2-user@<public-ip>

# List instances
aws ec2 describe-instances --query \
    'Reservations[].Instances[].[InstanceId,State.Name,PublicIpAddress,Tags[?Key==`Name`].Value|[0]]' \
    --output table

# Stop / start / terminate
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
aws ec2 start-instances --instance-ids i-1234567890abcdef0
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
```


## Auto Scaling

```
AUTO SCALING GROUP (ASG):
  Automatically adjusts number of EC2 instances based on demand.
  
  Components:
    Launch Template: what to launch (AMI, instance type, security groups)
    ASG: how many, min/max, scaling policies
    Scaling Policy: when to scale (CPU > 70% → add instance)

  Flow:
    Traffic increases
      → CloudWatch alarm triggers (CPU > 70%)
      → ASG launches new instance
      → Load balancer adds it to rotation
    Traffic decreases
      → CloudWatch alarm triggers (CPU < 30%)
      → ASG terminates instance
      → Load balancer removes it
```

```bash
# Create launch template
aws ec2 create-launch-template \
    --launch-template-name my-template \
    --launch-template-data '{
        "ImageId": "ami-0c55b159cbfafe1f0",
        "InstanceType": "t3.micro",
        "KeyName": "mykey",
        "SecurityGroupIds": ["sg-12345"]
    }'

# Create ASG
aws autoscaling create-auto-scaling-group \
    --auto-scaling-group-name my-asg \
    --launch-template LaunchTemplateName=my-template,Version='$Latest' \
    --min-size 2 \
    --max-size 10 \
    --desired-capacity 3 \
    --availability-zones eu-central-1a eu-central-1b \
    --target-group-arns arn:aws:elasticloadbalancing:...

# Scaling policy
aws autoscaling put-scaling-policy \
    --auto-scaling-group-name my-asg \
    --policy-name scale-up \
    --policy-type TargetTrackingScaling \
    --target-tracking-configuration '{
        "PredefinedMetricSpecification": {
            "PredefinedMetricType": "ASGAverageCPUUtilization"
        },
        "TargetValue": 70.0
    }'
```


---

# CHAPTER 4: S3 (Simple Storage Service)


## S3 Concepts

```
WHAT: Object storage (files) with unlimited capacity.
USE: Static assets, backups, data lakes, website hosting, logs.

CONCEPTS:
  Bucket:    Container for objects (globally unique name)
  Object:    File + metadata (up to 5 TB per object)
  Key:       Object path within bucket (e.g., "images/photo.jpg")
  
  URL: https://my-bucket.s3.eu-central-1.amazonaws.com/images/photo.jpg

STORAGE CLASSES (cost vs access speed):
  Standard:           Frequent access (most common)
  Standard-IA:        Infrequent access (cheaper storage, retrieval fee)
  One Zone-IA:        Single AZ (cheaper, less durable)
  Glacier Instant:    Archive, instant retrieval
  Glacier Flexible:   Archive, 1-5 min retrieval
  Glacier Deep:       Cheapest, 12-48 hour retrieval
  Intelligent-Tiering: Auto-moves between tiers based on access patterns

DURABILITY: 99.999999999% (11 nines!) — virtually impossible to lose data.
AVAILABILITY: 99.99% (Standard).
```


## S3 Operations

```bash
# Create bucket
aws s3 mb s3://my-unique-bucket-name-2026

# Upload
aws s3 cp file.txt s3://my-bucket/
aws s3 cp file.txt s3://my-bucket/folder/file.txt
aws s3 cp . s3://my-bucket/backup/ --recursive          # Upload directory
aws s3 cp bigfile.zip s3://my-bucket/ --storage-class GLACIER

# Download
aws s3 cp s3://my-bucket/file.txt .
aws s3 cp s3://my-bucket/folder/ ./local/ --recursive    # Download directory

# Sync (like rsync — only transfers changed files)
aws s3 sync ./dist s3://my-bucket/static/
aws s3 sync s3://my-bucket/backup/ ./restore/

# List
aws s3 ls s3://my-bucket/
aws s3 ls s3://my-bucket/folder/ --recursive

# Delete
aws s3 rm s3://my-bucket/file.txt
aws s3 rm s3://my-bucket/folder/ --recursive             # Delete folder

# Delete bucket (must be empty first)
aws s3 rb s3://my-bucket --force                         # Force empties then deletes

# Presigned URL (temporary access without credentials)
aws s3 presign s3://my-bucket/private-file.pdf --expires-in 3600   # 1 hour
```


## S3 with Python (boto3)

```python
import boto3

s3 = boto3.client('s3')

# Upload file
s3.upload_file('local_file.txt', 'my-bucket', 'path/file.txt')

# Upload with metadata
s3.upload_file(
    'image.jpg', 'my-bucket', 'images/photo.jpg',
    ExtraArgs={
        'ContentType': 'image/jpeg',
        'ACL': 'public-read',
        'Metadata': {'author': 'alice'},
    }
)

# Download
s3.download_file('my-bucket', 'path/file.txt', 'local_copy.txt')

# Read file content directly (without downloading)
response = s3.get_object(Bucket='my-bucket', Key='data.json')
content = response['Body'].read().decode('utf-8')
data = json.loads(content)

# List objects
paginator = s3.get_paginator('list_objects_v2')
for page in paginator.paginate(Bucket='my-bucket', Prefix='logs/'):
    for obj in page.get('Contents', []):
        print(f"{obj['Key']} ({obj['Size']} bytes)")

# Generate presigned URL
url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'my-bucket', 'Key': 'private/report.pdf'},
    ExpiresIn=3600,
)
print(f"Download URL (valid 1hr): {url}")

# Delete
s3.delete_object(Bucket='my-bucket', Key='path/file.txt')
```


## Static Website Hosting

```bash
# Enable static website hosting
aws s3 website s3://my-website-bucket \
    --index-document index.html \
    --error-document error.html

# Upload website files
aws s3 sync ./dist s3://my-website-bucket --delete

# Bucket policy for public access
cat > policy.json << 'EOF'
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicRead",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my-website-bucket/*"
        }
    ]
}
EOF

aws s3api put-bucket-policy --bucket my-website-bucket --policy file://policy.json

# URL: http://my-website-bucket.s3-website.eu-central-1.amazonaws.com
# For HTTPS + custom domain: use CloudFront in front
```


---

# CHAPTER 5: LAMBDA (Serverless Compute)


## Lambda Basics

```
WHAT: Run code without managing servers.
      Upload function, AWS handles everything else.
      Pay only when function runs (per request + duration).

USE CASES:
  - API backends (behind API Gateway)
  - Event processing (S3 upload → resize image)
  - Scheduled tasks (cron jobs)
  - Data transformation (Kinesis/SQS processing)
  - ChatOps (Slack bot handlers)

LIMITS:
  Timeout:     15 minutes max
  Memory:      128 MB - 10 GB
  Package:     50 MB zipped (250 MB unzipped)
  /tmp:        512 MB - 10 GB ephemeral storage
  Concurrency: 1000 concurrent (default, can increase)

COLD START:
  First invocation after idle → takes longer (init runtime).
  Python/Node: ~200-500ms
  Java/C#: ~1-5 seconds
  Provisioned Concurrency: pre-warm instances (costs more)

PRICING:
  Requests: $0.20 per 1M requests
  Duration: $0.0000166667 per GB-second
  Example: 1M requests × 256MB × 200ms = ~$0.83/month
  VERY CHEAP for spiky/low-traffic workloads.
```


## Lambda Function

```python
# lambda_function.py

import json
import boto3
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """
    event:   trigger data (API Gateway request, S3 event, etc.)
    context: runtime info (function name, memory, time remaining)
    """
    
    # API Gateway event
    if 'httpMethod' in event:
        method = event['httpMethod']
        path = event['path']
        body = json.loads(event.get('body', '{}'))
        query = event.get('queryStringParameters', {}) or {}
        
        if method == 'GET' and path == '/users':
            users = get_users(query.get('limit', 20))
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({'data': users}),
            }
        
        if method == 'POST' and path == '/users':
            user = create_user(body)
            return {
                'statusCode': 201,
                'body': json.dumps(user),
            }
        
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Not found'}),
        }
    
    # S3 event (file uploaded)
    if 'Records' in event and event['Records'][0].get('eventSource') == 'aws:s3':
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        print(f"New file uploaded: s3://{bucket}/{key}")
        process_upload(bucket, key)
        
        return {'statusCode': 200}
    
    return {'statusCode': 400, 'body': 'Unknown event'}


def get_users(limit):
    # Query DynamoDB or RDS
    pass

def create_user(data):
    # Insert into database
    pass

def process_upload(bucket, key):
    # Example: resize uploaded image
    pass
```

```bash
# Deploy Lambda
zip function.zip lambda_function.py

aws lambda create-function \
    --function-name my-api \
    --runtime python3.12 \
    --handler lambda_function.lambda_handler \
    --role arn:aws:iam::123456789:role/lambda-role \
    --zip-file fileb://function.zip \
    --timeout 30 \
    --memory-size 256 \
    --environment Variables='{DB_HOST=mydb.cluster.amazonaws.com}'

# Update function code
aws lambda update-function-code \
    --function-name my-api \
    --zip-file fileb://function.zip

# Invoke (test)
aws lambda invoke \
    --function-name my-api \
    --payload '{"httpMethod":"GET","path":"/users"}' \
    output.json

cat output.json

# View logs
aws logs tail /aws/lambda/my-api --follow
```


---

# CHAPTER 6: DATABASES (RDS, DynamoDB)


## RDS (Relational Database Service)

```
WHAT: Managed relational databases.
      AWS handles: backups, patches, replication, failover.

ENGINES:
  PostgreSQL, MySQL, MariaDB, Oracle, SQL Server, Aurora

AURORA:
  AWS's custom engine (MySQL/PostgreSQL compatible).
  5x faster than MySQL, 3x than PostgreSQL.
  Auto-scales storage (10 GB → 128 TB).
  Up to 15 read replicas.
  Multi-AZ by default.
  
  Aurora Serverless: auto-scales compute (pay per ACU-second).
  Great for variable workloads.
```

```bash
# Create RDS instance
aws rds create-db-instance \
    --db-instance-identifier mydb \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --engine-version 16 \
    --master-username admin \
    --master-user-password MySecretPass123 \
    --allocated-storage 20 \
    --storage-type gp3 \
    --vpc-security-group-ids sg-12345 \
    --backup-retention-period 7 \
    --multi-az \
    --storage-encrypted

# Connect
psql -h mydb.xxxx.eu-central-1.rds.amazonaws.com -U admin -d postgres

# Create read replica
aws rds create-db-instance-read-replica \
    --db-instance-identifier mydb-read \
    --source-db-instance-identifier mydb

# Snapshot (manual backup)
aws rds create-db-snapshot \
    --db-instance-identifier mydb \
    --db-snapshot-identifier mydb-snap-2026-06-10
```


## DynamoDB (NoSQL)

```
WHAT: Fully managed NoSQL key-value + document database.
      Single-digit millisecond latency at any scale.
      No servers, no patches, no capacity planning (on-demand).

USE CASES:
  - Session stores
  - Shopping carts
  - Gaming leaderboards
  - IoT data
  - User preferences
  - High-throughput event logging

CONCEPTS:
  Table:         Collection of items
  Item:          Row (document)
  Attribute:     Field
  Partition Key: Primary key (hash) — required, distributes data
  Sort Key:      Optional secondary key — enables range queries
  GSI:           Global Secondary Index — query on different keys
  LSI:           Local Secondary Index — same partition key, different sort

PRICING:
  On-Demand:    pay per read/write ($1.25 per million writes)
  Provisioned:  set capacity units, cheaper for steady workloads
  Free tier:    25 GB + 25 read/write capacity units (ALWAYS free!)
```

```python
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

# Put item
table.put_item(Item={
    'user_id': 'user-123',
    'email': 'alice@example.com',
    'name': 'Alice',
    'age': 30,
    'tags': ['developer', 'python'],
    'address': {
        'city': 'Brașov',
        'country': 'Romania',
    },
})

# Get item
response = table.get_item(Key={'user_id': 'user-123'})
user = response.get('Item')

# Query (partition key + sort key condition)
response = table.query(
    KeyConditionExpression='user_id = :uid AND created_at > :date',
    ExpressionAttributeValues={
        ':uid': 'user-123',
        ':date': '2026-01-01',
    },
)
items = response['Items']

# Scan (full table — expensive, avoid in production!)
response = table.scan(
    FilterExpression='age > :min_age',
    ExpressionAttributeValues={':min_age': 25},
)

# Update item
table.update_item(
    Key={'user_id': 'user-123'},
    UpdateExpression='SET #n = :name, age = :age',
    ExpressionAttributeNames={'#n': 'name'},   # 'name' is reserved word
    ExpressionAttributeValues={':name': 'Alice Smith', ':age': 31},
)

# Delete
table.delete_item(Key={'user_id': 'user-123'})

# Batch write (up to 25 items)
with table.batch_writer() as batch:
    for i in range(100):
        batch.put_item(Item={
            'user_id': f'user-{i}',
            'name': f'User {i}',
        })
```


---

# CHAPTER 7: NETWORKING (VPC)


## VPC Basics

```
VPC (Virtual Private Cloud): your isolated network in AWS.

COMPONENTS:
  Subnet:           Sub-network within VPC (public or private)
  Internet Gateway:  Connects VPC to internet
  NAT Gateway:       Lets private subnets access internet (outbound only)
  Route Table:       Rules for traffic routing
  Security Group:    Instance-level firewall (stateful)
  NACL:              Subnet-level firewall (stateless)

TYPICAL ARCHITECTURE:
  
  Internet
      │
  Internet Gateway
      │
  ┌───┴────────────────────────────────┐
  │ VPC: 10.0.0.0/16                   │
  │                                     │
  │  ┌──────────────┐ ┌──────────────┐ │
  │  │ Public Subnet │ │ Public Subnet│ │
  │  │ 10.0.1.0/24  │ │ 10.0.2.0/24 │ │
  │  │ (AZ-a)       │ │ (AZ-b)      │ │
  │  │ [ALB, NAT]   │ │ [ALB]       │ │
  │  └──────┬───────┘ └──────┬──────┘ │
  │         │                 │        │
  │  ┌──────┴───────┐ ┌──────┴──────┐ │
  │  │Private Subnet│ │Private Subnet│ │
  │  │ 10.0.3.0/24  │ │ 10.0.4.0/24 │ │
  │  │ (AZ-a)       │ │ (AZ-b)      │ │
  │  │ [EC2, RDS]   │ │ [EC2, RDS]  │ │
  │  └──────────────┘ └─────────────┘ │
  └────────────────────────────────────┘

SECURITY GROUPS (instance firewall):
  - Stateful: allow outbound → response auto-allowed inbound
  - Default: deny all inbound, allow all outbound
  - Rules: protocol + port + source (IP or another security group)

  Example:
    Web server SG:  allow TCP 80, 443 from 0.0.0.0/0
    App server SG:  allow TCP 3000 from web-server-SG
    Database SG:    allow TCP 5432 from app-server-SG only
```


---

# CHAPTER 8: OTHER ESSENTIAL SERVICES


## SQS (Simple Queue Service)

```python
import boto3

sqs = boto3.client('sqs')
queue_url = 'https://sqs.eu-central-1.amazonaws.com/123456789/my-queue'

# Send message
sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=json.dumps({'order_id': '123', 'action': 'process'}),
    MessageAttributes={
        'Priority': {'StringValue': 'high', 'DataType': 'String'},
    },
)

# Receive messages (long polling)
response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=10,
    WaitTimeSeconds=20,       # Long polling (cheaper, fewer empty responses)
    VisibilityTimeout=30,     # Hide message for 30s while processing
)

for msg in response.get('Messages', []):
    body = json.loads(msg['Body'])
    process_order(body)

    # Delete after successful processing
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=msg['ReceiptHandle'],
    )
```


## SNS (Simple Notification Service)

```python
sns = boto3.client('sns')

# Create topic
topic_arn = sns.create_topic(Name='order-events')['TopicArn']

# Subscribe
sns.subscribe(TopicArn=topic_arn, Protocol='email', Endpoint='admin@example.com')
sns.subscribe(TopicArn=topic_arn, Protocol='sqs', Endpoint=sqs_queue_arn)
sns.subscribe(TopicArn=topic_arn, Protocol='lambda', Endpoint=lambda_arn)

# Publish
sns.publish(
    TopicArn=topic_arn,
    Subject='New Order',
    Message=json.dumps({'order_id': '123', 'total': 99.99}),
)
# All subscribers receive the message (fan-out pattern)
```


## CloudFront (CDN)

```
WHAT: Content Delivery Network.
      Cache content at 400+ edge locations worldwide.

USE:
  - Static websites (S3 + CloudFront)
  - API acceleration
  - Video streaming
  - Software distribution

BENEFITS:
  - Low latency (served from nearest edge)
  - HTTPS with custom domain (free cert via ACM)
  - DDoS protection (AWS Shield)
  - Cache headers respected
```


## Route 53 (DNS)

```
WHAT: DNS service.
      Register domains, route traffic, health checks.

ROUTING POLICIES:
  Simple:       One record, one destination
  Weighted:     Split traffic (80% to v1, 20% to v2)
  Latency:      Route to lowest-latency region
  Failover:     Active/standby with health checks
  Geolocation:  Route by user's country/continent
  Multi-value:  Return multiple IPs (client-side LB)
```


## CloudWatch (Monitoring)

```bash
# CloudWatch = AWS monitoring service
# Metrics, logs, alarms, dashboards

# View metrics
aws cloudwatch get-metric-statistics \
    --namespace AWS/EC2 \
    --metric-name CPUUtilization \
    --start-time 2026-06-10T00:00:00 \
    --end-time 2026-06-10T23:59:59 \
    --period 3600 \
    --statistics Average

# Create alarm
aws cloudwatch put-metric-alarm \
    --alarm-name HighCPU \
    --metric-name CPUUtilization \
    --namespace AWS/EC2 \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 2 \
    --alarm-actions arn:aws:sns:...:alert-topic \
    --dimensions Name=InstanceId,Value=i-12345

# Log groups (Lambda auto-creates /aws/lambda/function-name)
aws logs describe-log-groups
aws logs tail /aws/lambda/my-function --follow
```


---

# CHAPTER 9: INFRASTRUCTURE AS CODE


## CloudFormation

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Simple web app stack

Parameters:
  InstanceType:
    Type: String
    Default: t3.micro
    AllowedValues: [t3.micro, t3.small, t3.medium]

  Environment:
    Type: String
    Default: dev
    AllowedValues: [dev, staging, prod]

Resources:
  WebSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Web server security group
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0

  WebServer:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !Ref InstanceType
      ImageId: ami-0c55b159cbfafe1f0
      SecurityGroupIds:
        - !Ref WebSecurityGroup
      Tags:
        - Key: Name
          Value: !Sub "${Environment}-web-server"
        - Key: Environment
          Value: !Ref Environment
      UserData:
        Fn::Base64: |
          #!/bin/bash
          yum update -y
          yum install -y httpd
          systemctl start httpd

  AppBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "${Environment}-app-assets-${AWS::AccountId}"

Outputs:
  WebServerIP:
    Description: Public IP of web server
    Value: !GetAtt WebServer.PublicIp

  BucketName:
    Description: S3 bucket name
    Value: !Ref AppBucket
```

```bash
# Deploy stack
aws cloudformation create-stack \
    --stack-name my-app \
    --template-body file://template.yaml \
    --parameters ParameterKey=Environment,ParameterValue=prod

# Update stack
aws cloudformation update-stack \
    --stack-name my-app \
    --template-body file://template.yaml

# Delete stack (removes ALL resources!)
aws cloudformation delete-stack --stack-name my-app

# View outputs
aws cloudformation describe-stacks --stack-name my-app \
    --query 'Stacks[0].Outputs'
```


---

# CHAPTER 10: COMMON PITFALLS


## AWS Pitfalls

```
PITFALL 1: Using root account
  Root has unlimited access. If compromised → total control.
  Fix: Create IAM user, enable MFA on root, lock root away.

PITFALL 2: Access keys in code/Git
  Leaked keys → attacker mines crypto on your account → $50K bill.
  Fix: Use IAM roles for EC2/Lambda. Never commit credentials.
  AWS has automated scanning that disables leaked keys.

PITFALL 3: Public S3 buckets
  Misconfigured bucket → data exposed to internet.
  Fix: Block public access by default. Use S3 Block Public Access.
  aws s3api put-public-access-block --bucket my-bucket \
      --public-access-block-configuration BlockPublicAcls=true,...

PITFALL 4: No budget alerts
  Surprise $10K bill at end of month.
  Fix: Set AWS Budgets + alerts. Check daily during learning.

PITFALL 5: Leaving resources running
  Forgot to terminate EC2, NAT Gateway, RDS → charges accumulate.
  Fix: Tag everything, review costs weekly, use AWS Cost Explorer.

PITFALL 6: Single AZ deployment
  AZ goes down → entire app down.
  Fix: Deploy across 2+ AZs. Use ALB + ASG.

PITFALL 7: No backups
  Delete database → data gone forever.
  Fix: Enable automated backups (RDS), versioning (S3), snapshots.

PITFALL 8: Security groups too open
  0.0.0.0/0 on SSH (port 22) → brute force attacks.
  Fix: Restrict SSH to your IP only. Use Systems Manager Session Manager instead.

PITFALL 9: Not using managed services
  Running your own PostgreSQL on EC2 (patching, backups, replication).
  Fix: Use RDS. Let AWS handle operations.

PITFALL 10: Ignoring the free tier
  Free tier is generous! t3.micro, S3, Lambda, DynamoDB.
  Fix: Start with free tier services. Upgrade when needed.

PITFALL 11: Hardcoding region/account
  Code assumes us-east-1, breaks in eu-central-1.
  Fix: Use environment variables, SDK auto-detection.

PITFALL 12: Not encrypting data
  S3 objects, RDS databases, EBS volumes unencrypted.
  Fix: Enable encryption at rest (SSE-S3, KMS). Enable in-transit (TLS).

PITFALL 13: Lambda cold starts in production
  User hits API → 3 second delay (cold start).
  Fix: Provisioned Concurrency, or use smaller runtimes (Node > Java).

PITFALL 14: DynamoDB scan in production
  Scan reads EVERY item in table → expensive + slow.
  Fix: Design proper partition/sort keys. Use Query, not Scan.

PITFALL 15: No monitoring
  Something breaks, nobody knows for hours.
  Fix: CloudWatch alarms on key metrics. SNS notifications. PagerDuty.
```