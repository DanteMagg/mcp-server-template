#!/usr/bin/env python3
"""Debug Poke 400 error by testing MCP protocol directly"""

import requests
import json

def test_mcp_endpoint():
    """Test the MCP endpoint with proper MCP protocol requests"""
    url = "https://fastmcp-server-rpo4.onrender.com/mcp"
    
    print("🔍 DEBUGGING POKE 400 ERROR")
    print("=" * 50)
    print(f"Testing: {url}")
    print()
    
    # Test 1: Basic GET request (should return 406 - this is normal)
    print("🧪 Test 1: HTTP GET (should return 406)")
    try:
        response = requests.get(url, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        if response.status_code == 406:
            print("   ✅ Expected 406 - MCP server is running correctly")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 2: MCP Initialize request (what Poke should send)
    print("🧪 Test 2: MCP Initialize Request")
    mcp_initialize = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        response = requests.post(url, json=mcp_initialize, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type')}")
        
        if response.status_code == 200:
            print("   ✅ MCP Initialize successful!")
            try:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)}")
            except:
                print(f"   Response text: {response.text[:200]}...")
        elif response.status_code == 400:
            print("   ❌ 400 Bad Request - This is what Poke is seeing!")
            print(f"   Response: {response.text}")
            print("   🔍 Possible issues:")
            print("      - MCP protocol version mismatch")
            print("      - Invalid JSON format")
            print("      - Missing required fields")
        else:
            print(f"   ⚠️ Unexpected status: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 3: Check if it's a CORS issue
    print("🧪 Test 3: CORS Headers Check")
    try:
        response = requests.options(url, timeout=10)
        print(f"   OPTIONS Status: {response.status_code}")
        cors_headers = {k: v for k, v in response.headers.items() if 'cors' in k.lower() or 'access-control' in k.lower()}
        if cors_headers:
            print(f"   CORS Headers: {cors_headers}")
        else:
            print("   ❌ No CORS headers found - this could be the issue!")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("=" * 50)
    print("🎯 DIAGNOSIS:")
    print("If Test 1 = 406: Server is running ✅")
    print("If Test 2 = 400: MCP protocol issue ❌") 
    print("If Test 2 = 200: MCP working, Poke config issue ❌")
    print("If Test 3 = No CORS: CORS issue ❌")

if __name__ == "__main__":
    test_mcp_endpoint()