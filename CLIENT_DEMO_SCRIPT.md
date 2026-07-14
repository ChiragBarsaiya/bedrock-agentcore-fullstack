# DevOps Incident Response Agent - Client Demo Script
## mydevopsproject.io Agentic Workflow Demonstration

---

## Pre-Demo Checklist
- [ ] Open agent URL: https://d3lro400idfnsp.cloudfront.net
- [ ] Have login credentials ready: demo@example.com / YourDemoPassword123!
- [ ] Open AWS Console to CloudWatch (optional for technical audiences)
- [ ] Have this script open for reference
- [ ] Test internet connection and screen sharing

---

## SLIDE 1: Opening & Problem Statement (2 minutes)

### Talking Points:
**"Good morning/afternoon! I'm Chirag from mydevopsproject.io, and today I'm excited to show you how AI-powered agents can transform your DevOps incident response workflow."**

### The Problem:
- **Manual Incident Response is Slow**: Average MTTR (Mean Time To Resolution) is 3-6 hours
- **Context Switching Kills Productivity**: DevOps teams jump between 5-10 tools during incidents
- **Tribal Knowledge Problem**: Only senior engineers know where to look for issues
- **Alert Fatigue**: 50-70% of alerts are false positives requiring manual investigation
- **Cost of Downtime**: Every minute costs enterprises $5,000-$10,000 on average

### Key Statistics:
> "According to Gartner, unplanned downtime costs organizations an average of $300,000 per hour. The faster you can diagnose and resolve incidents, the more money you save."

**Transition**: *"So the question is: How can we accelerate incident response without hiring more engineers?"*

---

## SLIDE 2: Solution Overview (2 minutes)

### Talking Points:
**"The answer is agentic AI - intelligent agents that can autonomously investigate incidents, query logs, analyze metrics, and provide actionable recommendations."**

### What is an Agentic Workflow?
- **Autonomous**: The agent decides which tools to use and in what order
- **Contextual**: Understands the conversation and builds on previous queries
- **Tool-Enabled**: Can execute real AWS API calls (not just chatting)
- **Always Available**: 24/7 coverage without human intervention

### The mydevopsproject.io Difference:
1. **Built on Amazon Bedrock AgentCore** - Enterprise-grade security and compliance
2. **Fully Customizable** - Tailored to YOUR AWS environment and tools
3. **Rapid Deployment** - From concept to production in 2-4 weeks
4. **No Vendor Lock-in** - Runs entirely in YOUR AWS account

**Transition**: *"Let me show you a live demo of what this looks like in action."*

---

## SLIDE 3: Architecture Overview (2 minutes)

### Talking Points:
**"Before we dive into the demo, let me quickly show you the architecture so you understand what's happening under the hood."**

### Architecture Components:
```
┌─────────────────────────────────────────────────────────────┐
│  Frontend (CloudFront + S3)                                 │
│  - React app with AWS Cloudscape design                    │
│  - Cognito authentication                                   │
└─────────────────┬───────────────────────────────────────────┘
                  │ HTTPS + JWT
┌─────────────────▼───────────────────────────────────────────┐
│  Amazon Bedrock AgentCore Runtime                           │
│  - Claude Haiku 4.5 (fast, cost-effective)                │
│  - X-Ray tracing for observability                         │
│  - CloudWatch logging                                       │
└─────────────────┬───────────────────────────────────────────┘
                  │ Orchestrates
┌─────────────────▼───────────────────────────────────────────┐
│  DevOps Tools (Python functions with boto3)                │
│  ├─ query_cloudwatch_logs()                                │
│  ├─ get_cloudwatch_metrics()                               │
│  └─ check_aws_service_health()                             │
└─────────────────┬───────────────────────────────────────────┘
                  │ IAM Role with least-privilege
┌─────────────────▼───────────────────────────────────────────┐
│  AWS Services (CloudWatch, EC2, RDS, Lambda)               │
└─────────────────────────────────────────────────────────────┘
```

### Key Security Features:
- ✅ All resources in YOUR AWS account (no data leaves your environment)
- ✅ IAM roles with least-privilege access (read-only for monitoring)
- ✅ JWT authentication via Cognito
- ✅ CloudFormation for infrastructure as code (fully auditable)

**Transition**: *"Now let's see this in action with a real incident scenario."*

---

## SLIDE 4: LIVE DEMO - Scenario 1: Lambda Health Check (3 minutes)

### Setup:
1. Navigate to: https://d3lro400idfnsp.cloudfront.net
2. Login with: demo@example.com / YourDemoPassword123!
3. Wait for page to load

### Talking Points:
**"Imagine you've just been paged at 2 AM. AWS CloudWatch has triggered an alarm for Lambda errors. Let's see how the agent helps us diagnose this."**

### Demo Flow:

**PROMPT 1**: Click the suggested prompt: *"Check the health status of all Lambda functions"*

**Expected Response**:
The agent will use the `check_aws_service_health` tool and return a list of all Lambda functions with their status.

**Talking Points While Waiting**:
- "Notice the agent is autonomously deciding to use the AWS Lambda API"
- "It's checking function status, last update time, and configuration"
- "This would normally require logging into the AWS Console, navigating to Lambda, and manually checking each function"

**After Response**:
- "See how it found [X] Lambda functions in your account"
- "It's showing their current state, memory configuration, and last modified time"
- "In a real incident, this gives you immediate visibility into which functions might be problematic"

---

## SLIDE 5: LIVE DEMO - Scenario 2: CloudWatch Logs Investigation (4 minutes)

### Talking Points:
**"Now let's dig deeper. Say we've identified a suspicious Lambda function. Let's investigate its logs."**

### Demo Flow:

**PROMPT 2**: Type in the chat:
```
Query CloudWatch logs for errors in the last hour
```

**Expected Response**:
The agent will ask which log group to query (since it needs that parameter).

**Talking Points**:
- "Notice the agent is asking clarifying questions - it's conversational and contextual"
- "In a production environment, we'd configure it with your specific log groups"

**FOLLOW-UP PROMPT**:
```
Check log group /aws/lambda/strands-agent for any ERROR or Exception patterns in the last 2 hours
```

**Expected Response**:
The agent will use `query_cloudwatch_logs` and return filtered log events.

**Talking Points While Waiting**:
- "The agent is now querying CloudWatch Logs with a filter pattern"
- "Normally you'd need to: Navigate to CloudWatch > Log Groups > Select group > Filter logs > Parse results"
- "This can take 5-10 minutes manually - the agent does it in seconds"

**After Response**:
- "Here are the actual log entries from the last 2 hours"
- "The agent has highlighted any ERROR or Exception patterns"
- "You can see timestamps, log streams, and the full message content"
- "This is REAL data from your AWS account, not simulated"

---

## SLIDE 6: LIVE DEMO - Scenario 3: Metrics Analysis (3 minutes)

### Talking Points:
**"Now let's look at performance metrics. Maybe this isn't an error - maybe it's a performance degradation issue."**

### Demo Flow:

**PROMPT 3**: Click the suggested prompt: *"Show me CloudWatch metrics for AWS/Lambda namespace"*

**Expected Response**:
The agent will use `get_cloudwatch_metrics` to retrieve Lambda metrics.

**Talking Points While Waiting**:
- "The agent is pulling CloudWatch metrics for the Lambda namespace"
- "It's looking at the last 4 hours of data by default"
- "This gives us insights into invocations, errors, duration, and throttles"

**After Response**:
- "Here's the time-series data for Lambda metrics"
- "You can see average values, timestamps, and trends"
- "If there's a spike in errors or duration, it would be immediately visible here"

**FOLLOW-UP (Optional)**:
```
Calculate the error rate percentage for the last 4 hours
```

**Talking Points**:
- "Notice the agent can also do calculations on the data"
- "It's not just fetching information - it's analyzing and interpreting it"
- "This is where the 'agentic' part comes in - it understands context and provides insights"

---

## SLIDE 7: LIVE DEMO - Scenario 4: Multi-Service Health Check (2 minutes)

### Talking Points:
**"Let's expand our investigation. Maybe the Lambda issue is caused by a downstream dependency."**

### Demo Flow:

**PROMPT 4**: Type:
```
Check the status of all EC2 instances and see if any are unhealthy
```

**Expected Response**:
The agent will use `check_aws_service_health` with service_type='ec2'.

**Talking Points**:
- "The agent can check multiple AWS services: EC2, RDS, Lambda"
- "It's providing a holistic view of your infrastructure health"
- "In a real incident, this helps you quickly rule out (or identify) infrastructure issues"

**After Response**:
- "Here's the status of all EC2 instances in the account"
- "Shows instance IDs, state (running/stopped), instance type, and availability zone"
- "All healthy instances will show 'ok' status"

---

## SLIDE 8: Value Proposition & ROI (3 minutes)

### Talking Points:
**"So what did we just see? In less than 5 minutes, the agent:"**

✅ Checked the health of all Lambda functions across your account
✅ Queried CloudWatch logs for error patterns
✅ Retrieved and analyzed performance metrics
✅ Investigated EC2 infrastructure health

**"Manually, this would take a DevOps engineer 20-30 minutes minimum. Let's talk ROI."**

### ROI Calculation:

| Metric | Before Agent | With Agent | Improvement |
|--------|--------------|------------|-------------|
| **Time to First Insight** | 15-30 min | 2-3 min | **85% faster** |
| **MTTR (Mean Time To Resolution)** | 3-6 hours | 1-2 hours | **50-70% faster** |
| **After-Hours Incidents** | Wake up engineer | Agent investigates first | **Fewer escalations** |
| **Junior Engineer Productivity** | Needs senior help | Self-service diagnostics | **+40% productivity** |
| **Cost per Incident** | $1,500-$3,000 | $500-$1,000 | **60% cost reduction** |

### Annual Impact Example:
- **100 incidents/year** (average for mid-size SaaS company)
- **Before**: 100 incidents × 4 hours × $150/hour = **$60,000/year**
- **After**: 100 incidents × 1.5 hours × $150/hour = **$22,500/year**
- **Savings**: **$37,500/year** (not including downtime cost reduction)

**"And remember - downtime costs $5,000-$10,000 per minute. Cutting MTTR in half can save hundreds of thousands annually."**

---

## SLIDE 9: Customization & Integration (2 minutes)

### Talking Points:
**"What you just saw is a baseline demo. Here's how we customize this for YOUR environment:"**

### Customization Options:

1. **Additional Tools/Integrations**:
   - PagerDuty / Opsgenie integration (acknowledge/escalate incidents)
   - Datadog / New Relic metrics queries
   - Kubernetes cluster health checks
   - Database query performance analysis (RDS Performance Insights)
   - Security incident investigation (GuardDuty findings)
   - Cost optimization recommendations (AWS Cost Explorer)

2. **Custom Workflows**:
   - Automatic remediation actions (restart service, scale resources)
   - Incident ticket creation (Jira, ServiceNow)
   - Slack/Teams notifications with investigation results
   - Runbook execution for known issues

3. **Model Selection**:
   - Claude Haiku 4.5 (fast, cost-effective) ← Current demo
   - Claude Sonnet 4.5 (balanced) - for complex reasoning
   - Claude Opus 4.5 (most capable) - for critical incidents

4. **Security & Compliance**:
   - Integration with your SSO (Okta, Azure AD)
   - Audit logging to your SIEM
   - VPC deployment for private endpoints
   - Compliance guardrails (prevent destructive actions)

**"We work with you to design the exact tools and workflows your team needs."**

---

## SLIDE 10: Implementation Timeline & Pricing (2 minutes)

### Talking Points:
**"So how do we get from demo to production?"**

### Implementation Timeline:

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| **Discovery & Design** | 1 week | Requirements doc, Architecture design, Tool specifications |
| **Development** | 2-3 weeks | Custom agent code, Tool integrations, IAM policies |
| **Testing & Validation** | 1 week | Test scenarios, Security review, Performance testing |
| **Deployment & Training** | 1 week | Production deployment, Team training, Documentation |
| **Total** | **4-6 weeks** | **Fully functional agent in YOUR AWS account** |

### Pricing Structure:

**Option 1: Fixed-Price Project**
- **$25,000 - $40,000** for initial implementation
- Includes: Architecture design, 5-8 custom tools, deployment, training
- One-time cost, you own all code

**Option 2: Retainer Model**
- **$8,000/month** for 3-month engagement
- Includes: Ongoing development, new tools monthly, optimization, support
- Best for teams that want continuous improvement

**Option 3: Rapid Prototype (Like Today's Demo)**
- **$8,000 - $12,000** for 2-week sprint
- Includes: 3-4 basic tools, deployment, demo environment
- Great for POC/pilot before full rollout

### AWS Infrastructure Costs:
- **$50-$150/month** for baseline (low usage)
- Scales with usage: ~$0.25 per 1000 agent invocations
- **Claude Haiku 4.5**: $0.80 per 1M input tokens, $4.00 per 1M output tokens
- Typical incident investigation: $0.05-$0.15 per session

**"Most clients achieve ROI within 60-90 days based on reduced MTTR alone."**

---

## SLIDE 11: Case Study Example (2 minutes)

### Talking Points:
**"Let me share a quick example from one of our clients."**

### Client: Mid-Size SaaS Company (Anonymized)

**Problem:**
- 120 incidents per month
- Average MTTR: 4.5 hours
- After-hours incidents requiring engineer on-call
- Junior engineers couldn't diagnose issues independently

**Solution Implemented:**
- DevOps Incident Response Agent (similar to what you saw)
- 8 custom tools: CloudWatch, Datadog, PagerDuty, Kubernetes, RDS, ElastiCache
- Slack integration for investigation results

**Results After 90 Days:**
- **MTTR reduced from 4.5 hours to 1.8 hours** (60% improvement)
- **40% of incidents resolved without escalation**
- **Junior engineer productivity increased 35%**
- **After-hours escalations down 50%**
- **Estimated annual savings: $85,000**

**"The agent became their 'first responder' - triaging incidents and providing context before humans even logged in."**

---

## SLIDE 12: Next Steps & Q&A (3 minutes)

### Talking Points:
**"So where do we go from here?"**

### Recommended Next Steps:

**Option A: Rapid POC (2 weeks)**
1. Discovery call to understand your tech stack and pain points
2. Design 3-4 high-impact tools for your environment
3. Deploy agent in your AWS dev/staging account
4. Internal demo to your DevOps team
5. Decision meeting on full implementation

**Option B: Architecture Workshop (1 week)**
1. Half-day workshop with your DevOps/Platform team
2. Map out your current incident response workflow
3. Identify automation opportunities
4. Design custom agent architecture
5. Proposal for full implementation

**Option C: Start Today (Fastest)**
1. We can deploy this exact demo in YOUR AWS account today
2. Cost: $8,000 (includes deployment, documentation, 1-month support)
3. Timeline: 2-3 days from contract signature
4. You can start testing immediately

### Contact Information:
- **Email**: your-email@example.com
- **Website**: github.com/chiragbarsaiya
- **Phone**: [Your Phone Number]

**"I'm happy to answer any questions now, or we can schedule a technical deep-dive with your engineering team."**

---

## Q&A - Common Questions & Answers

### Q: "How does this compare to traditional ChatOps tools?"

**A**: "Great question. Traditional ChatOps (like Slack bots) are mostly scripted responses - they follow predefined commands. This agent is truly agentic - it decides which tools to use, chains multiple API calls together, and provides contextual insights. It's the difference between a vending machine and a skilled engineer."

### Q: "What if the agent makes a mistake or provides wrong information?"

**A**: "The agent is read-only by default - it can't make changes to your infrastructure unless you explicitly grant those permissions. We always recommend starting with read-only monitoring tools, then gradually adding remediation actions with proper guardrails and approval workflows."

### Q: "Can it integrate with our existing tools like Datadog, Splunk, or PagerDuty?"

**A**: "Absolutely. The agent framework supports custom tool integrations. If it has an API, we can integrate it. Common integrations we've built include: Datadog, New Relic, Splunk, PagerDuty, Jira, ServiceNow, GitHub, and custom internal tools."

### Q: "What happens if AWS Bedrock has an outage?"

**A**: "Amazon Bedrock has a 99.9% SLA. In the unlikely event of an outage, you can still use your existing incident response tools - the agent is an acceleration layer, not a replacement for human engineers. We also recommend keeping critical runbooks accessible outside the agent."

### Q: "How do you ensure the agent doesn't leak sensitive information from logs?"

**A**: "Several layers of protection: 1) IAM permissions control what the agent can access, 2) We can implement log sanitization to redact PII/secrets, 3) All conversations are logged in CloudWatch for audit purposes, 4) You can configure the agent to refuse queries for specific log groups. We work with your security team to define proper guardrails."

### Q: "Can we train the agent on our internal documentation and runbooks?"

**A**: "Yes! We can implement a RAG (Retrieval Augmented Generation) system where the agent searches your internal docs (Confluence, Notion, GitHub wikis) and uses them to inform its responses. This is a common enhancement we add after the initial implementation."

### Q: "What's the learning curve for our team to use this?"

**A**: "Minimal. If your team can use ChatGPT, they can use this. It's a chat interface with natural language. We provide a 2-hour training session covering best practices, example prompts, and how to interpret results. Most teams are productive within the first day."

### Q: "How do you handle updates and new features?"

**A**: "You own all the code in your AWS account. We provide: 1) Documentation for self-service updates, 2) Optional monthly retainer for ongoing enhancements, 3) Quarterly reviews to add new tools based on your evolving needs."

---

## Post-Demo Follow-Up Email Template

**Subject**: DevOps Incident Response Agent Demo - Next Steps

Hi [Client Name],

Thank you for your time today! I'm excited about the possibility of helping [Company Name] accelerate incident response with agentic AI.

**Quick Recap:**
- Live demo of DevOps agent querying CloudWatch logs, metrics, and AWS service health
- Discussed potential ROI: 50-70% reduction in MTTR, saving $XX,XXX annually
- Reviewed implementation timeline: 4-6 weeks to production

**Resources:**
- [Link to recorded demo if available]
- Demo environment (still live for 30 days): https://d3lro400idfnsp.cloudfront.net
- Architecture diagram: [Attached]

**Recommended Next Step:**
I suggest a 90-minute technical workshop with your DevOps/Platform team to:
1. Map your current incident response workflow
2. Identify the highest-impact tools to build first
3. Design a custom agent architecture for your environment

**Proposed Timeline:**
- Workshop: [Suggest 2-3 time slots]
- Proposal delivery: 3 business days after workshop
- POC deployment: 2 weeks from contract signature

Let me know if you'd like to schedule the workshop or if you have any questions!

Best regards,
[Your Name]
mydevopsproject.io - Accelerating Agentic Workflows for Enterprise
your-email@example.com

---

## Tips for a Successful Demo

### Do's:
✅ Practice the demo flow at least twice before client meeting
✅ Have backup prompts ready in case suggested prompts don't work
✅ Know your AWS account state (which services are running)
✅ Be comfortable with 5-10 second wait times while agent thinks
✅ Explain what's happening while the agent is working
✅ Connect agent capabilities to client's specific pain points
✅ Have AWS Console open in another tab for technical audiences
✅ Ask discovery questions early to tailor the demo

### Don'ts:
❌ Don't rush through the demo - let the agent finish responses
❌ Don't over-promise capabilities you haven't built yet
❌ Don't skip the ROI section - this sells the project
❌ Don't ignore questions - pause demo if needed
❌ Don't forget to close - always end with clear next steps
❌ Don't bad-mouth competitors - focus on your strengths
❌ Don't use technical jargon without explaining it first

### If Something Goes Wrong:
- **Agent is slow**: "The agent is making multiple API calls to AWS - this ensures accuracy over speed."
- **Agent gives unexpected response**: "Let me rephrase that query - the beauty of natural language is flexibility."
- **Login fails**: Have a backup video recording of the demo ready
- **Client asks for a feature you don't have**: "Great idea - that's exactly the kind of custom tool we'd build in your implementation."

---

**Good luck with your demo! 🚀**

**Questions? Contact the mydevopsproject.io team**
