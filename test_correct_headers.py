#!/usr/bin/env python3
"""Test MCP server with correct headers that Poke should use"""

import requests
import json

def test_with_correct_headers():
    """Test MCP endpoint with the required Accept headers"""
    url = "https://fastmcp-server-rpo4.onrender.com/mcp"
    
    print("🔧 TESTING WITH CORRECT MCP HEADERS")
    print("=" * 50)
    
    # MCP Initialize request with correct headers
    mcp_initialize = {
        "jsonrpc": "2.0",
        "id": "1", 
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "poke-client",
                "version": "1.0.0"
            }
        }
    }
    
    # The key is including BOTH content types in Accept header
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",  # This is what was missing!
        "User-Agent": "Poke/1.0"
    }
    
    print(f"🧪 Testing MCP Initialize with correct headers:")
    print(f"   URL: {url}")
    print(f"   Headers: {headers}")
    print()
    
    try:
        response = requests.post(url, json=mcp_initialize, headers=headers, timeout=15)
        print(f"✅ Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type')}")
        
        if response.status_code == 200:
            print("🎉 SUCCESS! MCP Initialize worked!")
            try:
                data = response.json()
                print("📋 Server Response:")
                print(json.dumps(data, indent=2))
                
                # Test tools list
                if 'result' in data and 'capabilities' in data['result']:
                    print("\n🛠️ Server Capabilities:")
                    capabilities = data['result']['capabilities']
                    for key, value in capabilities.items():
                        print(f"   {key}: {value}")
                        
            except Exception as e:
                print(f"   Response parsing error: {e}")
                print(f"   Raw response: {response.text}")
                
        elif response.status_code == 406:
            print("❌ Still 406 - header issue persists")
            print(f"   Error: {response.text}")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 SOLUTION FOR POKE:")
    if response.status_code == 200:
        print("✅ MCP server works with correct headers!")
        print("📝 Poke needs to send: Accept: application/json, text/event-stream")
        print("🏆 Your server is working correctly!")
    else:
        print("❌ Still having issues - may need FastMCP configuration")

if __name__ == "__main__":
    test_with_correct_headers()