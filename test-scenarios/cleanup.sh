#!/bin/bash

# DevOps Agent Demo - Test Infrastructure Cleanup Script
# This script removes all demo Lambda functions and related resources

set -e  # Exit on error

echo "=========================================="
echo "DevOps Agent Demo - Cleanup"
echo "=========================================="
echo ""

# Configuration
STACK_NAME="devops-agent-demo-lambdas"
REGION="us-east-1"

echo "⚠️  WARNING: This will delete the following resources:"
echo "  - CloudFormation Stack: $STACK_NAME"
echo "  - 4 Lambda Functions (demo-*)"
echo "  - 3 EventBridge Rules"
echo "  - 2 CloudWatch Alarms"
echo "  - IAM Role and Policies"
echo ""
read -p "Are you sure you want to proceed? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo ""
echo "Checking if stack exists..."
if ! aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION &> /dev/null; then
    echo "❌ Stack '$STACK_NAME' not found. Nothing to clean up."
    exit 0
fi

echo "✅ Stack found. Proceeding with deletion..."
echo ""

# Delete CloudFormation stack
echo "Deleting CloudFormation stack..."
aws cloudformation delete-stack \
    --stack-name $STACK_NAME \
    --region $REGION

echo "⏳ Waiting for stack deletion to complete (this takes 1-2 minutes)..."
aws cloudformation wait stack-delete-complete \
    --stack-name $STACK_NAME \
    --region $REGION

echo "✅ CloudFormation stack deleted successfully!"
echo ""

# Optional: Delete CloudWatch Log Groups
echo "Do you want to delete CloudWatch Log Groups? (They are retained by default for audit purposes)"
echo "  - /aws/lambda/demo-error-simulator"
echo "  - /aws/lambda/demo-slow-response"
echo "  - /aws/lambda/demo-api-errors"
echo "  - /aws/lambda/demo-high-memory"
echo ""
read -p "Delete log groups? (yes/no): " delete_logs

if [ "$delete_logs" = "yes" ]; then
    echo ""
    echo "Deleting CloudWatch Log Groups..."

    LOG_GROUPS=(
        "/aws/lambda/demo-error-simulator"
        "/aws/lambda/demo-slow-response"
        "/aws/lambda/demo-api-errors"
        "/aws/lambda/demo-high-memory"
    )

    for log_group in "${LOG_GROUPS[@]}"; do
        if aws logs describe-log-groups --log-group-name-prefix "$log_group" --region $REGION | grep -q "$log_group"; then
            echo "  Deleting $log_group..."
            aws logs delete-log-group \
                --log-group-name "$log_group" \
                --region $REGION
            echo "    ✅ Deleted"
        else
            echo "    ℹ️  $log_group not found (may have been already deleted)"
        fi
    done
else
    echo "ℹ️  CloudWatch Log Groups retained. You can delete them manually later if needed."
fi

echo ""
echo "=========================================="
echo "✅ Cleanup Complete!"
echo "=========================================="
echo ""

# Verify cleanup
echo "Verifying cleanup..."
REMAINING_FUNCTIONS=$(aws lambda list-functions \
    --query 'Functions[?starts_with(FunctionName, `demo-`)].FunctionName' \
    --output text \
    --region $REGION)

if [ -z "$REMAINING_FUNCTIONS" ]; then
    echo "✅ All demo Lambda functions have been removed"
else
    echo "⚠️  Warning: Some functions may still exist:"
    echo "$REMAINING_FUNCTIONS"
fi

echo ""
echo "📊 Current AWS Lambda Functions:"
aws lambda list-functions \
    --query 'Functions[*].FunctionName' \
    --output table \
    --region $REGION

echo ""
echo "💰 Cost Impact: Demo resources have been removed. You should see reduced costs on your next AWS bill."
echo ""
echo "🔄 To redeploy test infrastructure: ./deploy.sh"
echo ""
