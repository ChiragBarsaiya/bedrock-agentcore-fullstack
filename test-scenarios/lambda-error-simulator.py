"""
Lambda Error Simulator - For DevOps Agent Demo
This Lambda function generates various types of errors and logs for demonstration purposes.

Deploy this to create realistic incident scenarios for your DevOps Agent demos.
"""

import json
import random
import time
from datetime import datetime
import os

def lambda_handler(event, context):
    """
    Main handler that randomly generates different error scenarios.

    Environment Variables:
    - ERROR_RATE: Percentage (0-100) of requests that should fail (default: 30)
    - SCENARIO: Force specific scenario (database|timeout|memory|api|success)
    """

    # Get configuration from environment
    error_rate = int(os.environ.get('ERROR_RATE', '30'))
    forced_scenario = os.environ.get('SCENARIO', None)

    # Random scenario selection if not forced
    if forced_scenario:
        scenario = forced_scenario
    elif random.randint(1, 100) <= error_rate:
        scenario = random.choice(['database', 'timeout', 'memory', 'api', 'exception'])
    else:
        scenario = 'success'

    # Log the incoming request
    print(f"[INFO] Processing request at {datetime.utcnow().isoformat()}")
    print(f"[INFO] Scenario selected: {scenario}")
    print(f"[INFO] Event: {json.dumps(event)}")

    # Execute scenario
    try:
        if scenario == 'database':
            return simulate_database_error()
        elif scenario == 'timeout':
            return simulate_timeout()
        elif scenario == 'memory':
            return simulate_memory_error()
        elif scenario == 'api':
            return simulate_api_error()
        elif scenario == 'exception':
            return simulate_unhandled_exception()
        else:
            return simulate_success()
    except Exception as e:
        print(f"[ERROR] Unhandled exception: {str(e)}")
        print(f"[ERROR] Exception type: {type(e).__name__}")
        raise

def simulate_database_error():
    """Simulate a database connection error"""
    print("[ERROR] Database connection failed")
    print("[ERROR] Could not connect to RDS instance: demo-db-instance.us-east-1.rds.amazonaws.com")
    print("[ERROR] Connection timeout after 30 seconds")
    print("[ERROR] Error code: 2003 - Can't connect to MySQL server")

    return {
        'statusCode': 500,
        'body': json.dumps({
            'error': 'DatabaseConnectionError',
            'message': 'Failed to connect to database',
            'timestamp': datetime.utcnow().isoformat()
        })
    }

def simulate_timeout():
    """Simulate a slow operation that times out"""
    print("[WARN] Starting slow external API call")
    print("[WARN] Calling external service: https://api.external-service.com/v1/data")

    # Simulate slow operation (but not actually timeout in Lambda to keep demo fast)
    time.sleep(2)

    print("[ERROR] External API call timed out after 30 seconds")
    print("[ERROR] Request ID: req_abc123xyz")
    print("[ERROR] Circuit breaker OPEN - failing fast for next 60 seconds")

    return {
        'statusCode': 504,
        'body': json.dumps({
            'error': 'GatewayTimeout',
            'message': 'External service timed out',
            'timestamp': datetime.utcnow().isoformat()
        })
    }

def simulate_memory_error():
    """Simulate a memory allocation error"""
    print("[WARN] Loading large dataset into memory")
    print("[WARN] Current memory usage: 512 MB / 1024 MB allocated")
    print("[ERROR] MemoryError: Cannot allocate 2GB array")
    print("[ERROR] Consider increasing Lambda memory or using streaming processing")

    return {
        'statusCode': 500,
        'body': json.dumps({
            'error': 'MemoryError',
            'message': 'Insufficient memory for operation',
            'timestamp': datetime.utcnow().isoformat()
        })
    }

def simulate_api_error():
    """Simulate an API validation error"""
    print("[WARN] Validating request payload")
    print("[ERROR] Validation failed: Missing required field 'user_id'")
    print("[ERROR] Invalid data type for field 'amount': expected float, got string")
    print("[ERROR] Request rejected")

    return {
        'statusCode': 400,
        'body': json.dumps({
            'error': 'ValidationError',
            'message': 'Invalid request payload',
            'details': {
                'missing_fields': ['user_id'],
                'type_errors': {'amount': 'expected float, got string'}
            },
            'timestamp': datetime.utcnow().isoformat()
        })
    }

def simulate_unhandled_exception():
    """Simulate an unhandled exception"""
    print("[INFO] Processing user request")
    print("[INFO] Fetching user data for user_id: 12345")

    # This will actually raise an exception
    raise ValueError("User not found: user_id 12345 does not exist in database")

def simulate_success():
    """Simulate a successful request"""
    print("[INFO] Request processed successfully")
    print(f"[INFO] Response time: {random.randint(50, 150)}ms")
    print("[INFO] Data returned: 1024 bytes")

    return {
        'statusCode': 200,
        'body': json.dumps({
            'status': 'success',
            'data': {
                'processed': True,
                'records': random.randint(10, 100),
                'timestamp': datetime.utcnow().isoformat()
            }
        })
    }

# For local testing
if __name__ == "__main__":
    test_event = {
        'httpMethod': 'GET',
        'path': '/test',
        'headers': {'User-Agent': 'Test'}
    }

    print("=== Testing Lambda Error Simulator ===")
    for i in range(5):
        print(f"\n--- Test {i+1} ---")
        result = lambda_handler(test_event, None)
        print(f"Result: {result}")
