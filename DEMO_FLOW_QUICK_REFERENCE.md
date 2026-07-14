# DevOps Agent Demo - Quick Reference Card
## Copy-Paste Prompts for Live Demonstrations

---

## 🔗 Demo URL
**URL**: https://d3lro400idfnsp.cloudfront.net
**Login**: demo@example.com
**Password**: YourDemoPassword123!

---

## 📋 Demo Flow (15-minute version)

### 1️⃣ Lambda Health Check (2 min)
**Click suggested prompt or type:**
```
Check the health status of all Lambda functions
```

**What to say while agent works:**
- "The agent is autonomously calling the AWS Lambda API"
- "It's checking function status, configuration, and last update time"
- "This would take 5+ minutes manually through AWS Console"

**Expected result:** List of Lambda functions with status, runtime, memory, last modified

---

### 2️⃣ CloudWatch Logs Query (3 min)
**Type this prompt:**
```
Query CloudWatch logs for errors in the last hour
```

**Agent will ask for log group name. Respond with:**
```
Check log group /aws/lambda/strands-agent for any ERROR or Exception patterns in the last 2 hours
```

**What to say while agent works:**
- "Agent is filtering CloudWatch logs with error patterns"
- "Manual process: Navigate CloudWatch > Log Groups > Filter > Parse results = 10 minutes"
- "Agent does this in seconds"

**Expected result:** Filtered log events with timestamps, log streams, and error messages

---

### 3️⃣ CloudWatch Metrics Analysis (2 min)
**Click suggested prompt or type:**
```
Show me CloudWatch metrics for AWS/Lambda namespace
```

**What to say while agent works:**
- "Pulling Lambda performance metrics from the last 4 hours"
- "Looking at invocations, errors, duration, throttles"
- "Agent can spot performance degradation patterns"

**Expected result:** Time-series metrics data with timestamps and values

**Optional follow-up:**
```
Calculate the error rate percentage for the last 4 hours
```

---

### 4️⃣ EC2 Health Check (2 min)
**Type this prompt:**
```
Check the status of all EC2 instances and see if any are unhealthy
```

**What to say while agent works:**
- "Agent can check multiple AWS services: EC2, RDS, Lambda"
- "Provides holistic infrastructure health view"
- "Helps identify downstream dependencies causing issues"

**Expected result:** List of EC2 instances with state, type, availability zone, status checks

---

### 5️⃣ Advanced Multi-Tool Query (3 min - optional)
**Type this complex prompt:**
```
I'm seeing high latency on my API. Can you check Lambda function health, query recent error logs, and show me performance metrics for the last hour?
```

**What to say while agent works:**
- "This is where it gets powerful - the agent chains multiple tools together"
- "It will: check Lambda status, query logs for errors, fetch performance metrics"
- "One natural language request triggers multiple AWS API calls automatically"

**Expected result:** Comprehensive report using all three tools

---

### 6️⃣ Calculator Tool (Bonus - 1 min)
**Type this prompt:**
```
If my Lambda runs 10,000 times per day and has a 2.5% error rate, how many errors am I seeing per day?
```

**What to say:**
- "Agent also has a calculator tool for on-the-fly analysis"
- "Useful for capacity planning, error rate calculations, cost estimates"

**Expected result:** 250 errors per day (with explanation)

---

## 🎯 Demo Scenarios by Audience Type

### For Technical Audiences (DevOps/SRE Teams)
**Focus on:** Tool capabilities, API integrations, IAM permissions, customization potential

**Recommended prompts:**
```
1. Check the health status of all Lambda functions
2. Query CloudWatch logs for errors in log group /aws/lambda/strands-agent in the last 2 hours
3. Show me CloudWatch metrics for AWS/Lambda namespace
4. Check the status of all EC2 instances
```

**Technical talking points:**
- "Built on Amazon Bedrock AgentCore with Claude Haiku 4.5"
- "Agent has read-only IAM permissions via least-privilege policy"
- "Uses boto3 SDK for AWS API calls"
- "All code runs in your VPC, no data leaves your account"

---

### For Executive/Business Audiences
**Focus on:** ROI, time savings, cost reduction, business impact

**Recommended prompts:**
```
1. Check the health status of all Lambda functions
2. Show me CloudWatch metrics for AWS/Lambda namespace
3. Calculate 4 hours of downtime at $8,000 per hour
```

**Business talking points:**
- "Reduces Mean Time To Resolution (MTTR) by 50-70%"
- "Average incident investigation: 30 minutes manual → 3 minutes with agent"
- "Annual savings: $37,500 based on 100 incidents/year"
- "ROI achieved in 60-90 days"

---

### For Security/Compliance Teams
**Focus on:** Security controls, audit logging, data privacy

**Recommended prompts:**
```
1. Check the health status of all Lambda functions (show read-only nature)
2. Query CloudWatch logs (show IAM-controlled access)
```

**Security talking points:**
- "All infrastructure deployed via CloudFormation (auditable IaC)"
- "JWT authentication via AWS Cognito"
- "IAM policies with least-privilege (read-only for monitoring)"
- "All API calls logged to CloudWatch for compliance audit"
- "No data sent to external services - runs entirely in your AWS account"

---

## 🚨 Incident Response Scenario (Advanced Demo)

### Scenario: "You just got paged - API is returning 500 errors"

**Prompt sequence:**
```
1. Check the health status of all Lambda functions
   → Identify which functions might be failing

2. Query CloudWatch logs for log group /aws/lambda/[problematic-function] in the last hour for ERROR patterns
   → Find error messages and stack traces

3. Show me CloudWatch metrics for AWS/Lambda namespace focusing on errors and invocations
   → Identify when the issue started

4. Check the status of EC2 instances
   → Rule out infrastructure issues

5. Based on the errors you found, what do you recommend for next steps?
   → Agent provides diagnosis and recommendations
```

**Timeline:**
- Manual investigation: 20-30 minutes
- With agent: 3-5 minutes
- **Savings: 85% faster time to insight**

---

## 💡 Recovery Prompts (If Demo Issues Occur)

### If agent gives unexpected response:
```
Let me rephrase: [reword the prompt more specifically]
```

### If agent says it can't access a resource:
```
What permissions would you need to complete that task?
```
*Then explain: "This shows the security guardrails - agent can't access resources without explicit IAM permissions"*

### If you need to show a different capability:
```
What tools and capabilities do you have available?
```
*Agent will list all its tools*

---

## 📊 ROI Calculator (Use During Demo)

### Quick Math to Show Value:

**Scenario: Mid-size company with 100 incidents/year**

| Metric | Before Agent | With Agent | Improvement |
|--------|--------------|------------|-------------|
| Time to First Insight | 20 min | 3 min | 85% faster |
| MTTR | 4 hours | 1.5 hours | 62% faster |
| Cost per incident | $2,400 | $900 | $1,500 saved |
| **Annual savings** | — | — | **$150,000** |

**Prompt to demonstrate:**
```
Calculate the annual savings if we reduce MTTR from 4 hours to 1.5 hours for 100 incidents per year, assuming engineer cost is $150/hour and downtime cost is $8,000/hour
```

---

## 🎤 Opening Lines (Choose Based on Audience)

### For Technical Teams:
*"I'm going to show you an AI agent that can autonomously query CloudWatch logs, pull metrics, and check AWS service health - all through natural language. It's like having a senior SRE on-call 24/7."*

### For Business Teams:
*"Companies spend an average of 4-6 hours resolving incidents. I'm going to show you how to cut that in half using AI-powered agents that investigate issues automatically."*

### For Mixed Audiences:
*"Imagine getting paged at 2 AM. Instead of spending 30 minutes just figuring out what's wrong, an AI agent has already investigated logs, checked metrics, and identified the root cause. Let me show you how this works."*

---

## 🎬 Closing Lines (Always Close with Next Steps)

### After Demo:
*"So in 5 minutes, we investigated Lambda health, queried logs, analyzed metrics, and checked infrastructure - tasks that would take 20-30 minutes manually. The question is: what specific tools would accelerate YOUR incident response?"*

### Call to Action:
*"I recommend we schedule a 90-minute technical workshop with your DevOps team to map out your incident response workflow and design custom tools for your environment. Does [DATE/TIME] work for your calendar?"*

---

## 📞 Contact Information to Provide

**mydevopsproject.io Contact:**
- Email: your-email@example.com
- Website: github.com/chiragbarsaiya
- Demo Environment (30-day access): https://d3lro400idfnsp.cloudfront.net

**Leave-Behind Resources:**
- Architecture diagram (email after demo)
- ROI calculator spreadsheet
- Sample custom tools we've built for other clients
- Implementation timeline and pricing sheet

---

## ⚡ Quick Tips

### Do's:
✅ Let the agent fully respond before moving to next prompt
✅ Explain what's happening while agent "thinks"
✅ Connect capabilities to client's specific pain points
✅ Ask questions: "What are your biggest incident response challenges?"
✅ Demonstrate value: "This just saved you 15 minutes"

### Don'ts:
❌ Don't rush through responses
❌ Don't apologize for 5-10 second response times (this is normal)
❌ Don't over-promise features you haven't built
❌ Don't forget to close with next steps
❌ Don't use jargon without explaining it

---

## 🔧 Pre-Demo Checklist

**15 minutes before demo:**
- [ ] Test login at https://d3lro400idfnsp.cloudfront.net
- [ ] Verify all suggested prompts are visible
- [ ] Check that agent responds to basic query: "What tools do you have?"
- [ ] Have AWS Console open in another tab (for technical audiences)
- [ ] Review client's tech stack notes
- [ ] Have this reference card open
- [ ] Start screen share software
- [ ] Silence phone/notifications

**5 minutes before demo:**
- [ ] Close unnecessary browser tabs
- [ ] Set browser zoom to 125% for better visibility
- [ ] Have a glass of water ready
- [ ] Take a deep breath 😊

---

**You've got this! 🚀**

**Remember**: You're not just demonstrating technology - you're showing how to save time, reduce stress, and improve reliability for DevOps teams.
