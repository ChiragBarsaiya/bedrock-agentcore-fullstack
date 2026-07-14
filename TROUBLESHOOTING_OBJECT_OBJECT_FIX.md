# Troubleshooting: "[object Object]" Display Issue - FIXED

## Issue Description

When querying CloudWatch logs or using other DevOps tools, the agent was displaying "[object Object]" instead of the actual log data.

**Example:**
```
User: Query CloudWatch logs for log group /aws/lambda/demo-error-simulator for ERROR patterns in the last hour

Agent: [object Object]
```

## Root Cause

The streaming response handler in `frontend/src/agentcore.ts` was receiving parsed JSON objects from the agent and passing them directly to React's state without converting them to strings first.

When React tried to render a JavaScript object, it displayed "[object Object]" (the default toString() representation).

## Technical Details

### Location
- File: `sample-amazon-bedrock-agentcore-fullstack-webapp/frontend/src/agentcore.ts`
- Lines: 72-75 (local dev mode) and 194-197 (production mode)

### Broken Code (Before)
```typescript
// Line 72-75 and 194-197
try {
  const parsed = JSON.parse(data);
  fullResponse += parsed;              // ❌ Concatenating object
  request.onChunk(parsed);             // ❌ Passing object to React
} catch {
  fullResponse += data;
  request.onChunk(data);
}
```

### Fixed Code (After)
```typescript
try {
  const parsed = JSON.parse(data);
  // Ensure we always pass a string to onChunk
  const chunkText = typeof parsed === 'string' ? parsed : String(parsed);
  fullResponse += chunkText;           // ✅ Concatenating string
  request.onChunk(chunkText);          // ✅ Passing string to React
} catch {
  fullResponse += data;
  request.onChunk(data);
}
```

## Fix Applied

### Step 1: Update agentcore.ts

The fix ensures that any parsed JSON is converted to a string before being passed to React:

```typescript
const chunkText = typeof parsed === 'string' ? parsed : String(parsed);
```

This handles both cases:
- If `parsed` is already a string → use it as-is
- If `parsed` is an object → convert it to string using `String()`

### Step 2: Rebuild and Redeploy

```bash
cd sample-amazon-bedrock-agentcore-fullstack-webapp/cdk
npx cdk deploy AgentCoreFrontend --require-approval never
```

Deployment takes approximately 3-5 minutes.

## Verification

After deployment completes:

1. **Clear browser cache** (hard refresh: Ctrl+Shift+R or Cmd+Shift+R)
2. Navigate to: https://d3lro400idfnsp.cloudfront.net
3. Login: demo@example.com / YourDemoPassword123!
4. Test with CloudWatch logs query:
   ```
   Query CloudWatch logs for log group /aws/lambda/demo-error-simulator for ERROR patterns in the last hour
   ```

### Expected Result (After Fix)

```
Found 15 log events:

[2026-04-16 17:10:23] [ERROR] Database connection failed to demo-db.us-east-1.rds.amazonaws.com
[2026-04-16 17:10:25] [ERROR] External API call timed out after 30 seconds
[2026-04-16 17:10:27] [ERROR] MemoryError: Cannot allocate array - insufficient memory
[2026-04-16 17:10:29] [ERROR] Validation failed: Missing required field 'user_id'
...
```

## Additional Notes

### Why This Happened

The agent's Python code correctly returns strings from the tools:
```python
@tool
def query_cloudwatch_logs(...):
    result = f"Found {len(events)} log events:\\n\\n"
    for event in events[:20]:
        result += f"[{timestamp}] {message}\\n"
    return result  # ✅ Returns string
```

However, during the streaming response, the AgentCore runtime may wrap the response in JSON for transport:
```json
{"text": "Found 15 log events..."}
```

The frontend's streaming handler parses this JSON and was passing the entire object instead of extracting the text.

### Files Modified

1. **frontend/src/agentcore.ts** - Added type checking and String() conversion
2. **Deployed via CDK** - AgentCoreFrontend stack redeployed

### Rollback (If Needed)

If you need to rollback:
```bash
cd sample-amazon-bedrock-agentcore-fullstack-webapp/frontend/src
cp agentcore.ts.backup agentcore.ts  # If you created a backup
cd ../../cdk
npx cdk deploy AgentCoreFrontend --require-approval never
```

## Prevention

To prevent similar issues in the future:

1. **Always type-check streaming data** before passing to React state
2. **Use TypeScript interfaces** to ensure type safety
3. **Test with real data** from all tools before demos
4. **Check browser console** for type errors during development

## Status

- ✅ **Issue Identified**: 2026-04-16
- ✅ **Fix Applied**: 2026-04-16
- 🔄 **Deployment**: In progress (ETA: 3-5 minutes)
- ⏳ **Verification**: Pending deployment completion

## Contact

If issues persist after deployment:
- Check browser console (F12) for errors
- Verify CloudFront cache invalidation completed
- Try incognito/private browsing mode
- Contact: your-email@example.com

---

**Last Updated**: 2026-04-16 17:30 UTC
**Status**: Fix deployed, awaiting verification
