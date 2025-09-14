#!/usr/bin/env python3
"""
Simple proxy server to make FastMCP compatible with Poke
Converts Poke's Accept headers to what FastMCP expects
"""

import os
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json

app = FastAPI(title="Poke-FastMCP Proxy")

# Add CORS middleware for Poke compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# The actual FastMCP server URL (pointing to Render deployment)
FASTMCP_URL = "https://fastmcp-server-rpo4.onrender.com/mcp"

@app.post("/mcp")
async def proxy_to_fastmcp(request: Request):
    """Proxy requests from Poke to FastMCP with corrected headers"""
    
    # Get the request body
    body = await request.body()
    
    # Get original headers and fix the Accept header
    headers = dict(request.headers)
    
    # This is the key fix: add text/event-stream to Accept header
    if "accept" in headers and "text/event-stream" not in headers["accept"]:
        headers["accept"] = "application/json, text/event-stream"
    
    # Remove host header to avoid conflicts
    headers.pop("host", None)
    
    print(f"🔄 Proxying request to FastMCP:")
    print(f"   Original Accept: {request.headers.get('accept')}")
    print(f"   Modified Accept: {headers.get('accept')}")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Forward request to FastMCP
            response = await client.post(
                FASTMCP_URL,
                content=body,
                headers=headers
            )
            
            print(f"✅ FastMCP responded with status: {response.status_code}")
            
            # Return the FastMCP response back to Poke
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.headers.get("content-type")
            )
            
    except Exception as e:
        print(f"❌ Proxy error: {e}")
        return Response(
            content=json.dumps({
                "jsonrpc": "2.0",
                "id": "proxy-error",
                "error": {
                    "code": -32603,
                    "message": f"Proxy error: {str(e)}"
                }
            }),
            status_code=500,
            media_type="application/json"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "proxy": "poke-fastmcp-proxy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", int(os.environ.get("PROXY_PORT", 8001))))
    print(f"🚀 Starting Poke-FastMCP Proxy on port {port}")
    print(f"📡 Proxying to: {FASTMCP_URL}")
    print(f"🔗 Use this URL in Poke: http://localhost:{port}/mcp")
    
    uvicorn.run(app, host="0.0.0.0", port=port)