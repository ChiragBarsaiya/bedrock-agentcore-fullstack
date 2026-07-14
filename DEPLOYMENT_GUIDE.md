# FAST Deployment Guide - DevOps Incident Response Agent

**Company:** mydevopsproject.io
**Use Case:** DevOps Incident Response Agent
**Date:** April 16, 2026
**GitHub Account:** https://github.com/chiragbarsaiya (username: chiragbarsaiya)

---

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Environment Setup](#environment-setup)
4. [AWS CLI Installation & Configuration](#aws-cli-installation--configuration)
5. [Clone FAST Repository](#clone-fast-repository)
6. [Customize for DevOps Incident Response](#customize-for-devops-incident-response)
7. [Deploy to AWS](#deploy-to-aws)
8. [Post-Deployment Configuration](#post-deployment-configuration)
9. [Testing & Validation](#testing--validation)
10. [Troubleshooting](#troubleshooting)

---

## Overview

**What is FAST?**
FAST (Fullstack AgentCore Solution Template) is an AWS starter template that deploys a complete AI agent application with Amazon Bedrock AgentCore in under 30 minutes.

**Our Use Case: DevOps Incident Response Agent**
An intelligent agent that helps DevOps teams diagnose and respond to production incidents by:
- Querying CloudWatch logs and metrics
- Checking system health across multiple AWS services
- Executing diagnostic commands via Code Interpreter
- Generating incident reports with root cause analysis

**Why This Demo?**
This prototype showcases mydevopsproject.io's capability to deliver production-ready agentic workflows for enterprise clients, demonstrating:
- Technical depth in AWS infrastructure
- Real-world problem-solving with AI agents
- Rapid deployment and customization capabilities

---

## Prerequisites

### Required Software
- **Node.js**: v22.16.0 or higher
- **npm**: v10.9.2 or higher
- **Git**: v2.39.0 or higher
- **Python**: v3.13.2 or higher
- **AWS CLI**: v1.44.79 or higher

### Required AWS Resources
- Active AWS Account
- IAM User with Administrator Access (or permissions for CDK, Cognito, Lambda, API Gateway, DynamoDB, Amplify, CloudWatch, X-Ray)
- AWS Access Key ID and Secret Access Key

### Verification Commands
```bash
# Check installed versions
node --version
npm --version
git --version
python --version
aws --version
```

---

## Environment Setup

### System Information
- **Platform:** Windows (MINGW64_NT-10.0-19045)
- **Working Directory:** C:\Users\youruser\Documents\AWS\FAST
- **Git Repository:** Not initialized (will clone FAST)

---

## AWS CLI Installation & Configuration

### Step 1: Install AWS CLI

**Using pip (Recommended for Windows):**
```bash
pip install awscli --upgrade --user
```

**Expected Output:**
```
Successfully installed awscli-1.44.79 botocore-1.42.89 docutils-0.19 jmespath-1.1.0 rsa-4.7.2 s3transfer-0.16.0
```

### Step 2: Add AWS CLI to PATH (For Current Session)

```bash
export PATH="$PATH:/usr/local/bin"
```

**Verify Installation:**
```bash
aws --version
```

**Expected Output:**
```
aws-cli/1.44.79 Python/3.13.2 Windows/10 botocore/1.42.89
```

### Step 3: Configure AWS Credentials

**Important:** You'll need:
1. AWS Access Key ID
2. AWS Secret Access Key
3. Default region (recommended: us-east-1)

**How to Get AWS Credentials:**
1. Log into AWS Console
2. Navigate to: IAM → Users → [Your User] → Security Credentials
3. Click "Create Access Key"
4. Choose "Command Line Interface (CLI)" as use case
5. Copy Access Key ID and Secret Access Key

**Configuration Command:**
```bash
aws configure
```

**You'll be prompted for:**
```
AWS Access Key ID [None]: YOUR_ACCESS_KEY_ID
AWS Secret Access Key [None]: YOUR_SECRET_ACCESS_KEY
Default region name [None]: us-east-1
Default output format [None]: json
```

**Verify Configuration:**
```bash
aws sts get-caller-identity
```

**Expected Output:**
```json
{
    "UserId": "AIXXXXXXXXXXXXX",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/your-username"
}
```

---

## Clone FAST Repository

### Step 1: Clone the Repository

```bash
git clone https://github.com/aws-samples/sample-amazon-bedrock-agentcore-fullstack-webapp.git
cd sample-amazon-bedrock-agentcore-fullstack-webapp
```

### Step 2: Review Repository Structure

```bash
ls -la
```

**Expected Directory Structure:**
```
/backend          - CDK infrastructure code
/frontend         - React application
/docs             - Documentation
package.json      - Project dependencies
README.md         - Setup instructions
```

### Step 3: Install Dependencies

```bash
npm install
```

---

## Customize for DevOps Incident Response

### Use Case Overview

**Agent Name:** DevOps Incident Response Agent
**Primary Functions:**
1. CloudWatch log analysis
2. Metrics retrieval and anomaly detection
3. System health checks across AWS services
4. Diagnostic code execution
5. Incident report generation

### Customization Steps

#### 1. Update Agent Configuration

**File:** `backend/lib/agent-config.ts` (or similar)

```typescript
// Agent system prompt customization
const SYSTEM_PROMPT = `
You are a DevOps Incident Response Agent designed to help engineering teams
diagnose and resolve production incidents quickly.

Your capabilities:
1. Query CloudWatch Logs for error patterns and anomalies
2. Retrieve and analyze CloudWatch Metrics
3. Check health status of AWS services (EC2, RDS, Lambda, etc.)
4. Execute diagnostic Python scripts via Code Interpreter
5. Generate structured incident reports

When responding to incidents:
- Start with a quick summary of system health
- Identify the most likely root cause
- Provide actionable remediation steps
- Use data-driven insights from logs and metrics
- Escalate to human engineers when necessary

Always prioritize accuracy and clarity in high-pressure situations.
`;
```

#### 2. Configure MCP Tools (Model Context Protocol)

**Tools to Enable:**
- CloudWatch Logs API access
- CloudWatch Metrics API access
- EC2 DescribeInstances API
- RDS DescribeDBInstances API
- Lambda ListFunctions API

**File:** `backend/lib/mcp-tools.ts` (or gateway configuration)

```typescript
const devOpsTools = [
  {
    name: "query_cloudwatch_logs",
    description: "Query CloudWatch Logs for a specific log group and time range",
    parameters: {
      logGroupName: "string",
      startTime: "timestamp",
      endTime: "timestamp",
      filterPattern: "string"
    }
  },
  {
    name: "get_cloudwatch_metrics",
    description: "Retrieve CloudWatch metrics for monitoring",
    parameters: {
      namespace: "string",
      metricName: "string",
      dimensions: "object",
      startTime: "timestamp",
      endTime: "timestamp"
    }
  },
  {
    name: "check_service_health",
    description: "Check health status of AWS services",
    parameters: {
      serviceType: "string", // ec2, rds, lambda, etc.
      resourceIds: "array"
    }
  }
];
```

#### 3. Update Frontend UI

**File:** `frontend/src/components/ChatInterface.tsx` (or similar)

**Branding Changes:**
- Update logo to mydevopsproject.io branding
- Change application title to "DevOps Incident Response Agent - Powered by mydevopsproject.io"
- Customize color scheme to match company branding

**Sample Chat Prompts:**
```typescript
const samplePrompts = [
  "What's the current health status of our production environment?",
  "Show me error logs from the last 30 minutes",
  "Analyze CPU and memory metrics for instance i-1234567890",
  "Generate an incident report for the recent API latency spike"
];
```

#### 4. Configure Environment Variables

**File:** `backend/.env` or CDK context

```bash
# Application Configuration
APP_NAME=devops-incident-response-agent
COMPANY_NAME=mydevopsproject
ENVIRONMENT=demo

# AWS Region
AWS_REGION=us-east-1

# Bedrock Configuration
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0
BEDROCK_REGION=us-east-1

# Agent Configuration
AGENT_MEMORY_ENABLED=true
AGENT_CODE_INTERPRETER_ENABLED=true
AGENT_OBSERVABILITY_ENABLED=true

# CloudWatch Configuration
LOG_RETENTION_DAYS=7
ENABLE_XRAY_TRACING=true
```

---

## Deploy to AWS

### Step 1: Bootstrap AWS CDK (First Time Only)

```bash
npx cdk bootstrap aws://ACCOUNT-NUMBER/REGION
```

**Replace:**
- `ACCOUNT-NUMBER` with your AWS account ID
- `REGION` with your chosen region (e.g., us-east-1)

**Example:**
```bash
npx cdk bootstrap aws://123456789012/us-east-1
```

### Step 2: Review CDK Stacks

```bash
npx cdk list
```

**Expected Output:**
```
FastStack
FastFrontendStack
```

### Step 3: Synthesize CloudFormation Templates

```bash
npx cdk synth
```

This generates CloudFormation templates and validates your CDK code.

### Step 4: Deploy Infrastructure

```bash
npx cdk deploy --all
```

**What Gets Deployed:**
1. **Amazon Cognito** - User authentication
2. **AWS Lambda** - AgentCore runtime functions
3. **API Gateway** - REST API endpoints
4. **DynamoDB** - Agent memory storage
5. **AWS Amplify** - Frontend hosting
6. **CloudWatch** - Logging and metrics
7. **X-Ray** - Distributed tracing
8. **IAM Roles** - Permissions for services

**Deployment Time:** 15-25 minutes

**During Deployment:**
- You'll see progress for each stack
- CloudFormation will create resources sequentially
- You may be asked to confirm security-sensitive changes (type 'y' to proceed)

**Expected Output:**
```
✅  FastStack
✅  FastFrontendStack

Outputs:
FastStack.ApiEndpoint = https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod
FastStack.CognitoUserPoolId = us-east-1_XXXXXXXXX
FastStack.CognitoClientId = xxxxxxxxxxxxxxxxxxxxxxxxxx
FastFrontendStack.FrontendUrl = https://main.xxxxxxxxxxxxx.amplifyapp.com
```

**IMPORTANT:** Save these output values - you'll need them for configuration!

### Step 5: Verify Deployment

```bash
# Check CloudFormation stacks
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE

# Check Cognito user pool
aws cognito-idp list-user-pools --max-results 10

# Test API endpoint
curl https://YOUR_API_ENDPOINT/health
```

---

## Post-Deployment Configuration

### Step 1: Create Test User in Cognito

```bash
aws cognito-idp admin-create-user \
  --user-pool-id YOUR_USER_POOL_ID \
  --username testuser@example.com \
  --user-attributes Name=email,Value=testuser@example.com \
  --temporary-password TempPassword123! \
  --message-action SUPPRESS
```

### Step 2: Set Permanent Password

```bash
aws cognito-idp admin-set-user-password \
  --user-pool-id YOUR_USER_POOL_ID \
  --username testuser@example.com \
  --password YourSecurePassword123! \
  --permanent
```

### Step 3: Configure CloudWatch Access Permissions

The deployed Lambda functions need permissions to read CloudWatch Logs and Metrics. Verify the IAM role has these policies:

```bash
# Get Lambda execution role
aws lambda get-function --function-name AGENT_FUNCTION_NAME --query 'Configuration.Role'

# Verify attached policies
aws iam list-attached-role-policies --role-name LAMBDA_ROLE_NAME
```

**Required Policies:**
- CloudWatchLogsReadOnlyAccess
- CloudWatchReadOnlyAccess
- AmazonEC2ReadOnlyAccess (for service health checks)

**Add Policy if Missing:**
```bash
aws iam attach-role-policy \
  --role-name LAMBDA_ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsReadOnlyAccess
```

---

## Testing & Validation

### Step 1: Access the Frontend

Open the Frontend URL from deployment outputs:
```
https://main.xxxxxxxxxxxxx.amplifyapp.com
```

### Step 2: Login with Test User

- **Username:** testuser@example.com
- **Password:** YourSecurePassword123!

### Step 3: Test Agent Capabilities

**Test Prompt 1: System Health Check**
```
What's the current health status of our AWS environment?
```

**Test Prompt 2: CloudWatch Logs Query**
```
Show me any error logs from the last hour in the application log group
```

**Test Prompt 3: Metrics Analysis**
```
Analyze CPU utilization for EC2 instances over the last 4 hours
```

**Test Prompt 4: Code Interpreter**
```
Write a Python script to calculate the average response time from these API logs
```

### Step 4: Verify Observability

**Check CloudWatch Logs:**
```bash
aws logs describe-log-groups --log-group-name-prefix /aws/lambda/
```

**Check X-Ray Traces:**
```bash
aws xray get-trace-summaries --start-time $(date -u -d '1 hour ago' +%s) --end-time $(date -u +%s)
```

---

## Troubleshooting

### Issue 1: CDK Deploy Fails with Permission Errors

**Solution:**
- Verify IAM user has AdministratorAccess or required permissions
- Check AWS credentials: `aws sts get-caller-identity`
- Ensure CDK bootstrap was run: `npx cdk bootstrap`

### Issue 2: Frontend Not Loading

**Solution:**
- Check Amplify deployment status in AWS Console
- Verify API endpoint is correctly configured in frontend environment variables
- Check browser console for CORS errors

### Issue 3: Agent Not Responding

**Solution:**
- Check Lambda function logs: `aws logs tail /aws/lambda/FUNCTION_NAME --follow`
- Verify Bedrock model access in your region
- Check API Gateway logs for request/response details

### Issue 4: Authentication Fails

**Solution:**
- Verify Cognito user pool and client IDs match frontend configuration
- Check user exists: `aws cognito-idp list-users --user-pool-id YOUR_POOL_ID`
- Reset user password if needed

### Issue 5: AWS CLI Command Not Found

**Solution:**
```bash
# Add to PATH for current session
export PATH="$PATH:/usr/local/bin"

# Verify
aws --version
```

---

## Useful Commands Reference

### AWS CLI
```bash
# Configure credentials
aws configure

# Check identity
aws sts get-caller-identity

# List CloudFormation stacks
aws cloudformation list-stacks

# Describe specific stack
aws cloudformation describe-stacks --stack-name FastStack
```

### CDK Commands
```bash
# List all stacks
npx cdk list

# Synthesize CloudFormation
npx cdk synth

# Show differences
npx cdk diff

# Deploy all stacks
npx cdk deploy --all

# Destroy all resources
npx cdk destroy --all
```

### CloudWatch
```bash
# Tail Lambda logs
aws logs tail /aws/lambda/FUNCTION_NAME --follow

# List log groups
aws logs describe-log-groups

# Query logs
aws logs filter-log-events --log-group-name GROUP_NAME --filter-pattern "ERROR"
```

### Cognito
```bash
# List user pools
aws cognito-idp list-user-pools --max-results 10

# List users
aws cognito-idp list-users --user-pool-id POOL_ID

# Create user
aws cognito-idp admin-create-user --user-pool-id POOL_ID --username USERNAME
```

---

## Next Steps for Client Demos

### 1. Customize Branding
- Replace logos and colors with client branding
- Update agent name and description
- Customize sample prompts for client use cases

### 2. Add Client-Specific Data
- Connect to client's CloudWatch log groups
- Configure access to client's AWS resources
- Load client-specific knowledge base

### 3. Prepare Demo Script
- Create realistic incident scenarios
- Prepare sample log data
- Document expected agent responses

### 4. Measure Success Metrics
- Time to diagnose incident (before/after agent)
- Accuracy of root cause identification
- Reduction in mean time to resolution (MTTR)

---

## Resources

- **FAST Repository:** https://github.com/aws-samples/sample-amazon-bedrock-agentcore-fullstack-webapp
- **AWS Bedrock Documentation:** https://docs.aws.amazon.com/bedrock/
- **AgentCore Documentation:** https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html
- **mydevopsproject.io GitHub:** https://github.com/chiragbarsaiya

---

## Support

For questions or issues:
- **Email:** your-email@example.com
- **GitHub Issues:** https://github.com/chiragbarsaiya/devops-incident-agent/issues

---

**Document Version:** 1.0
**Last Updated:** April 16, 2026
**Maintained By:** mydevopsproject.io Engineering Team
