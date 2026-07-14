# DevOps Agent Demo - Test Infrastructure

This directory contains everything needed to deploy and manage test Lambda functions for realistic DevOps incident demonstrations.

## 📋 Contents

- **deploy-test-lambdas.yaml** - CloudFormation template that deploys 4 Lambda functions, EventBridge schedules, and CloudWatch alarms
- **lambda-error-simulator.py** - Detailed Python code for the error simulator (reference implementation)
- **deploy.sh** - Bash script to automate deployment
- **cleanup.sh** - Bash script to remove all test resources

## 🚀 Quick Start

### Deploy Test Infrastructure

**Option 1: Using CloudFormation Directly**

```bash
cd /path/to/your/project/test-scenarios

export MSYS_NO_PATHCONV=1

"/c/Program Files/Amazon/AWSCLIV2/aws" cloudformation create-stack \
  --stack-name devops-agent-demo-lambdas \
  --template-body file://deploy-test-lambdas.yaml \
  --capabilities CAPABILITY_IAM \
  --parameters ParameterKey=ErrorRate,ParameterValue=30 \
  --region us-east-1

# Wait for creation
"/c/Program Files/Amazon/AWSCLIV2/aws" cloudformation wait stack-create-complete \
  --stack-name devops-agent-demo-lambdas \
  --region us-east-1

echo "Deployment complete!"
```

**Option 2: Using Deploy Script**

```bash
cd /path/to/your/project/test-scenarios
bash deploy.sh
```

### Generate Initial Test Data

```bash
# Invoke each function 10 times
for func in demo-error-simulator demo-slow-response demo-api-errors demo-high-memory; do
  echo "Invoking $func..."
  for i in {1..10}; do
    "/c/Program Files/Amazon/AWSCLIV2/aws" lambda invoke \
      --function-name $func \
      --region us-east-1 \
      --log-type None \
      /dev/null &> /dev/null
    sleep 1
  done
  echo "Done!"
done
```

**Wait 2-3 minutes** for CloudWatch Logs to be available.

### Verify Deployment

```bash
# List Lambda functions
"/c/Program Files/Amazon/AWSCLIV2/aws" lambda list-functions \
  --query 'Functions[?starts_with(FunctionName, `demo-`)].FunctionName' \
  --region us-east-1

# Check CloudWatch Log Groups
"/c/Program Files/Amazon/AWSCLIV2/aws" logs describe-log-groups \
  --log-group-name-prefix /aws/lambda/demo- \
  --region us-east-1
```

## 📦 What Gets Deployed

### Lambda Functions (4)

1. **demo-error-simulator**
   - Runtime: Python 3.11
   - Memory: 256 MB
   - Purpose: Generates random errors (database, timeout, memory, API, exceptions)
   - Error Rate: 30% (configurable via CloudFormation parameter)
   - Auto-invoked every 5 minutes via EventBridge

2. **demo-slow-response**
   - Runtime: Python 3.11
   - Memory: 128 MB
   - Purpose: Simulates slow operations (2-8 second delays)
   - Logs warnings when queries exceed 5 seconds
   - Auto-invoked every 5 minutes via EventBridge

3. **demo-api-errors**
   - Runtime: Python 3.11
   - Memory: 128 MB
   - Purpose: Generates various HTTP error codes (400, 401, 403, 404, 500, 502, 503)
   - Randomly selects error type on each invocation
   - Auto-invoked every 5 minutes via EventBridge

4. **demo-high-memory**
   - Runtime: Python 3.11
   - Memory: 512 MB
   - Purpose: Simulates memory-intensive operations
   - Occasionally triggers memory warnings
   - Can be invoked manually to test memory issues

### EventBridge Rules (3)

- Automatically invoke demo functions every 5 minutes
- Ensures continuous log data generation
- Can be disabled by updating stack parameter

### CloudWatch Alarms (2)

1. **demo-error-simulator-high-errors**
   - Triggers when error count > 3 in 5 minutes
   - Useful for demonstrating alarm integration

2. **demo-slow-response-high-duration**
   - Triggers when average duration > 5 seconds
   - Useful for performance monitoring demos

### IAM Role

- Least-privilege execution role for Lambda functions
- Includes CloudWatch Logs permissions
- Includes CloudWatch Metrics permissions

## 🎯 Use Cases

### Demo Scenario 1: Error Investigation
Use `demo-error-simulator` to demonstrate:
- Querying CloudWatch logs for error patterns
- Identifying different error types
- Analyzing error frequency

**Agent Prompts:**
```
Query CloudWatch logs for log group /aws/lambda/demo-error-simulator for ERROR patterns in the last hour
```

### Demo Scenario 2: Performance Analysis
Use `demo-slow-response` to demonstrate:
- Identifying slow functions
- Analyzing duration metrics
- Correlating slow queries with logs

**Agent Prompts:**
```
Show me CloudWatch metrics for AWS/Lambda namespace for demo-slow-response function
Query CloudWatch logs for log group /aws/lambda/demo-slow-response for WARN patterns in the last hour
```

### Demo Scenario 3: API Error Troubleshooting
Use `demo-api-errors` to demonstrate:
- Categorizing different error types
- Counting error occurrences
- Identifying error patterns

**Agent Prompts:**
```
Query CloudWatch logs for log group /aws/lambda/demo-api-errors for ERROR patterns showing HTTP status codes in the last hour
```

### Demo Scenario 4: Memory Issues
Use `demo-high-memory` to demonstrate:
- Memory usage analysis
- Calculating memory requirements
- Optimization recommendations

**Agent Prompts:**
```
Check the health status of demo-high-memory Lambda function
Query CloudWatch logs for log group /aws/lambda/demo-high-memory for MemoryError patterns in the last 2 hours
```

## 🔧 Configuration

### Adjust Error Rate

Update the `ErrorRate` parameter (0-100):

```bash
"/c/Program Files/Amazon/AWSCLIV2/aws" cloudformation update-stack \
  --stack-name devops-agent-demo-lambdas \
  --template-body file://deploy-test-lambdas.yaml \
  --capabilities CAPABILITY_IAM \
  --parameters ParameterKey=ErrorRate,ParameterValue=50 \
  --region us-east-1
```

### Disable Auto-Invocation

If you want to manually control when functions are invoked:

1. Edit `deploy-test-lambdas.yaml`
2. Change EventBridge Rule `State` from `ENABLED` to `DISABLED`
3. Update the stack

### Change Invocation Frequency

Edit EventBridge `ScheduleExpression`:
- Current: `rate(5 minutes)`
- Options: `rate(1 minute)`, `rate(10 minutes)`, `cron(0/5 * * * ? *)`

## 🧹 Cleanup

### Option 1: Using Cleanup Script

```bash
cd /path/to/your/project/test-scenarios
bash cleanup.sh
```

### Option 2: Manual Cleanup

```bash
# Delete CloudFormation stack
"/c/Program Files/Amazon/AWSCLIV2/aws" cloudformation delete-stack \
  --stack-name devops-agent-demo-lambdas \
  --region us-east-1

# Wait for deletion
"/c/Program Files/Amazon/AWSCLIV2/aws" cloudformation wait stack-delete-complete \
  --stack-name devops-agent-demo-lambdas \
  --region us-east-1

# Optionally delete log groups (they persist after Lambda deletion)
for log_group in /aws/lambda/demo-error-simulator /aws/lambda/demo-slow-response /aws/lambda/demo-api-errors /aws/lambda/demo-high-memory; do
  "/c/Program Files/Amazon/AWSCLIV2/aws" logs delete-log-group \
    --log-group-name "$log_group" \
    --region us-east-1
done
```

## 💰 Cost Considerations

- **Lambda invocations**: First 1M requests/month free
  - 4 functions × 12/hour × 720 hours = ~35,000 invocations/month = **FREE**
- **Lambda compute**: First 400,000 GB-seconds/month free
  - Estimated usage: ~10,000 GB-seconds/month = **FREE**
- **CloudWatch Logs**: First 5 GB ingestion free
  - Estimated: <500 MB/month = **FREE**
- **EventBridge**: First 1M events/month free
  - ~35,000 events/month = **FREE**

**Total monthly cost**: $0 (within AWS Free Tier)

## 🚨 Troubleshooting

### Issue: Lambda functions not generating logs

**Check if functions exist:**
```bash
"/c/Program Files/Amazon/AWSCLIV2/aws" lambda list-functions --query 'Functions[?starts_with(FunctionName, `demo-`)].FunctionName' --region us-east-1
```

**Manually invoke:**
```bash
"/c/Program Files/Amazon/AWSCLIV2/aws" lambda invoke --function-name demo-error-simulator --region us-east-1 response.json
cat response.json
```

**Check EventBridge rules:**
```bash
"/c/Program Files/Amazon/AWSCLIV2/aws" events list-rules --name-prefix demo- --region us-east-1
```

### Issue: CloudFormation stack creation failed

**Get failure reason:**
```bash
"/c/Program Files/Amazon/AWSCLIV2/aws" cloudformation describe-stack-events \
  --stack-name devops-agent-demo-lambdas \
  --query 'StackEvents[?ResourceStatus==`CREATE_FAILED`]' \
  --region us-east-1
```

Common fixes:
- Ensure IAM permissions to create Lambda, EventBridge, CloudWatch resources
- Check if functions with same names already exist
- Verify CloudFormation quota limits

### Issue: Agent says "No log data found"

**Verify log groups exist:**
```bash
"/c/Program Files/Amazon/AWSCLIV2/aws" logs describe-log-groups --log-group-name-prefix /aws/lambda/demo- --region us-east-1
```

**Check recent log streams:**
```bash
"/c/Program Files/Amazon/AWSCLIV2/aws" logs describe-log-streams \
  --log-group-name /aws/lambda/demo-error-simulator \
  --order-by LastEventTime \
  --descending \
  --max-items 5 \
  --region us-east-1
```

**Wait time**: CloudWatch Logs can take 2-3 minutes to be queryable after Lambda execution.

## 📚 Additional Resources

- **Incident Response Playbook**: `../INCIDENT_RESPONSE_PLAYBOOK.md`
- **Demo Script**: `../CLIENT_DEMO_SCRIPT.md`
- **Quick Reference**: `../DEMO_FLOW_QUICK_REFERENCE.md`
- **Summary**: `../DEMO_READY_SUMMARY.md`

## 🔐 Security Notes

- All Lambda functions are read-only (no write operations to AWS services)
- IAM role follows least-privilege principle
- Functions only write to CloudWatch Logs
- No external API calls (all simulated)
- Safe to run in production AWS accounts

## 📝 Customization Ideas

### Add More Error Types
Edit the Lambda function code in CloudFormation template to add:
- Network errors
- Permission denied errors
- Rate limiting errors
- Dependency failures

### Integrate with Real Services
Replace simulated errors with actual service calls:
- Connect to real RDS database
- Call real external APIs
- Read from DynamoDB tables

### Add Metrics Publishing
Enhance functions to publish custom CloudWatch metrics:
```python
import boto3
cloudwatch = boto3.client('cloudwatch')

cloudwatch.put_metric_data(
    Namespace='DemoApp',
    MetricData=[{
        'MetricName': 'ErrorRate',
        'Value': error_count,
        'Unit': 'Count'
    }]
)
```

## 🎯 Best Practices

1. **Before demos**: Manually invoke functions to ensure fresh logs
2. **After demos**: Leave EventBridge rules enabled for continuous data
3. **Cost control**: Monitor with AWS Budget alerts
4. **Cleanup**: Remove test infrastructure after demo period ends
5. **Documentation**: Keep this README updated with customizations

---

**Status**: ✅ DEPLOYED AND READY
**Last Updated**: 2026-04-16
**Maintained By**: mydevopsproject.io Team
