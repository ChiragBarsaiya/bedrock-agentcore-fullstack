# DevOps Incident Response Agent - Complete Code
# Copy this to: sample-amazon-bedrock-agentcore-fullstack-webapp/agent/strands_agent.py

from strands import Agent, tool
from strands_tools import calculator
import json
import boto3
from datetime import datetime, timedelta
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands.models import BedrockModel

# Create the AgentCore app
app = BedrockAgentCoreApp()

# Initialize AWS clients
logs_client = boto3.client('logs')
cloudwatch_client = boto3.client('cloudwatch')
ec2_client = boto3.client('ec2')
rds_client = boto3.client('rds')
lambda_client = boto3.client('lambda')

# DevOps Tool 1: CloudWatch Logs Query
@tool
def query_cloudwatch_logs(log_group_name: str, filter_pattern: str = "", hours_back: int = 1, limit: int = 50):
    """Query CloudWatch Logs for error patterns and anomalies."""
    try:
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours_back)
        start_timestamp = int(start_time.timestamp() * 1000)
        end_timestamp = int(end_time.timestamp() * 1000)

        response = logs_client.filter_log_events(
            logGroupName=log_group_name,
            startTime=start_timestamp,
            endTime=end_timestamp,
            filterPattern=filter_pattern,
            limit=limit
        )

        events = response.get('events', [])
        if not events:
            return f"No log events found in '{log_group_name}' for the last {hours_back} hour(s)"

        result = f"Found {len(events)} log events:\\n\\n"
        for event in events[:20]:
            timestamp = datetime.fromtimestamp(event['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            message = event.get('message', '').strip()
            result += f"[{timestamp}] {message}\\n"

        if len(events) > 20:
            result += f"\\n... and {len(events) - 20} more events"
        return result
    except Exception as e:
        return f"Error querying CloudWatch Logs: {str(e)}"

# DevOps Tool 2: CloudWatch Metrics
@tool
def get_cloudwatch_metrics(namespace: str, metric_name: str, dimensions: str = "", hours_back: int = 4, statistic: str = "Average"):
    """Retrieve CloudWatch metrics for system monitoring."""
    try:
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours_back)

        # Parse dimensions
        dim_list = []
        if dimensions:
            for dim in dimensions.split(','):
                if '=' in dim:
                    key, value = dim.split('=', 1)
                    dim_list.append({'Name': key.strip(), 'Value': value.strip()})

        response = cloudwatch_client.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dim_list,
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=[statistic]
        )

        datapoints = response.get('Datapoints', [])
        if not datapoints:
            return f"No metric data found for {metric_name} in {namespace}"

        datapoints = sorted(datapoints, key=lambda x: x['Timestamp'])

        result = f"{metric_name} ({statistic}) - Last {hours_back} hour(s):\\n\\n"
        for dp in datapoints[-10:]:
            timestamp = dp['Timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            value = dp.get(statistic, 0)
            unit = dp.get('Unit', '')
            result += f"[{timestamp}] {value:.2f} {unit}\\n"

        # Summary
        values = [dp.get(statistic, 0) for dp in datapoints]
        avg_value = sum(values) / len(values) if values else 0
        max_value = max(values) if values else 0
        min_value = min(values) if values else 0
        result += f"\\nSummary: Avg={avg_value:.2f}, Max={max_value:.2f}, Min={min_value:.2f}"

        return result
    except Exception as e:
        return f"Error retrieving metrics: {str(e)}"

# DevOps Tool 3: AWS Service Health Check
@tool
def check_aws_service_health(service_type: str, resource_ids: str = ""):
    """Check health status of AWS services (EC2, RDS, Lambda)."""
    try:
        resource_list = [r.strip() for r in resource_ids.split(',') if r.strip()] if resource_ids else []

        if service_type.lower() == 'ec2':
            if resource_list:
                response = ec2_client.describe_instance_status(InstanceIds=resource_list)
            else:
                response = ec2_client.describe_instance_status()

            statuses = response.get('InstanceStatuses', [])
            if not statuses:
                return "No EC2 instances found or all instances are stopped"

            result = "EC2 Instance Health Status:\\n\\n"
            for status in statuses:
                result += f"Instance: {status['InstanceId']}\\n"
                result += f"  State: {status['InstanceState']['Name']}\\n"
                result += f"  System Status: {status['SystemStatus']['Status']}\\n"
                result += f"  Instance Status: {status['InstanceStatus']['Status']}\\n\\n"
            return result

        elif service_type.lower() == 'rds':
            response = rds_client.describe_db_instances()
            db_instances = response.get('DBInstances', [])

            if resource_list:
                db_instances = [db for db in db_instances if db['DBInstanceIdentifier'] in resource_list]

            if not db_instances:
                return "No RDS databases found"

            result = "RDS Database Health Status:\\n\\n"
            for db in db_instances:
                result += f"Database: {db['DBInstanceIdentifier']}\\n"
                result += f"  Status: {db['DBInstanceStatus']}\\n"
                result += f"  Engine: {db['Engine']} {db.get('EngineVersion', 'N/A')}\\n\\n"
            return result

        elif service_type.lower() == 'lambda':
            response = lambda_client.list_functions()
            functions = response.get('Functions', [])

            if resource_list:
                functions = [f for f in functions if f['FunctionName'] in resource_list]

            if not functions:
                return "No Lambda functions found"

            result = "Lambda Function Status:\\n\\n"
            for func in functions[:20]:
                result += f"Function: {func['FunctionName']}\\n"
                result += f"  Runtime: {func['Runtime']}\\n"
                result += f"  Last Modified: {func['LastModified']}\\n"
                result += f"  Memory: {func['MemorySize']} MB\\n\\n"

            if len(functions) > 20:
                result += f"... and {len(functions) - 20} more functions"
            return result

        else:
            return f"Unsupported service type: {service_type}. Supported: ec2, rds, lambda"

    except Exception as e:
        return f"Error checking service health: {str(e)}"

# Configure the Agent
model_id = "global.anthropic.claude-haiku-4-5-20251001-v1:0"
model = BedrockModel(model_id=model_id)

agent = Agent(
    model=model,
    tools=[calculator, query_cloudwatch_logs, get_cloudwatch_metrics, check_aws_service_health],
    system_prompt="""You are a DevOps Incident Response Agent designed to help engineering teams diagnose and resolve production incidents quickly.

Your primary mission is to assist DevOps engineers and SREs during critical incidents by:
1. Analyzing CloudWatch logs to identify error patterns and root causes
2. Monitoring system metrics to detect anomalies and performance issues
3. Checking the health status of AWS infrastructure (EC2, RDS, Lambda)
4. Performing calculations to analyze trends and capacity
5. Providing clear, actionable recommendations for incident resolution

When responding to incidents:
- Start with a quick summary of the current situation
- Identify the most likely root cause based on data
- Provide specific, actionable remediation steps
- Use data-driven insights from logs and metrics
- Explain technical findings in clear, concise language
- Escalate to human engineers when you encounter limitations

Best practices:
- Always verify information from multiple data sources when possible
- Look for correlations between metrics, logs, and service health
- Consider both immediate fixes and long-term preventive measures
- Prioritize customer impact and system stability
- Document findings for post-incident reviews

Remember: Speed and accuracy are critical during incidents. Focus on actionable insights that help resolve issues quickly while maintaining system reliability.

Powered by mydevopsproject.io - Accelerating Agentic Workflows for Enterprise.""",
    callback_handler=None
)

@app.entrypoint
async def agent_invocation(payload):
    """Invoke the agent with a payload"""
    if isinstance(payload, str):
        payload = json.loads(payload)

    user_input = None
    if isinstance(payload, dict):
        if "input" in payload and isinstance(payload["input"], dict):
            user_input = payload["input"].get("prompt")
        else:
            user_input = payload.get("prompt")

    if not user_input:
        raise ValueError(f"No prompt found in payload. Expected {{'prompt': '...'}} or {{'input': {{'prompt': '...'}}}}. Received: {payload}")

    stream = agent.stream_async(user_input)
    async for event in stream:
        if (event.get('event',{}).get('contentBlockDelta',{}).get('delta',{}).get('text')):
            print(event.get('event',{}).get('contentBlockDelta',{}).get('delta',{}).get('text'))
            yield (event.get('event',{}).get('contentBlockDelta',{}).get('delta',{}).get('text'))

if __name__ == "__main__":
    app.run()
