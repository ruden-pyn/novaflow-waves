# NovaFlow Merged - Your Automation + Agentic AI Layer
# Combines your original executor with intelligent planning

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from automation.executor import run_search
from nova_client import get_agent, nova_plan
import json
import asyncio

app = FastAPI(title="NovaFlow Merged - Agentic Web Automation")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for UI
app.mount("/ui", StaticFiles(directory="ui"), name="ui")

# Prevent concurrent executions
automation_lock = asyncio.Lock()

# Store history
execution_history = []

@app.get("/")
def home():
    return {
        "message": "NovaFlow Merged API running",
        "version": "Your Code + Agentic AI",
        "capabilities": [
            "Your original executor",
            "Agentic planning with Nova",
            "Error adaptation",
            "Result reflection"
        ]
    }

@app.get("/command")
async def command(task: str):
    """
    AGENTIC WORKFLOW - Your executor with AI planning
    
    Flow:
    1. Nova plans the best approach (AGENTIC)
    2. Your executor runs the automation (YOUR CODE)
    3. Nova reflects on results (AGENTIC)
    4. If errors, Nova adapts (AGENTIC)
    
    Args:
        task: Natural language instruction
        
    Returns:
        Results with agent reasoning
    """
    
    # Prevent multiple simultaneous runs
    if automation_lock.locked():
        return {
            "status": "busy",
            "message": "Automation already running. Please wait."
        }
    
    async with automation_lock:
        try:
            print(f"\n{'='*60}")
            print(f"USER TASK: {task}")
            print(f"{'='*60}\n")
            
            agent = get_agent()
            
            # STAGE 1: AGENTIC PLANNING
            print("🧠 Stage 1: Agent Planning...")
            plan = agent.plan_workflow(task)
            
            print(f"✓ Plan Created")
            print(f"Reasoning: {plan.get('reasoning', 'N/A')}")
            print(f"Action: {plan.get('action')}")
            print(f"Query: {plan.get('query')}")
            print(f"Count: {plan.get('count')}")
            print()
            
            # STAGE 2: EXECUTION (YOUR CODE!)
            print("⚙️  Stage 2: Running Your Executor...")
            
            # Run your automation in a thread (non-blocking)
            result = await asyncio.to_thread(
                run_search,
                plan.get("query", ""),
                plan.get("count", 3)
            )
            
            print(f"✓ Execution Complete")
            print(f"Success: {result.get('success')}")
            print(f"URLs Opened: {len(result.get('opened_urls', []))}")
            print(f"Errors: {len(result.get('errors', []))}")
            print()
            
            # STAGE 3: ADAPTATION (if needed)
            adapted_plan = None
            if not result.get("success") or result.get("errors"):
                print("🔄 Stage 3: Agent Adapting to Errors...")
                error_context = "; ".join(result.get("errors", []))
                adapted_plan = agent.adapt_plan(plan, error_context)
                print(f"New strategy: {adapted_plan.get('reasoning', 'N/A')}")
                print()
            
            # STAGE 4: REFLECTION
            print("💭 Stage 4: Agent Reflection...")
            reflection = agent.reflect_on_results(task, plan, result)
            print(f"Analysis: {reflection}")
            print()
            
            print(f"{'='*60}")
            print(f"WORKFLOW COMPLETE")
            print(f"{'='*60}\n")
            
            # Store in history
            execution_record = {
                "task": task,
                "agent_plan": plan,
                "execution_result": result,
                "adapted_plan": adapted_plan,
                "agent_reflection": reflection
            }
            
            execution_history.append(execution_record)
            
            return {
                "status": "success",
                "task": task,
                "agent_reasoning": plan.get("reasoning"),
                "plan": plan,
                "result": result,
                "adapted_plan": adapted_plan,
                "reflection": reflection,
                "urls_opened": result.get("opened_urls", [])
            }
            
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                "status": "error",
                "error": str(e)
            }

@app.get("/simple")
async def simple_command(task: str):
    """
    BACKWARD COMPATIBLE - Works like your original code
    
    Args:
        task: Natural language instruction
        
    Returns:
        Simple execution results
    """
    
    if automation_lock.locked():
        return {"error": "Automation busy"}
    
    async with automation_lock:
        try:
            print("User task:", task)
            
            # Use simple planning
            plan_json = nova_plan(task)
            plan = json.loads(plan_json)
            
            print("Nova plan:", plan)
            
            # Run your automation
            result = await asyncio.to_thread(
                run_search,
                plan.get("query", ""),
                plan.get("count", 3)
            )
            
            return {
                "status": "success",
                "plan": plan,
                "result": result
            }
            
        except Exception as e:
            print("ERROR:", e)
            return {"error": str(e)}

@app.get("/history")
def get_history(limit: int = 10):
    """Get execution history"""
    return {
        "total": len(execution_history),
        "recent": execution_history[-limit:]
    }

@app.get("/clear-history")
def clear_history():
    """Clear execution history"""
    global execution_history
    execution_history = []
    return {"status": "cleared"}

@app.get("/health")
def health_check():
    """Health check"""
    try:
        agent = get_agent()
        test = agent.plan_workflow("test")
        
        return {
            "status": "healthy",
            "nova": "connected",
            "automation": "ready",
            "your_executor": "working"
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("NovaFlow Merged - Your Automation + Agentic AI")
    print("="*60)
    print("\nYour original executor is running!")
    print("Enhanced with:")
    print("  ✓ Agentic planning")
    print("  ✓ Error adaptation")
    print("  ✓ Result reflection")
    print("\nStarting server...")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
