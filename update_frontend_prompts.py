#!/usr/bin/env python3
import re

# Read the file
with open('sample-amazon-bedrock-agentcore-fullstack-webapp/frontend/src/App.tsx', 'r') as f:
    content = f.read()

# Old prompts to replace
old_prompts = """      return [
        { id: 'calc', text: 'What is 123 + 456?' },
        { id: 'weather', text: "What's the weather like today?" },
        { id: 'table', text: 'Create a comparison table of 3 AWS services' },
        { id: 'math', text: 'Calculate 2048 * 1024 and explain the result' }
      ];"""

# New DevOps prompts
new_prompts = """      return [
        { id: 'lambda', text: 'Check the health status of all Lambda functions' },
        { id: 'logs', text: 'Query CloudWatch logs for errors in the last hour' },
        { id: 'metrics', text: 'Show me CloudWatch metrics for AWS/Lambda namespace' },
        { id: 'ec2', text: 'Check the status of EC2 instances' }
      ];"""

# Replace
content = content.replace(old_prompts, new_prompts)

# Write back
with open('sample-amazon-bedrock-agentcore-fullstack-webapp/frontend/src/App.tsx', 'w') as f:
    f.write(content)

print("Frontend prompts updated successfully!")
