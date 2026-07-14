// Note: Using direct HTTP calls to AgentCore with JWT bearer tokens
// as shown in AWS AgentCore documentation

const region = (import.meta as any).env.VITE_REGION || 'us-east-1';
const agentRuntimeArn = (import.meta as any).env.VITE_AGENT_RUNTIME_ARN;
const isLocalDev = (import.meta as any).env.VITE_LOCAL_DEV === 'true';
const localAgentUrl = (import.meta as any).env.VITE_AGENT_RUNTIME_URL || '/api';

export interface InvokeAgentRequest {
  prompt: string;
  sessionId: string;
  onChunk?: (chunk: string) => void;
}

export interface InvokeAgentResponse {
  response: string;
}

// Helper function to ensure we always get a string from agent response
const extractStringFromResponse = (data: any): string => {
  if (typeof data === 'string') {
    return data;
  }

  if (data && typeof data === 'object') {
    // Try common response properties, ensuring each is converted to string
    const candidates = [data.response, data.content, data.text, data.message, data.output];
    for (const candidate of candidates) {
      if (candidate !== undefined && candidate !== null) {
        // If candidate is a string, use it; otherwise stringify it
        return typeof candidate === 'string' ? candidate : JSON.stringify(candidate);
      }
    }
    // If no valid property found, stringify the whole object
    return JSON.stringify(data);
  }

  return 'No response from agent';
};

export const invokeAgent = async (request: InvokeAgentRequest): Promise<InvokeAgentResponse> => {
  try {
    // Local development mode - call local AgentCore instance
    if (isLocalDev) {
      console.log('Invoking local AgentCore:', { url: localAgentUrl });
      console.log('Request payload:', { prompt: request.prompt });

      const response = await fetch(`${localAgentUrl}/invocations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: request.prompt
        }),
      });

      console.log('Local AgentCore response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Local AgentCore error response:', errorText);
        throw new Error(`Local AgentCore invocation failed: ${response.status} ${response.statusText} - ${errorText}`);
      }

      // Check if streaming callback is provided
      if (request.onChunk && response.body) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullResponse = '';
        let buffer = '';

        try {
          while (true) {
            const { done, value} = await reader.read();

            if (done) {
              break;
            }

            const chunk = decoder.decode(value, { stream: true });
            buffer += chunk;

            // Process complete SSE messages in the buffer
            const lines = buffer.split('\n');
            // Keep the last incomplete line in the buffer
            buffer = lines.pop() || '';

            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const data = line.slice(6); // Remove 'data: ' prefix

                // Try to parse as JSON string
                try {
                  const parsed = JSON.parse(data);
                  // FIX: Ensure we always pass a string to onChunk
                  const chunkText = typeof parsed === 'string' ? parsed : JSON.stringify(parsed);
                  fullResponse += chunkText;
                  // Call the chunk callback with parsed content as string
                  request.onChunk(chunkText);
                } catch {
                  // If not JSON, use the raw data
                  fullResponse += data;
                  request.onChunk(data);
                }
              }
            }
          }

          console.log('Streaming completed. Full response:', fullResponse);
          return { response: fullResponse };
        } finally {
          reader.releaseLock();
        }
      }

      // Non-streaming mode (backward compatibility)
      let data;
      try {
        data = await response.json();
        console.log('Local AgentCore response data:', data);
      } catch (parseError) {
        console.error('Failed to parse JSON response:', parseError);
        const textResponse = await response.text();
        console.log('Raw response text:', textResponse);
        throw new Error(`Invalid JSON response from local AgentCore: ${textResponse}`);
      }

      // Use helper function to ensure string response
      const responseText = extractStringFromResponse(data);
      console.log('Final response text:', responseText);

      return {
        response: responseText
      };
    }

    // Production mode - call AWS AgentCore
    // Check if runtime ARN is available
    if (!agentRuntimeArn) {
      throw new Error('AgentCore Runtime ARN not configured. Please check deployment.');
    }

    // Get JWT access token from Cognito (required for AgentCore as per AWS documentation)
    const { getAccessToken } = await import('./auth');
    const jwtToken = await getAccessToken();
    if (!jwtToken) {
      throw new Error('Not authenticated - no access token available');
    }

    // URL encode the agent runtime ARN for the API call (as per AWS documentation)
    const encodedAgentRuntimeArn = encodeURIComponent(agentRuntimeArn);

    // Use the correct AgentCore endpoint format from AWS documentation
    const url = `https://bedrock-agentcore.${region}.amazonaws.com/runtimes/${encodedAgentRuntimeArn}/invocations?qualifier=DEFAULT`;

    console.log('Invoking AgentCore directly:', { url, agentRuntimeArn, region });
    console.log('Request payload:', { prompt: request.prompt });

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${jwtToken}`,
        'X-Amzn-Bedrock-AgentCore-Runtime-Session-Id': request.sessionId,
        'X-Amzn-Trace-Id': `trace-${Date.now()}`,
      },
      body: JSON.stringify({
        prompt: request.prompt
      }),
    });

    console.log('AgentCore response status:', response.status);
    console.log('AgentCore response headers:', Object.fromEntries(response.headers.entries()));

    if (!response.ok) {
      const errorText = await response.text();
      console.error('AgentCore error response:', errorText);
      throw new Error(`AgentCore invocation failed: ${response.status} ${response.statusText} - ${errorText}`);
    }

    // Check if streaming callback is provided
    if (request.onChunk && response.body) {
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullResponse = '';
      let buffer = '';

      try {
        while (true) {
          const { done, value } = await reader.read();

          if (done) {
            break;
          }

          const chunk = decoder.decode(value, { stream: true });
          buffer += chunk;

          // Process complete SSE messages in the buffer
          const lines = buffer.split('\n');
          // Keep the last incomplete line in the buffer
          buffer = lines.pop() || '';

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6); // Remove 'data: ' prefix

              // Try to parse as JSON string
              try {
                const parsed = JSON.parse(data);
                // FIX: Ensure we always pass a string to onChunk
                const chunkText = typeof parsed === 'string' ? parsed : JSON.stringify(parsed);
                fullResponse += chunkText;
                // Call the chunk callback with parsed content as string
                request.onChunk(chunkText);
              } catch {
                // If not JSON, use the raw data
                fullResponse += data;
                request.onChunk(data);
              }
            }
          }
        }

        console.log('Streaming completed. Full response:', fullResponse);
        return { response: fullResponse };
      } finally {
        reader.releaseLock();
      }
    }

    // Non-streaming mode (backward compatibility)
    let data;
    try {
      data = await response.json();
      console.log('AgentCore response data:', data);
    } catch (parseError) {
      console.error('Failed to parse JSON response:', parseError);
      const textResponse = await response.text();
      console.log('Raw response text:', textResponse);
      throw new Error(`Invalid JSON response from AgentCore: ${textResponse}`);
    }

    // Use helper function to ensure string response
    const responseText = extractStringFromResponse(data);
    console.log('Final response text:', responseText);

    return {
      response: responseText
    };

  } catch (error: any) {
    console.error('AgentCore invocation error:', error);
    throw new Error(`Failed to invoke agent: ${error.message}`);
  }
};
