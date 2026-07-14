# DevOps Incident Response Agent — AWS Bedrock AgentCore

An AI-powered DevOps assistant that diagnoses and responds to production incidents in real time. Built on **Amazon Bedrock AgentCore** using the **Strands Agents SDK**, with a full-stack React frontend, Cognito authentication, and fully automated CDK infrastructure.

This is a hands-on exploration of **agentic AI on AWS** — from building custom tools that call live AWS APIs, to deploying a production-ready multi-stack CDK application from a single command.

---

## What It Does

The agent acts as a first-responder during incidents. Ask it questions in natural language and it will:

- **Query CloudWatch Logs** — surface error patterns, exceptions, and anomalies from any log group
- **Pull CloudWatch Metrics** — retrieve CPU, latency, error rate, and other metrics with statistical summaries
- **Check infrastructure health** — inspect EC2 instance state, RDS database status, and Lambda function configuration
- **Check the AWS Service Health Dashboard** — proactively rule out AWS-side outages before investigating your application
- **Synthesize findings** — correlate data across sources and recommend specific remediation steps

**Example prompts:**
```
What errors appeared in /aws/lambda/my-api in the last hour?
Show me CPU utilization for my EC2 instances over the last 4 hours
Is there any active AWS outage in us-east-1 that might explain this latency spike?
Analyze the error rate trend for my RDS instance
```

---

## Architecture

```
Browser (React + Cloudscape)
    │
    │  JWT Bearer Token (Cognito)
    ▼
Amazon Bedrock AgentCore Runtime
    │  (ARM64 container, isolated microVM)
    ▼
Strands Agent (Claude Haiku 4.5 via Bedrock)
    ├── query_cloudwatch_logs()
    ├── get_cloudwatch_metrics()
    ├── check_aws_service_health()
    └── check_aws_service_health_dashboard()
```

![Architecture Diagram](./sample-amazon-bedrock-agentcore-fullstack-webapp/img/architecture_diagram.svg)

### Infrastructure (AWS CDK — 4 stacks)

| Stack | Purpose | Key Resources |
|---|---|---|
| **AgentCoreInfra** | Build pipeline | ECR, CodeBuild (ARM64), IAM, S3 |
| **AgentCoreAuth** | User management | Cognito User Pool + Client |
| **AgentCoreRuntime** | Agent runtime | AgentCore Runtime, Lambda waiter |
| **AgentCoreFrontend** | Web UI | S3, CloudFront (OAC), React app |

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI Agent | [Strands Agents SDK](https://github.com/awslabs/strands) |
| LLM | Anthropic Claude Haiku 4.5 (via Amazon Bedrock) |
| Agent Runtime | Amazon Bedrock AgentCore |
| Infrastructure | AWS CDK (TypeScript) |
| Frontend | React + TypeScript + [Cloudscape Design System](https://cloudscape.design/) |
| Auth | Amazon Cognito (JWT, email verification) |
| CDN | CloudFront + S3 (Origin Access Control) |
| Container | ARM64 Docker (built via CodeBuild — no local Docker needed) |
| Monitoring | CloudWatch Logs, Metrics, X-Ray tracing |

---

## Project Structure

```
├── sample-amazon-bedrock-agentcore-fullstack-webapp/
│   ├── agent/
│   │   ├── strands_agent.py        # Agent implementation + custom DevOps tools
│   │   ├── requirements.txt        # Python dependencies
│   │   └── Dockerfile              # ARM64 container (built by CodeBuild)
│   │
│   ├── cdk/
│   │   ├── bin/app.ts              # CDK app entry point
│   │   └── lib/
│   │       ├── infra-stack.ts      # ECR, CodeBuild, IAM
│   │       ├── auth-stack.ts       # Cognito User Pool
│   │       ├── runtime-stack.ts    # AgentCore Runtime + Lambda waiter
│   │       └── frontend-stack.ts  # CloudFront + S3
│   │
│   ├── frontend/src/
│   │   ├── App.tsx                 # Chat UI (Cloudscape GenAI components)
│   │   ├── AuthModal.tsx           # Sign in / sign up flow
│   │   ├── auth.ts                 # Cognito token management
│   │   └── agentcore.ts           # Direct AgentCore invocation with JWT
│   │
│   ├── scripts/
│   │   ├── build-frontend.sh       # Injects ARN + Cognito config at build time
│   │   └── build-frontend.ps1      # Windows equivalent
│   │
│   ├── deploy-all.sh               # One-command full deployment (macOS/Linux)
│   └── deploy-all.ps1              # One-command full deployment (Windows)
│
├── test-scenarios/                 # CloudFormation stacks for demo Lambda errors
│   ├── deploy-test-lambdas.yaml    # Deploys error/slow/high-memory Lambda functions
│   ├── lambda-error-simulator.py   # Generates realistic incident log data
│   ├── deploy.sh                   # Deploy test scenario
│   └── cleanup.sh                  # Cleanup test resources
│
├── devops_agent_code_reference.py  # Standalone agent code reference
├── devops-permissions-policy.json  # Minimal IAM policy for the agent
└── update_frontend_prompts.py      # Script to update UI sample prompts
```

---

## Key Engineering Decisions

### Why AgentCore over self-hosted?
AgentCore provides built-in JWT authentication, isolated microVM execution per request, X-Ray tracing, and CloudWatch observability out of the box — all without managing servers or containers at runtime.

### Why a Lambda waiter Custom Resource?
CDK deploys synchronously via CloudFormation. CodeBuild's container build takes 5–10 minutes and its API response exceeds CloudFormation's 4 KB Custom Resource limit. A Lambda waiter polls CodeBuild internally and returns only a pass/fail signal to CloudFormation, keeping the deployment synchronous without blocking infrastructure creation.

### Why CodeBuild for container builds?
AgentCore requires ARM64 images. CodeBuild runs natively on ARM64, avoiding emulation overhead. This also means no local Docker Desktop is required — the build runs entirely in AWS.

### Why four CDK stacks?
Each stack has a different change frequency. Splitting them means an agent code update only redeploys `AgentCoreRuntime` (~10 min), not the entire infrastructure. Frontend CSS changes redeploy only `AgentCoreFrontend` (~2 min).

### Direct frontend-to-AgentCore invocation
The React frontend calls AgentCore directly using HTTPS + JWT Bearer token (Cognito access token). This avoids adding a backend API layer for a demo, leveraging AgentCore's built-in Cognito JWT authorizer.

---

## Deploy It Yourself

### Prerequisites

- **AWS CLI v2.31.13+** (AgentCore support added January 2025)
- **Node.js 22+**
- **AWS credentials** configured with permissions for: CloudFormation, Bedrock, Lambda, S3, ECR, CodeBuild, Cognito, IAM, CloudFront
- Verify AgentCore is available in your region: [AgentCore Regions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html)

### One-Command Deploy

```bash
# macOS / Linux
cd sample-amazon-bedrock-agentcore-fullstack-webapp
chmod +x deploy-all.sh scripts/build-frontend.sh
./deploy-all.sh
```

```powershell
# Windows
cd sample-amazon-bedrock-agentcore-fullstack-webapp
.\deploy-all.ps1
```

**~10 minutes.** Most of that is CodeBuild building the ARM64 container image. The CloudFront URL is printed at the end.

### Local Development (no deployment needed)

```bash
# macOS / Linux
cd sample-amazon-bedrock-agentcore-fullstack-webapp
chmod +x dev-local.sh
./dev-local.sh
```

```powershell
# Windows
cd sample-amazon-bedrock-agentcore-fullstack-webapp
.\dev-local.ps1
```

Starts the agent on `http://localhost:8080` and the Vite dev server on `http://localhost:5173`. No authentication required locally. Agent changes restart in ~10 seconds vs ~10 minutes for a full redeploy.

### Test Scenarios (realistic incident simulation)

```bash
cd test-scenarios
./deploy.sh        # Deploys 4 Lambda functions that simulate errors, timeouts, and high memory
./cleanup.sh       # Removes all test resources
```

Once deployed, ask the agent to investigate the `demo-error-simulator`, `demo-slow-response`, `demo-api-errors`, or `demo-high-memory` Lambda functions.

### Cleanup

```bash
cd sample-amazon-bedrock-agentcore-fullstack-webapp/cdk
npx cdk destroy AgentCoreFrontend --no-cli-pager
npx cdk destroy AgentCoreRuntime --no-cli-pager
npx cdk destroy AgentCoreAuth --no-cli-pager
npx cdk destroy AgentCoreInfra --no-cli-pager
```

---

## Extending the Agent

### Add a new tool

```python
# In agent/strands_agent.py
@tool
def restart_ecs_service(cluster_name: str, service_name: str):
    """Restart an ECS service by forcing a new deployment."""
    ecs = boto3.client('ecs')
    ecs.update_service(
        cluster=cluster_name,
        service=service_name,
        forceNewDeployment=True
    )
    return f"Triggered new deployment for {service_name} in {cluster_name}"
```

Then add it to the `tools=[...]` list in the `Agent(...)` constructor. Redeploy the runtime:

```bash
cd sample-amazon-bedrock-agentcore-fullstack-webapp/cdk
npx cdk deploy AgentCoreRuntime --no-cli-pager
```

### Change the LLM

Edit `model_id` in `agent/strands_agent.py`:

```python
model_id = "us.anthropic.claude-opus-4-8-20251101-v1:0"  # Upgrade to Opus
```

### Update the system prompt

The agent's behaviour is controlled by the `system_prompt` argument in `Agent(...)`. Edit it to adjust tone, scope, or domain focus.

---

## Cost Estimate

Light usage (100–500 requests/month), us-east-1:

| Service | Estimated Cost |
|---|---|
| AgentCore Runtime | ~$0.50–2/month |
| Bedrock (Claude Haiku 4.5) | ~$0.50–3/month |
| CloudFront + S3 | Free tier covers light usage |
| Cognito | Free up to 10,000 MAUs |
| ECR | ~$0.10/month |
| CloudWatch Logs | ~$0.50–1/month |
| **Total** | **~$3–10/month** |

---

## Resources

- [Amazon Bedrock AgentCore Docs](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-agentcore.html)
- [Strands Agents SDK](https://github.com/awslabs/strands)
- [AgentCore JWT Authentication](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-oauth.html#invoke-agent)
- [Cloudscape Design System](https://cloudscape.design/)
- [CDK API Reference](https://docs.aws.amazon.com/cdk/api/v2/)

---

## License

MIT-0 — see [LICENSE](./sample-amazon-bedrock-agentcore-fullstack-webapp/LICENSE)
