#!/usr/bin/env python3
"""Test the Poke proxy with Poke-style headers"""

import requests
import json

def test_proxy():
    """Test the proxy with Poke-style headers"""
    proxy_url = "http://localhost:8001/mcp"
    
    print("🧪 TESTING POKE PROXY")
    print("=" * 50)
    
    # Poke-style headers (just application/json)
    poke_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",  # This is what Poke sends
        "User-Agent": "Poke/1.0"
    }
    
    mcp_initialize = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "poke-via-proxy",
                "version": "1.0.0"
            }
        }
    }
    
    print("📡 Testing proxy with Poke-style headers:")
    print(f"   URL: {proxy_url}")
    print(f"   Headers: {poke_headers}")
    print()
    
    try:
        response = requests.post(proxy_url, json=mcp_initialize, headers=poke_headers, timeout=15)
        
        print(f"✅ Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type')}")
        
        if response.status_code == 200:
            print("🎉 SUCCESS! Proxy fixed the header issue!")
            
            try:
                if 'application/json' in response.headers.get('content-type', ''):
                    data = response.json()
                    print("📋 JSON Response:")
                    print(json.dumps(data, indent=2))
                elif 'text/event-stream' in response.headers.get('content-type', ''):
                    print("📋 SSE Response:")
                    print(response.text)
                    # Parse SSE
                    lines = response.text.strip().split('\n')
                    for line in lines:
                        if line.startswith('data: '):
                            json_data = line[6:]
                            try:
                                parsed = json.loads(json_data)
                                print("\n📋 Parsed JSON from SSE:")
                                print(json.dumps(parsed, indent=2))
                            except:
                                pass
                else:
                    print(f"📋 Raw Response: {response.text}")
                    
            except Exception as e:
                print(f"Response parsing: {e}")
                print(f"Raw response: {response.text}")
                
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"   Response: {response.text}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    success = test_proxy()
    print("\n" + "=" * 50)
    if success:
        print("🎯 SOLUTION FOUND!")
        print("✅ Proxy successfully converts Poke headers for FastMCP")
        print("🔗 Use in Poke: http://localhost:8001/mcp")
        print("📡 Or with tunnel for remote access")
    else:
        print("❌ Proxy still needs debugging")