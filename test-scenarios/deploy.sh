#!/bin/bash

# DevOps Agent Demo - Test Infrastructure Deployment Script
# This script deploys Lambda functions for generating realistic incident scenarios

set -e  # Exit on error

echo "=========================================="
echo "DevOps Agent Demo - Test Infrastructure"
echo "=========================================="
echo ""

# Configuration
STACK_NAME="devops-agent-demo-lambdas"
REGION="us-east-1"
ERROR_RATE=30

echo "Configuration:"
echo "  Stack Name: $STACK_NAME"
echo "  Region: $REGION"
echo "  Error Rate: $ERROR_RATE%"
echo ""

# Check if stack already exists
echo "Checking if stack exists..."
if aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION &> /dev/null; then
    echo "⚠️  Stack '$STACK_NAME' already exists!"
    echo ""
    echo "Options:"
    echo "  1. Update existing stack"
    echo "  2. Delete and recreate"
    echo "  3. Cancel"
    read -p "Choose option (1-3): " option

    case $option in
        1)
            echo ""
            echo "Updating existing stack..."
            aws cloudformation update-stack \
                --stack-name $STACK_NAME \
                --template-body file://deploy-test-lambdas.yaml \
                --capabilities CAPABILITY_IAM \
                --parameters ParameterKey=ErrorRate,ParameterValue=$ERROR_RATE \
                --region $REGION

            echo "⏳ Waiting for stack update to complete..."
            aws cloudformation wait stack-update-complete \
                --stack-name $STACK_NAME \
                --region $REGION

            echo "✅ Stack updated successfully!"
            ;;
        2)
            echo ""
            echo "Deleting existing stack..."
            aws cloudformation delete-stack \
                --stack-name $STACK_NAME \
                --region $REGION

            echo "⏳ Waiting for stack deletion to complete..."
            aws cloudformation wait stack-delete-complete \
                --stack-name $STACK_NAME \
                --region $REGION

            echo "Creating new stack..."
            aws cloudformation create-stack \
                --stack-name $STACK_NAME \
                --template-body file://deploy-test-lambdas.yaml \
                --capabilities CAPABILITY_IAM \
                --parameters ParameterKey=ErrorRate,ParameterValue=$ERROR_RATE \
                --region $REGION

            echo "⏳ Waiting for stack creation to complete..."
            aws cloudformation wait stack-create-complete \
                --stack-name $STACK_NAME \
                --region $REGION

            echo "✅ Stack created successfully!"
            ;;
        3)
            echo "Cancelled."
            exit 0
            ;;
        *)
            echo "Invalid option. Exiting."
            exit 1
            ;;
    esac
else
    echo "Creating new stack..."
    aws cloudformation create-stack \
        --stack-name $STACK_NAME \
        --template-body file://deploy-test-lambdas.yaml \
        --capabilities CAPABILITY_IAM \
        --parameters ParameterKey=ErrorRate,ParameterValue=$ERROR_RATE \
        --region $REGION

    echo "⏳ Waiting for stack creation to complete (this takes 2-3 minutes)..."
    aws cloudformation wait stack-create-complete \
        --stack-name $STACK_NAME \
        --region $REGION

    echo "✅ Stack created successfully!"
fi

echo ""
echo "=========================================="
echo "📊 Stack Outputs"
echo "=========================================="
aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
    --output table \
    --region $REGION

echo ""
echo "=========================================="
echo "🧪 Generating Test Data"
echo "=========================================="
echo "Invoking Lambda functions to create initial log entries..."

# Invoke each function multiple times
FUNCTIONS=("demo-error-simulator" "demo-slow-response" "demo-api-errors" "demo-high-memory")

for func in "${FUNCTIONS[@]}"; do
    echo ""
    echo "Invoking $func (10 times)..."
    for i in {1..10}; do
        aws lambda invoke \
            --function-name $func \
            --region $REGION \
            --log-type None \
            /dev/null &> /dev/null
        echo -n "."
        sleep 1
    done
    echo " ✅ Done"
done

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "📋 Deployed Lambda Functions:"
aws lambda list-functions \
    --query 'Functions[?starts_with(FunctionName, `demo-`)].FunctionName' \
    --output table \
    --region $REGION

echo ""
echo "📝 CloudWatch Log Groups:"
echo "  - /aws/lambda/demo-error-simulator"
echo "  - /aws/lambda/demo-slow-response"
echo "  - /aws/lambda/demo-api-errors"
echo "  - /aws/lambda/demo-high-memory"
echo ""
echo "⏰ EventBridge Schedules (auto-invoke every 5 minutes):"
echo "  - All demo functions will be triggered automatically"
echo ""
echo "🔗 Test with DevOps Agent:"
echo "  URL: https://d3lro400idfnsp.cloudfront.net"
echo "  Login: demo@example.com / YourDemoPassword123!"
echo ""
echo "💡 Sample Prompts to Try:"
echo "  1. Check the health status of all Lambda functions"
echo "  2. Query CloudWatch logs for log group /aws/lambda/demo-error-simulator for ERROR patterns in the last hour"
echo "  3. Show me CloudWatch metrics for AWS/Lambda namespace"
echo ""
echo "⚠️  Note: Wait 2-3 minutes for CloudWatch Logs to be available before querying"
echo ""
echo "📚 See INCIDENT_RESPONSE_PLAYBOOK.md for detailed test scenarios"
echo ""
echo "🗑️  To clean up: ./cleanup.sh"
echo ""
