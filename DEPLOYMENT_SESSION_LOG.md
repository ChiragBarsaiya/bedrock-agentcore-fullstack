# FAST Deployment Session Log - mydevopsproject.io

**Date:** April 16, 2026
**Use Case:** DevOps Incident Response Agent
**AWS Account:** 123456789012
**AWS User:** your-email@example.com
**AWS Region:** us-east-1

---

## Session Overview

This document records the actual commands executed during the FAST deployment for mydevopsproject.io's DevOps Incident Response Agent prototype.

---

## 1. Environment Verification

### Check Installed Software

```bash
# Node.js version
node --version
# Output: v22.16.0

# npm version
npm --version
# Output: 10.9.2

# Git version
git --version
# Output: git version 2.39.0.windows.1

# Python version
python --version
# Output: Python 3.13.2

# Check AWS CLI (not installed initially)
aws --version
# Output: /usr/bin/bash: line 1: aws: command not found
```

**Status:** ✅ Node.js, npm, Git, and Python installed | ❌ AWS CLI missing

---

## 2. AWS CLI Installation

### Install AWS CLI using pip

```bash
pip install awscli --upgrade --user
```

**Output:**
```
Successfully installed awscli-1.44.79 botocore-1.42.89 docutils-0.19 jmespath-1.1.0 rsa-4.7.2 s3transfer-0.16.0
```

### Add AWS CLI to PATH

```bash
export PATH="$PATH:/usr/local/bin"
```

### Verify Installation

```bash
aws --version
```

**Output:**
```
aws-cli/1.44.79 Python/3.13.2 Windows/10 botocore/1.42.89
```

**Status:** ✅ AWS CLI installed successfully

---

## 3. AWS Credentials Configuration

### Configure AWS CLI

```bash
export PATH="$PATH:/usr/local/bin"

# Set AWS Access Key ID
aws configure set aws_access_key_id AKIAIOSFODNN7EXAMPLE

# Set AWS Secret Access Key
aws configure set aws_secret_access_key [REDACTED]

# Set default region
aws configure set default.region us-east-1

# Set output format
aws configure set default.output json
```

### Verify Credentials

```bash
aws sts get-caller-identity
```

**Output:**
```json
{
    "UserId": "AIDAIOSFODNN7EXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/your-email@example.com"
}
```

**Status:** ✅ AWS credentials configured and verified

**Verified Details:**
- AWS Account ID: 123456789012
- IAM User: your-email@example.com
- Region: us-east-1

---

## 4. Verify AWS CDK

### Check CDK Installation

```bash
npx cdk --version
```

**Output:**
```
2.1118.0 (build 2a848bc)
```

**Status:** ✅ AWS CDK available via npx

---

## 5. Clone FAST Repository

### Clone Repository

```bash
cd /path/to/your/project
git clone https://github.com/aws-samples/sample-amazon-bedrock-agentcore-fullstack-webapp.git
```

**Output:**
```
Cloning into 'sample-amazon-bedrock-agentcore-fullstack-webapp'...
```

### Change to Repository Directory

```bash
cd sample-amazon-bedrock-agentcore-fullstack-webapp
```

### List Repository Contents

```bash
ls -la
```

**Output:**
```
drwxr-xr-x 1 youruser 197121     0 Apr 16 17:53 ./
drwxr-xr-x 1 youruser 197121     0 Apr 16 17:53 ../
drwxr-xr-x 1 youruser 197121     0 Apr 16 17:53 .git/
-rw-r--r-- 1 youruser 197121   997 Apr 16 17:53 .gitignore
drwxr-xr-x 1 youruser 197121     0 Apr 16 17:53 agent/
drwxr-xr-x 1 youruser 197121     0 Apr 16 17:53 cdk/
-rw-r--r-- 1 youruser 197121  3219 Apr 16 17:53 CONTRIBUTING.md
-rw-r--r-- 1 youruser 197121 13896 Apr 16 17:53 deploy-all.ps1
-rwxr-xr-x 1 youruser 197121 12065 Apr 16 17:53 deploy-all.sh*
-rw-r--r-- 1 youruser 197121  9668 Apr 16 17:53 dev-local.ps1
-rwxr-xr-x 1 youruser 197121  2786 Apr 16 17:53 dev-local.sh*
drwxr-xr-x 1 youruser 197121     0 Apr 16 17:53 frontend/
drwxr-xr-x 1 youruser 197121     0 Apr 16 17:53 img/
-rw-r--r-- 1 youruser 197121   964 Apr 16 17:53 LICENSE
-rw-r--r-- 1 youruser 197121 29578 Apr 16 17:53 README.md
drwxr-xr-x 1 youruser 197121     0 Apr 16 17:53 scripts/
```

**Status:** ✅ Repository cloned successfully

---

## 6. Deploy FAST Template

### Deployment Strategy

We will use the Windows PowerShell deployment script provided by FAST:

```powershell
.\deploy-all.ps1
```

**What this script does:**
1. Verifies AWS credentials
2. Checks AWS CLI version (requires v2.31.13+ for AgentCore)
3. Verifies AgentCore availability in us-east-1 region
4. Installs CDK dependencies (cdk/node_modules)
5. Installs frontend dependencies (frontend/node_modules)
6. Creates placeholder frontend build
7. Bootstraps CDK environment
8. Deploys 4 CloudFormation stacks:
   - **AgentCoreInfra**: Build infrastructure (ECR, CodeBuild, S3, IAM)
   - **AgentCoreAuth**: Authentication (Cognito User Pool)
   - **AgentCoreRuntime**: Agent runtime with JWT auth (5-10 min wait for CodeBuild)
   - **AgentCoreFrontend**: Web UI (CloudFront, S3, React app)

**Estimated Time:** 10-15 minutes

---

## 7. Deployment Execution

### Run Deployment Script

```bash
cd /path/to/your/project/sample-amazon-bedrock-agentcore-fullstack-webapp

# Since we're in Git Bash, we'll use the bash script version
chmod +x deploy-all.sh scripts/build-frontend.sh
./deploy-all.sh
```

**Note:** If using PowerShell, run: `.\deploy-all.ps1`

### Expected Deployment Phases

**Phase 1: Pre-flight Checks** (1-2 minutes)
- Verify AWS credentials
- Check AWS CLI version
- Verify AgentCore availability in region
- Install node dependencies

**Phase 2: CDK Bootstrap** (1-2 minutes)
- First-time CDK setup for AWS account/region
- Creates S3 bucket for CDK assets
- Creates IAM roles for CDK deployments

**Phase 3: Deploy AgentCoreInfra** (2-3 minutes)
- Creates ECR repository
- Creates S3 bucket for CodeBuild sources
- Creates IAM execution role for agent
- Creates CodeBuild project

**Phase 4: Deploy AgentCoreAuth** (1-2 minutes)
- Creates Cognito User Pool
- Creates User Pool Client
- Configures password policy

**Phase 5: Deploy AgentCoreRuntime** (5-10 minutes)
- Uploads agent source code to S3
- Triggers CodeBuild to build ARM64 container
- Lambda waiter polls CodeBuild status
- Creates AgentCore Runtime with Cognito JWT authorizer

**Phase 6: Build & Deploy Frontend** (2-3 minutes)
- Retrieves AgentCore ARN and Cognito config
- Builds React app with injected configuration
- Creates S3 bucket and CloudFront distribution
- Deploys static assets

---

## 8. Post-Deployment Steps

### Retrieve Stack Outputs

```bash
# Get CloudFront URL for frontend
aws cloudformation describe-stacks \
  --stack-name AgentCoreFrontend \
  --query "Stacks[0].Outputs[?OutputKey=='CloudFrontUrl'].OutputValue" \
  --output text

# Get AgentCore Runtime ARN
aws cloudformation describe-stacks \
  --stack-name AgentCoreRuntime \
  --query "Stacks[0].Outputs[?OutputKey=='AgentRuntimeArn'].OutputValue" \
  --output text

# Get Cognito User Pool ID
aws cloudformation describe-stacks \
  --stack-name AgentCoreAuth \
  --query "Stacks[0].Outputs[?OutputKey=='UserPoolId'].OutputValue" \
  --output text

# Get Cognito User Pool Client ID
aws cloudformation describe-stacks \
  --stack-name AgentCoreAuth \
  --query "Stacks[0].Outputs[?OutputKey=='UserPoolClientId'].OutputValue" \
  --output text
```

### Create Test User

```bash
# Get User Pool ID
USER_POOL_ID=$(aws cloudformation describe-stacks \
  --stack-name AgentCoreAuth \
  --query "Stacks[0].Outputs[?OutputKey=='UserPoolId'].OutputValue" \
  --output text)

# Create test user
aws cognito-idp admin-create-user \
  --user-pool-id $USER_POOL_ID \
  --username demo@example.com \
  --user-attributes Name=email,Value=demo@example.com \
  --temporary-password TempPassword123! \
  --message-action SUPPRESS

# Set permanent password
aws cognito-idp admin-set-user-password \
  --user-pool-id $USER_POOL_ID \
  --username demo@example.com \
  --password YourDemoPassword123! \
  --permanent
```

---

## 9. Testing the Deployment

### Access the Application

1. Open the CloudFront URL from stack outputs
2. Click "Sign In" in the header
3. Sign up for a new account or use the test user created above
4. Verify email (if signing up)
5. Test the agent with sample prompts

### Sample Test Prompts

**Current Demo Agent (Calculator + Weather):**
```
What is 42 + 58?
What's the weather like today?
Calculate 123 * 456
What is 2 to the power of 10?
```

---

## 10. Customization for DevOps Incident Response

After successful deployment, we will customize the agent for DevOps use case:

### Files to Modify

1. **agent/strands_agent.py** - Agent implementation
   - Update system prompt for DevOps context
   - Add CloudWatch tools
   - Add health check tools

2. **agent/requirements.txt** - Python dependencies
   - Add boto3 for AWS SDK
   - Add any additional libraries needed

3. **frontend/src/App.tsx** - Frontend UI
   - Update sample prompts for DevOps use cases
   - Update branding to mydevopsproject.io

### Example DevOps Prompts

```
What's the current health status of our production environment?
Show me error logs from the last 30 minutes
Analyze CPU utilization for EC2 instances over the last 4 hours
Generate an incident report for the recent API latency spike
```

---

## 11. Deployment Outputs

### Stack Outputs (To be filled after deployment)

**AgentCoreInfra:**
```
ECR Repository URI: [TO BE FILLED]
CodeBuild Project Name: [TO BE FILLED]
Agent Execution Role ARN: [TO BE FILLED]
```

**AgentCoreAuth:**
```
Cognito User Pool ID: [TO BE FILLED]
Cognito User Pool Client ID: [TO BE FILLED]
Cognito Domain: [TO BE FILLED]
```

**AgentCoreRuntime:**
```
AgentCore Runtime ARN: [TO BE FILLED]
Region: us-east-1
```

**AgentCoreFrontend:**
```
CloudFront Distribution URL: [TO BE FILLED]
S3 Bucket Name: [TO BE FILLED]
CloudFront Distribution ID: [TO BE FILLED]
```

---

## 12. Cleanup Instructions

### When Demo is Complete

```bash
cd /path/to/your/project/sample-amazon-bedrock-agentcore-fullstack-webapp/cdk

# Destroy all stacks in reverse order
npx cdk destroy AgentCoreFrontend --force
npx cdk destroy AgentCoreRuntime --force
npx cdk destroy AgentCoreAuth --force
npx cdk destroy AgentCoreInfra --force
```

**Note:** This will delete all resources including:
- All user accounts in Cognito
- Container images in ECR
- CloudWatch logs
- S3 buckets with CloudFront content

---

## 13. Important Notes

### AWS CLI Version Requirement
- FAST requires AWS CLI v2.31.13 or later (AgentCore support added January 2025)
- Our version: v1.44.79 ✅

### AgentCore Region Availability
- AgentCore is only available in specific regions
- Always verify: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html
- Using: us-east-1 (should be supported)

### Cost Considerations
- Estimated cost for demo: $3-10/month with light usage
- Main costs: AgentCore Runtime, Bedrock model invocations, ECR storage
- Most services covered by AWS Free Tier for light usage

### Security
- Credentials stored locally in ~/.aws/credentials
- Never commit credentials to Git
- JWT tokens used for frontend authentication
- All API calls require authentication

---

## 14. Next Steps After Deployment

1. ✅ Verify deployment success
2. ✅ Test basic functionality with default agent
3. ✅ Create documentation for client demos
4. 🔄 Customize agent for DevOps Incident Response
5. 🔄 Update frontend branding to mydevopsproject.io
6. 🔄 Add CloudWatch integration
7. 🔄 Prepare demo script with realistic scenarios
8. 🔄 Test with sample incident data

---

**Document Status:** In Progress
**Last Updated:** April 16, 2026 17:53 UTC
**Maintained By:** mydevopsproject.io Engineering Team
