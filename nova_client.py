"""
Agentic Nova Client - AI Planning Layer for Your Automation
"""
import boto3
import json
import re

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

class NovaAgent:
    """
    Agentic AI wrapper around your automation
    Adds: Planning, Reasoning, Adaptation, Reflection
    """
    
    def __init__(self):
        self.model_id = "amazon.nova-lite-v1:0"
        self.conversation_history = []
    
    def plan_workflow(self, task):
        """
        AGENTIC PLANNING: Nova reasons about the task and creates a plan
        
        This is what makes it "agentic" - the AI decides what to do,
        not just following hardcoded rules
        
        Args:
            task: Natural language instruction
            
        Returns:
            Plan with reasoning
        """
        
        prompt = f"""You are an intelligent web automation agent. Analyze this task carefully.

Task: {task}

Think step-by-step:
1. What is the user trying to accomplish?
2. What search query should be used?
3. How many results should be opened?
4. What's the best approach?

Return ONLY a JSON plan like this:

{{
  "reasoning": "Your thought process - why this approach is best",
  "action": "search",
  "query": "the optimized search query",
  "count": number_of_results,
  "expected_outcome": "what the user will get"
}}

Think carefully about the best search query and reasonable number of results."""

        try:
            body = json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ],
                "inferenceConfig": {
                    "maxTokens": 400,
                    "temperature": 0.3  # Lower for consistent planning
                }
            })
            
            response = bedrock.invoke_model(
                modelId=self.model_id,
                body=body,
                contentType="application/json",
                accept="application/json"
            )
            
            result = json.loads(response["body"].read())
            text = result["output"]["message"]["content"][0]["text"]
            
            # Extract JSON
            json_match = re.search(r"\{.*\}", text, re.DOTALL)
            
            if json_match:
                plan = json.loads(json_match.group())
                
                # Store in history
                self.conversation_history.append({
                    "task": task,
                    "plan": plan
                })
                
                return plan
            else:
                # Fallback to simple parsing
                return self._fallback_plan(task)
                
        except Exception as e:
            print(f"Nova planning error: {e}")
            return self._fallback_plan(task)
    
    def _fallback_plan(self, task):
        """Simple fallback if Nova fails"""
        task_lower = task.lower()
        
        # Extract query
        query = task_lower.replace("search", "").replace("find", "").strip()
        
        # Extract number
        number_match = re.search(r'\d+', task_lower)
        count = int(number_match.group()) if number_match else 3
        
        return {
            "reasoning": "Simple fallback plan (Nova unavailable)",
            "action": "search",
            "query": query,
            "count": count,
            "expected_outcome": f"Search results for '{query}'"
        }
    
    def adapt_plan(self, original_plan, error_context):
        """
        AGENTIC ADAPTATION: If something fails, Nova creates a new plan
        
        This shows true agent behavior - adapting to problems
        
        Args:
            original_plan: The plan that failed
            error_context: What went wrong
            
        Returns:
            Adapted plan
        """
        
        prompt = f"""You are a web automation agent. Your plan encountered errors.

Original Plan:
{json.dumps(original_plan, indent=2)}

What Went Wrong:
{error_context}

Think about:
1. Why did this fail?
2. How can we achieve the same goal differently?
3. Should we reduce the number of results?
4. Should we adjust the search query?

Create a NEW plan that avoids this error. Return ONLY JSON:

{{
  "reasoning": "why the original failed and how this is better",
  "action": "search",
  "query": "adjusted search query",
  "count": adjusted_number,
  "expected_outcome": "what should work now"
}}"""

        try:
            body = json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ],
                "inferenceConfig": {
                    "maxTokens": 300,
                    "temperature": 0.5
                }
            })
            
            response = bedrock.invoke_model(
                modelId=self.model_id,
                body=body,
                contentType="application/json",
                accept="application/json"
            )
            
            result = json.loads(response["body"].read())
            text = result["output"]["message"]["content"][0]["text"]
            
            json_match = re.search(r"\{.*\}", text, re.DOTALL)
            
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: reduce count
                return {
                    "reasoning": "Reducing result count to avoid errors",
                    "action": "search",
                    "query": original_plan.get("query", ""),
                    "count": max(1, original_plan.get("count", 3) - 1),
                    "expected_outcome": "Fewer results should be more reliable"
                }
                
        except Exception as e:
            print(f"Adaptation error: {e}")
            return original_plan
    
    def reflect_on_results(self, task, plan, results):
        """
        AGENTIC REFLECTION: Nova analyzes what happened
        
        The agent looks at results and provides insights
        
        Args:
            task: Original task
            plan: Executed plan
            results: What happened
            
        Returns:
            Analysis summary
        """
        
        prompt = f"""You are analyzing web automation results.

User's Task: {task}

Plan You Created:
{json.dumps(plan, indent=2)}

What Happened:
- Success: {results.get('success', False)}
- URLs Opened: {len(results.get('opened_urls', []))}
- Errors: {len(results.get('errors', []))}

Provide a brief analysis (2-3 sentences):
1. Was the task successful?
2. What was accomplished?
3. Any issues or improvements needed?

Keep it concise and helpful."""

        try:
            body = json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ],
                "inferenceConfig": {
                    "maxTokens": 150,
                    "temperature": 0.4
                }
            })
            
            response = bedrock.invoke_model(
                modelId=self.model_id,
                body=body,
                contentType="application/json",
                accept="application/json"
            )
            
            result = json.loads(response["body"].read())
            return result["output"]["message"]["content"][0]["text"]
            
        except Exception as e:
            return f"Automation completed. Opened {len(results.get('opened_urls', []))} results."


# Legacy function for backward compatibility
def nova_plan(task):
    """
    Simple planning function (backward compatible with your original code)
    
    Args:
        task: Natural language task
        
    Returns:
        JSON plan string
    """
    agent = NovaAgent()
    plan = agent.plan_workflow(task)
    
    # Return simplified format for backward compatibility
    return json.dumps({
        "action": plan.get("action", "search"),
        "query": plan.get("query", ""),
        "count": plan.get("count", 3)
    })


# Global agent instance
_agent = None

def get_agent():
    """Get or create Nova agent instance"""
    global _agent
    if _agent is None:
        _agent = NovaAgent()
    return _agent
