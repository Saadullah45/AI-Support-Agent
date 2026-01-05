from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import asyncio
from agent import app as agent_app  # Imports your compiled LangGraph

app = FastAPI(title="AI Support Desk API")

# Define the request body format
class ChatRequest(BaseModel):
    message: str

async def stream_agent_updates(user_input: str):
    """
    Streams updates from the LangGraph agent as they occur.
    """
    # Initialize the graph state with the user message
    initial_state = {"messages": [("user", user_input)]}
    
    # We use .astream to get updates node-by-node
    async for chunk in agent_app.astream(initial_state, stream_mode="updates"):
        for node_name, output in chunk.items():
            # Create a structured log of which node is running
            data = {
                "node": node_name,
                "content": str(output.get("messages", [-1])[-1].content) if "messages" in output else "Processing..."
            }
            yield f"data: {json.dumps(data)}\n\n"
            await asyncio.sleep(0.1) # Small delay for smoother streaming

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint to receive user messages and return a streamed agent response.
    """
    return StreamingResponse(
        stream_agent_updates(request.message), 
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)