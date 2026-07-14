# DevOps Agent - Incident Response Playbook
## Test Scenarios & Agent Demonstration Guide

---

## Table of Contents
1. [Setup Instructions](#setup-instructions)
2. [Test Scenario 1: Lambda Function Errors](#scenario-1-lambda-function-errors)
3. [Test Scenario 2: High Latency Investigation](#scenario-2-high-latency-investigation)
4. [Test Scenario 3: Memory Issues](#scenario-3-memory-issues)
5. [Test Scenario 4: API Gateway Errors](#scenario-4-api-gateway-errors)
6. [Test Scenario 5: Multi-Service Health Check](#scenario-5-multi-service-health-check)
7. [Test Scenario 6: Cost Analysis](#scenario-6-cost-analysis)
8. [Agent Testing Checklist](#agent-testing-checklist)
9. [Troubleshooting Guide](#troubleshooting-guide)

---

## Setup Instructions

### Prerequisites
- AWS account with appropriate permissions
- DevOps Agent deployed and accessible at: https://d3lro400idfnsp.cloudfront.net
- AWS CLI configured
- Test Lambda functions deployed (optional but recommended)

### Deploy Test Infrastructure

**Option 1: Deploy Test Lambda Functions (Recommended)**

```bash
cd /path/to/your/project/test-scenarios

# Deploy the CloudFormation stack
aws cloudformation create-stack \
  --stack-name devops-agent-demo-lambdas \
  --template-body file://deploy-test-lambdas.yaml \
  --capabilities CAPABILITY_IAM \
  --parameters ParameterKey=ErrorRate,ParameterValue=30 \
  --region us-east-1

# Wait for stack creation (takes ~2-3 minutes)
aws cloudformation wait stack-create-complete \
  --stack-name devops-agent-demo-lambdas \
  --region us-east-1

# Get stack outputs
aws cloudformation describe-stacks \
  --stack-name devops-agent-demo-lambdas \
  --query 'Stacks[0].Outputs' \
  --region us-east-1
```

**Option 2: Use Existing AWS Resources**

If you already have Lambda functions, EC2 instances, or other AWS resources, you can use those for demonstrations.

### Verify Deployment

```bash
# List deployed Lambda functions
aws lambda list-functions \
  --query 'Functions[?starts_with(FunctionName, `demo-`)].FunctionName' \
  --region us-east-1

# Expected output:
# [
#   "demo-error-simulator",
#   "demo-high-memory",
#   "demo-slow-response",
#   "demo-api-errors"
# ]
```

### Generate Initial Test Data

Trigger the Lambda functions manually to create log entries:

```bash
# Invoke error simulator
aws lambda invoke \
  --function-name demo-error-simulator \
  --region us-east-1 \
  response1.json

# Invoke slow response function
aws lambda invoke \
  --function-name demo-slow-response \
  --region us-east-1 \
  response2.json

# Invoke API error function
aws lambda invoke \
  --function-name demo-api-errors \
  --region us-east-1 \
  response3.json

# Invoke multiple times to generate more data
for i in {1..10}; do
  aws lambda invoke --function-name demo-error-simulator --region us-east-1 /dev/null
  sleep 2
done
```

**Wait 2-3 minutes** for CloudWatch Logs to be available before testing agent.

---

## Scenario 1: Lambda Function Errors

### Incident Description
**Alert**: CloudWatch Alarm triggered - High error rate on Lambda function `demo-error-simulator`

**Symptoms**:
- Users reporting API failures
- Error rate increased from 2% to 30%
- Multiple error types in logs

### Agent Investigation Steps

**Step 1: Check Lambda Function Health**

Navigate to DevOps Agent: https://d3lro400idfnsp.cloudfront.net

**Prompt:**
```
Check the health status of all Lambda functions
```

**Expected Agent Response:**
- Lists all Lambda functions including demo-error-simulator
- Shows function configuration (runtime, memory, timeout)
- Displays last modified time

**What to Look For:**
- Is the function configuration correct?
- Has it been recently modified (potential bad deployment)?
- What is the timeout setting?

---

**Step 2: Query Error Logs**

**Prompt:**
```
Query CloudWatch logs for log group /aws/lambda/demo-error-simulator for ERROR patterns in the last hour
```

**Expected Agent Response:**
- Filtered log events containing ERROR
- Timestamps of when errors occurred
- Specific error messages (DatabaseConnectionError, MemoryError, etc.)

**What to Look For:**
- What types of errors are occurring?
- Are errors clustered at specific times?
- Do error messages indicate root cause?

**Sample Errors You Might See:**
```
[ERROR] Database connection failed to demo-db.us-east-1.rds.amazonaws.com
[ERROR] External API call timed out after 30 seconds
[ERROR] MemoryError: Cannot allocate array - insufficient memory
[ERROR] Validation failed: Missing required field 'user_id'
```

---

**Step 3: Analyze Error Metrics**

**Prompt:**
```
Show me CloudWatch metrics for AWS/Lambda namespace, specifically for the demo-error-simulator function in the last 4 hours
```

**Expected Agent Response:**
- Invocation count over time
- Error count over time
- Duration metrics

**Follow-up Prompt:**
```
Based on the error logs and metrics, what is the error rate percentage in the last hour?
```

**Expected Agent Response:**
- Agent calculates error rate
- Example: "Based on the data, there were 30 errors out of 100 invocations = 30% error rate"

---

**Step 4: Root Cause Analysis**

Based on the error patterns, ask the agent:

**Prompt:**
```
Looking at the error logs, what are the top 3 error types and what could be causing them?
```

**Expected Agent Response:**
- Agent summarizes error types
- Provides potential root causes
- May suggest remediation steps

**Sample Root Causes:**
- `DatabaseConnectionError` → RDS instance might be down or security group blocking access
- `MemoryError` → Function needs more memory allocation
- `ValidationError` → Client sending malformed requests
- `Timeout` → External API slow or unreachable

---

**Step 5: Recommended Actions**

**Prompt:**
```
What steps should I take to resolve these Lambda errors?
```

**Expected Agent Response:**
- Actionable recommendations
- Prioritized list of fixes
- Links to relevant documentation (if configured)

---

### Resolution Steps

Based on agent findings, typical resolutions:

1. **Database Errors**: Check RDS instance status, security groups, connection limits
2. **Memory Errors**: Increase Lambda memory allocation from 256MB to 512MB or 1GB
3. **Timeout Errors**: Investigate external service, increase Lambda timeout, implement retries
4. **Validation Errors**: Fix client-side validation or add better error handling

### Validation

After implementing fixes:

**Prompt:**
```
Check the demo-error-simulator function again and compare error rates from the last 30 minutes vs the previous 30 minutes
```

---

## Scenario 2: High Latency Investigation

### Incident Description
**Alert**: API response times have increased from 200ms to 5+ seconds

**Symptoms**:
- Users complaining about slow application
- Timeout errors in frontend
- Database queries taking longer than usual

### Agent Investigation Steps

**Step 1: Identify Slow Functions**

**Prompt:**
```
Check the health status of all Lambda functions and identify any with high execution duration
```

**Expected Agent Response:**
- List of Lambda functions
- Configuration including timeout settings

---

**Step 2: Analyze Duration Metrics**

**Prompt:**
```
Show me CloudWatch metrics for AWS/Lambda namespace, focusing on Duration metric for demo-slow-response function in the last 2 hours
```

**Expected Agent Response:**
- Duration metrics over time
- Average, min, max duration values
- Timestamps of high-duration invocations

**What to Look For:**
- When did latency spike start?
- Is it trending up or down?
- Are there periodic spikes?

---

**Step 3: Query Slow Query Logs**

**Prompt:**
```
Query CloudWatch logs for log group /aws/lambda/demo-slow-response for WARN or ERROR patterns indicating slow performance in the last hour
```

**Expected Agent Response:**
```
[WARN] Simulating slow database query - expected delay: 6.84s
[ERROR] Query exceeded 5 second threshold - actual: 6.84s
[ERROR] Slow query detected - consider adding database index
```

**Follow-up Prompt:**
```
How many queries exceeded the 5 second threshold in the last hour?
```

---

**Step 4: Check Downstream Dependencies**

**Prompt:**
```
Check the status of all RDS database instances to see if database performance might be impacting Lambda
```

**Expected Agent Response:**
- RDS instance status
- Instance class and configuration
- Availability zone

**Follow-up for EC2:**
```
Check the status of all EC2 instances that might be hosting backend services
```

---

**Step 5: Correlation Analysis**

**Prompt:**
```
Compare the time when Lambda duration increased with any changes to EC2 or RDS instances. Did anything change around that time?
```

**Expected Agent Response:**
- Timeline correlation
- Potential causal relationships

---

### Resolution Steps

Based on agent findings:

1. **Database Slow**: Add indexes, scale up RDS instance, enable query caching
2. **External API Slow**: Implement caching, add circuit breaker, increase timeouts
3. **Lambda Cold Starts**: Enable provisioned concurrency, optimize package size
4. **Network Issues**: Check VPC configuration, NAT gateway, security groups

---

## Scenario 3: Memory Issues

### Incident Description
**Alert**: Lambda function `demo-high-memory` experiencing OOM (Out of Memory) errors

**Symptoms**:
- Function invocations failing intermittently
- "Task timed out" errors
- No response from function

### Agent Investigation Steps

**Step 1: Check Function Memory Configuration**

**Prompt:**
```
Check the health status of the demo-high-memory Lambda function and show me its memory configuration
```

**Expected Agent Response:**
- Function has 512MB memory allocated
- Runtime: Python 3.11
- Timeout: 30 seconds

---

**Step 2: Query Memory-Related Errors**

**Prompt:**
```
Query CloudWatch logs for log group /aws/lambda/demo-high-memory for MemoryError or "out of memory" patterns in the last 2 hours
```

**Expected Agent Response:**
```
[WARN] Memory usage at 85% - approaching limit
[ERROR] MemoryError: Cannot allocate memory
```

---

**Step 3: Analyze Memory Metrics**

**Prompt:**
```
Show me CloudWatch metrics for the demo-high-memory function, specifically looking at memory usage and errors in the last 4 hours
```

**Note**: Lambda doesn't natively expose memory usage metrics. Agent may indicate this limitation.

**Alternative Prompt:**
```
How many errors occurred for demo-high-memory in the last hour, and is there a pattern?
```

---

**Step 4: Calculate Memory Requirements**

**Prompt:**
```
If the function is currently allocated 512MB and experiencing memory errors at 85% usage, how much memory should I allocate to provide a 30% buffer?
```

**Expected Agent Response:**
- Current usage: 512MB × 0.85 = 435MB
- With 30% buffer: 435MB ÷ 0.7 = 621MB
- Recommendation: Increase to at least 768MB or 1024MB (next Lambda tier)

---

### Resolution Steps

```bash
# Increase Lambda memory allocation
aws lambda update-function-configuration \
  --function-name demo-high-memory \
  --memory-size 1024 \
  --region us-east-1
```

**Verification Prompt:**
```
Check the demo-high-memory function configuration and confirm the memory has been increased to 1024MB
```

---

## Scenario 4: API Gateway Errors

### Incident Description
**Alert**: High rate of 4xx and 5xx errors from API endpoints

**Symptoms**:
- 401 Unauthorized errors
- 500 Internal Server Errors
- Intermittent 503 Service Unavailable

### Agent Investigation Steps

**Step 1: Identify Error Types**

**Prompt:**
```
Query CloudWatch logs for log group /aws/lambda/demo-api-errors for ERROR patterns showing HTTP status codes in the last hour
```

**Expected Agent Response:**
```
[ERROR] Bad Request - Invalid JSON payload (400)
[ERROR] Unauthorized - Invalid API key (401)
[ERROR] Forbidden - Insufficient permissions (403)
[ERROR] Internal Server Error - Unexpected exception (500)
[ERROR] Service Unavailable - System overloaded (503)
```

---

**Step 2: Count Error Types**

**Prompt:**
```
Based on the logs, can you count how many of each error type (400, 401, 403, 500, 503) occurred in the last hour?
```

**Expected Agent Response:**
- Breakdown of error counts by type
- Percentage of each error type

---

**Step 3: Check for Patterns**

**Prompt:**
```
Are the errors distributed randomly or clustered at specific times? Show me when the 500 errors occurred.
```

**Expected Agent Response:**
- Timeline of errors
- Identification of patterns (e.g., all 500 errors between 2:00-2:15 PM)

---

**Step 4: Investigate 500 Errors**

**Prompt:**
```
For the Internal Server Errors (500), query the logs for Exception or stack trace information that might indicate root cause
```

**Expected Agent Response:**
```
[ERROR] Internal Server Error - Unexpected exception
Exception: Unexpected internal error occurred
```

---

### Resolution Steps

Based on error types:

1. **400 Bad Request**: Improve client-side validation, add API schema validation
2. **401/403 Authentication**: Check API keys, IAM permissions, Cognito configuration
3. **500 Internal Server**: Fix application bugs, add error handling, deploy fix
4. **503 Service Unavailable**: Scale resources, add load balancer, implement queue

---

## Scenario 5: Multi-Service Health Check

### Incident Description
**Alert**: General system degradation - multiple services reporting issues

**Symptoms**:
- Slow response times across all endpoints
- Intermittent failures
- User complaints about application being "down"

### Agent Investigation Steps

**Step 1: Comprehensive Health Check**

**Prompt:**
```
I need a full system health check. Check the status of:
1. All Lambda functions
2. All EC2 instances
3. All RDS databases

Show me everything that's running and any issues you find.
```

**Expected Agent Response:**
- Complete inventory of resources
- Status of each service
- Any unhealthy or stopped instances

---

**Step 2: Check Recent Changes**

**Prompt:**
```
Based on the Lambda functions you found, which ones were modified most recently? A recent deployment might have caused this.
```

**Expected Agent Response:**
- List of functions sorted by last modified time
- Recently changed functions highlighted

---

**Step 3: Correlate Errors Across Services**

**Prompt:**
```
Query CloudWatch logs for ALL Lambda function log groups for ERROR patterns in the last 30 minutes. Are multiple services experiencing errors?
```

**Note**: Agent may need to query each log group separately or ask which ones to check.

---

**Step 4: Metrics Overview**

**Prompt:**
```
Show me CloudWatch metrics for the AWS/Lambda namespace in the last hour. I want to see overall invocation count and error count across all functions.
```

**Expected Agent Response:**
- Aggregate metrics
- Comparison to normal baseline

---

**Step 5: Root Cause Hypothesis**

**Prompt:**
```
Based on all the health checks and error patterns, what do you think is the most likely root cause of this system-wide issue?
```

**Expected Agent Response:**
- Agent synthesizes all data
- Provides hypothesis (e.g., "RDS database is down affecting all Lambda functions that depend on it")
- Recommends next steps

---

### Resolution Steps

Common multi-service issues:

1. **Database Outage**: All services using DB will fail → Restart RDS, check backups
2. **Network Issue**: VPC/subnet problem → Check route tables, NAT gateway, security groups
3. **AWS Service Outage**: Regional issue → Check AWS Status Dashboard
4. **Bad Deployment**: Recent code change → Rollback to previous version
5. **Resource Exhaustion**: Out of capacity → Scale up, add auto-scaling

---

## Scenario 6: Cost Analysis

### Incident Description
**Alert**: AWS bill shows unexpected Lambda costs

**Symptoms**:
- Lambda costs 3x higher than usual
- Need to identify expensive functions

### Agent Investigation Steps

**Step 1: Identify High-Invocation Functions**

**Prompt:**
```
Show me CloudWatch metrics for all Lambda functions focusing on invocation count in the last 24 hours
```

**Expected Agent Response:**
- Invocation counts per function
- Functions with unusually high invocations

---

**Step 2: Calculate Cost**

**Prompt:**
```
If a Lambda function was invoked 1 million times in the last 24 hours, with an average duration of 500ms and 512MB memory, what would the approximate cost be?
```

**Expected Agent Response:**
- Compute GB-seconds: 1M × 0.5s × 0.5GB = 250,000 GB-seconds
- Cost calculation based on Lambda pricing
- Estimated daily cost

---

**Step 3: Identify Optimization Opportunities**

**Prompt:**
```
Looking at the Lambda functions, which ones have very low average duration but high invocations? Those might be good candidates for memory optimization.
```

**Expected Agent Response:**
- Functions with <100ms duration
- Recommendation to reduce memory (saves cost)

---

## Agent Testing Checklist

Before demos or client presentations, verify agent capabilities:

### Basic Functionality
- [ ] Agent loads at https://d3lro400idfnsp.cloudfront.net
- [ ] Login works with demo@example.com credentials
- [ ] Suggested prompts are visible
- [ ] Agent responds to "What tools do you have?"

### CloudWatch Logs Tool
- [ ] Can query logs with filter patterns
- [ ] Returns log events with timestamps
- [ ] Handles "log group not found" errors gracefully
- [ ] Can query multiple time ranges (1 hour, 4 hours, 24 hours)

### CloudWatch Metrics Tool
- [ ] Can retrieve Lambda metrics
- [ ] Returns time-series data with timestamps
- [ ] Handles different namespaces (AWS/Lambda, AWS/EC2, etc.)
- [ ] Can query different statistics (Average, Sum, Maximum)

### AWS Service Health Tool
- [ ] Can check Lambda function status
- [ ] Can check EC2 instance status
- [ ] Can check RDS database status
- [ ] Returns comprehensive health information

### Calculator Tool
- [ ] Can perform basic math
- [ ] Can calculate percentages
- [ ] Can do cost estimates
- [ ] Provides explanations with results

### Conversational Ability
- [ ] Remembers context from previous messages
- [ ] Asks clarifying questions when needed
- [ ] Provides actionable recommendations
- [ ] Synthesizes data from multiple tools

---

## Troubleshooting Guide

### Issue: Agent says "I don't have permission to access that log group"

**Solution:**
Check IAM role permissions. The agent needs:
```json
{
  "Action": ["logs:FilterLogEvents", "logs:GetLogEvents"],
  "Resource": "arn:aws:logs:us-east-1:123456789012:log-group:*"
}
```

---

### Issue: No log data returned when querying

**Possible Causes:**
1. Log group doesn't exist (check spelling)
2. No logs in the specified time range
3. Filter pattern doesn't match any logs

**Verification:**
```bash
# Check if log group exists
aws logs describe-log-groups \
  --log-group-name-prefix /aws/lambda/ \
  --region us-east-1

# Manually query logs
aws logs filter-log-events \
  --log-group-name /aws/lambda/demo-error-simulator \
  --start-time $(date -d '1 hour ago' +%s)000 \
  --region us-east-1
```

---

### Issue: Metrics show no data

**Possible Causes:**
1. Lambda hasn't been invoked recently
2. Wrong metric name or namespace
3. Time range too far in the past

**Solution:**
Invoke Lambda to generate fresh metrics:
```bash
aws lambda invoke --function-name demo-error-simulator --region us-east-1 /dev/null
```

Wait 2-3 minutes, then query metrics again.

---

### Issue: Agent response is slow

**Expected Behavior:**
- Simple queries: 3-5 seconds
- Complex queries: 5-10 seconds
- Multi-tool queries: 10-15 seconds

If slower than this:
1. Check AWS region latency
2. Check CloudWatch Logs volume (millions of log events = slower)
3. Reduce time range or add more specific filter patterns

---

### Issue: Test Lambda functions not generating errors

**Solution:**
Check ERROR_RATE environment variable:
```bash
aws lambda get-function-configuration \
  --function-name demo-error-simulator \
  --query 'Environment.Variables.ERROR_RATE' \
  --region us-east-1
```

Update if needed:
```bash
aws lambda update-function-configuration \
  --function-name demo-error-simulator \
  --environment Variables={ERROR_RATE=50} \
  --region us-east-1
```

---

## Clean Up Test Infrastructure

After demos, remove test resources to avoid costs:

```bash
# Delete CloudFormation stack (removes all Lambda functions)
aws cloudformation delete-stack \
  --stack-name devops-agent-demo-lambdas \
  --region us-east-1

# Wait for deletion
aws cloudformation wait stack-delete-complete \
  --stack-name devops-agent-demo-lambdas \
  --region us-east-1

# Delete CloudWatch Log Groups (optional - they persist after Lambda deletion)
aws logs delete-log-group --log-group-name /aws/lambda/demo-error-simulator --region us-east-1
aws logs delete-log-group --log-group-name /aws/lambda/demo-slow-response --region us-east-1
aws logs delete-log-group --log-group-name /aws/lambda/demo-api-errors --region us-east-1
aws logs delete-log-group --log-group-name /aws/lambda/demo-high-memory --region us-east-1

# Verify cleanup
aws lambda list-functions --query 'Functions[?starts_with(FunctionName, `demo-`)].FunctionName' --region us-east-1
# Should return empty array: []
```

---

## Additional Resources

### Demo Videos
- Record your screen during successful demos for backup
- Create short clips (30-60 seconds) of each scenario for social media

### Custom Scenarios
- Work with clients to create scenarios specific to their infrastructure
- Import their actual CloudWatch logs (sanitized) for realistic demos

### Agent Enhancements
- Add more tools based on client needs (Datadog, PagerDuty, Kubernetes)
- Implement custom workflows (auto-remediation, ticket creation)
- Integrate with Slack for notifications

---

**Questions or Issues?**

Contact: your-email@example.com

**Happy Demonstrating! 🚀**
