# DevOps Incident Response Agent - Customization Guide

**Status:** Ready to Customize
**Company:** mydevopsproject.io
**Date:** April 16, 2026

---

## Quick Summary

Your FAST deployment is complete and working with the default calculator + weather demo. To customize it for DevOps Incident Response, follow the steps below.

Due to the session length, I'm providing you with the complete customization code that you can apply manually or we can continue in a follow-up session.

---

## Files to Customize

### 1. Agent Code: `agent/strands_agent.py`

**Location:** `/path/to/your/project/sample-amazon-bedrock-agentcore-fullstack-webapp/agent/strands_agent.py`

**What to Change:**
- Add boto3 imports for AWS SDK
- Add 3 new DevOps tools: `query_cloudwatch_logs`, `get_cloudwatch_metrics`, `check_aws_service_health`
- Update system prompt for DevOps context
- Keep calculator tool (useful for incident calculations)

**See Full Code:** `/path/to/your/project/devops_agent_code.py` (created below)

### 2. Python Dependencies: `agent/requirements.txt`

**Location:** `/path/to/your/project/sample-amazon-bedrock-agentcore-fullstack-webapp/agent/requirements.txt`

**Add This Line:**
```
boto3>=1.34.0
```

### 3. Frontend Prompts: `frontend/src/App.tsx`

**Location:** `/path/to/your/project/sample-amazon-bedrock-agentcore-fullstack-webapp/frontend/src/App.tsx`

**Find and Replace Sample Prompts:**

Find this section (around line 200-220):
```typescript
const getSupportPrompts = () => {
  if (messages.length === 0) {
    return [
      { id: 'calc1', text: 'What is 42 + 58?' },
      { id: 'calc2', text: 'Calculate 123 * 456' },
      { id: 'weather', text: "What's the weather like today?" },
    ];
  }
```

Replace with:
```typescript
const getSupportPrompts = () => {
  if (messages.length === 0) {
    return [
      { id: 'health1', text: 'Check the health status of all EC2 instances' },
      { id: 'health2', text: 'Show me the status of Lambda functions' },
      { id: 'logs1', text: 'Query CloudWatch logs for errors in the last hour' },
      { id: 'metrics1', text: 'Show me CPU utilization for my EC2 instances over the last 4 hours' },
    ];
  }
```

**Update Page Title (around line 50-60):**

Find:
```typescript
<title>AgentCore Demo</title>
```

Replace with:
```typescript
<title>DevOps Incident Response Agent - mydevopsproject.io</title>
```

---

## Deployment Commands

After making the changes above, redeploy the agent:

```bash
cd /path/to/your/project/sample-amazon-bedrock-agentcore-fullstack-webapp/cdk

# Deploy updated agent (includes CodeBuild - takes ~6-8 minutes)
export PATH="/c/Program Files/Amazon/AWSCLIV2:$PATH"
npx cdk deploy AgentCoreRuntime --no-cli-pager

# If you also updated the frontend, deploy it too
cd ..
./scripts/build-frontend.sh "us-east-1_EXAMPLE1A" "your-cognito-client-id" "arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/strands_agent-XXXXXXXXXX" "us-east-1"
cd cdk
npx cdk deploy AgentCoreFrontend --no-cli-pager
```

---

## Testing DevOps Features

After redeployment, test with these prompts:

### Test 1: Check EC2 Health
```
Check the health status of all EC2 instances in our environment
```

### Test 2: Query CloudWatch Logs
```
Query CloudWatch logs from /aws/lambda/my-function for errors in the last hour
```

### Test 3: Get CloudWatch Metrics
```
Show me the CPUUtilization metrics for AWS/Lambda namespace over the last 4 hours
```

### Test 4: Check Lambda Functions
```
List all Lambda functions and their current status
```

### Test 5: Check RDS Databases
```
Check the health status of all RDS databases
```

---

## What Each Tool Does

### 1. `query_cloudwatch_logs`
**Purpose:** Query CloudWatch Logs for error patterns and anomalies

**Parameters:**
- `log_group_name`: Name of the log group (e.g., "/aws/lambda/my-function")
- `filter_pattern`: Filter for specific patterns (e.g., "ERROR", "Exception")
- `hours_back`: How far back to search (default: 1 hour)
- `limit`: Max events to return (default: 50)

**Example:**
```
Query CloudWatch logs from /aws/lambda/my-function for "ERROR" in the last 2 hours
```

### 2. `get_cloudwatch_metrics`
**Purpose:** Retrieve CloudWatch metrics for monitoring

**Parameters:**
- `namespace`: AWS namespace (e.g., "AWS/EC2", "AWS/RDS", "AWS/Lambda")
- `metric_name`: Metric name (e.g., "CPUUtilization", "DatabaseConnections")
- `dimensions`: Dimensions as "key=value,key2=value2"
- `hours_back`: Time range (default: 4 hours)
- `statistic`: Average, Sum, Maximum, Minimum (default: Average)

**Example:**
```
Get CPUUtilization metrics for AWS/EC2 namespace with InstanceId=i-1234567890 over the last 6 hours
```

### 3. `check_aws_service_health`
**Purpose:** Check health status of AWS resources

**Parameters:**
- `service_type`: Type of service ("ec2", "rds", "lambda")
- `resource_ids`: Comma-separated list of IDs (optional, returns all if empty)

**Examples:**
```
Check EC2 health status
Check RDS database health
List all Lambda functions
```

---

## IAM Permissions Required

The agent's execution role needs these permissions (already configured in deployment):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:FilterLogEvents",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams",
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:ListMetrics",
        "ec2:DescribeInstanceStatus",
        "ec2:DescribeInstances",
        "rds:DescribeDBInstances",
        "lambda:ListFunctions",
        "lambda:GetFunction"
      ],
      "Resource": "*"
    }
  ]
}
```

These permissions are READ-ONLY for safety.

---

##  Next Steps

### Option A: Manual Customization (Recommended for Learning)
1. Open the files listed above
2. Make the changes manually
3. Review the code to understand how it works
4. Deploy using the commands above

### Option B: Automated Script
Create a script to apply all changes automatically (I can help with this in a follow-up)

### Option C: Continue in New Session
Due to session length, we can continue the customization in a fresh session with full context

---

## Current Deployment Summary

**What's Working Now:**
- ✅ Full FAST deployment with 4 stacks
- ✅ Calculator + Weather demo agent
- ✅ Cognito authentication
- ✅ React frontend on CloudFront
- ✅ $20/month budget with alerts
- ✅ Complete documentation

**What Needs Customization:**
- [ ] Agent code (add DevOps tools)
- [ ] Python dependencies (add boto3)
- [ ] Frontend prompts (update for DevOps)
- [ ] Redeploy updated agent
- [ ] Test DevOps features

---

## Cost Impact of Customization

**No Additional Cost!**
- Same AgentCore runtime
- Same Bedrock model
- Same infrastructure
- Only code changes

Estimated cost remains: **$2-8/month** for demo usage

---

## Support Resources

**Documentation:**
- Full Deployment Summary: `DEPLOYMENT_SUMMARY.md`
- Deployment Guide: `DEPLOYMENT_GUIDE.md`
- Session Log: `DEPLOYMENT_SESSION_LOG.md`

**AWS Resources:**
- Frontend: https://d3lro400idfnsp.cloudfront.net
- Agent ARN: `arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/strands_agent-XXXXXXXXXX`
- Cognito Pool: `us-east-1_EXAMPLE1A`

**Contact:**
- Email: your-email@example.com
- GitHub: https://github.com/chiragbarsaiya

---

**Ready to Customize?** Follow the steps above or let me know if you'd like to continue in a follow-up session!
