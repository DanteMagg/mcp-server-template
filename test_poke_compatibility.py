#!/usr/bin/env python3
"""Test if our server changes make it compatible with Poke's headers"""

import requests
import json
import time

def test_poke_headers():
    """Test with headers that Poke typically sends"""
    # Test locally first
    local_url = "http://localhost:8000/mcp"
    
    print("🧪 TESTING POKE COMPATIBILITY")
    print("=" * 50)
    
    # Poke-style headers (typically just application/json)
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
                "name": "poke-test",
                "version": "1.0.0"
            }
        }
    }
    
    print("🧪 Testing with Poke-style headers:")
    print(f"   Headers: {poke_headers}")
    print()
    
    try:
        print("📡 Sending MCP Initialize request...")
        response = requests.post(local_url, json=mcp_initialize, headers=poke_headers, timeout=10)
        
        print(f"✅ Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type', 'Not set')}")
        
        if response.status_code == 200:
            print("🎉 SUCCESS! Server accepts Poke headers!")
            try:
                # Handle both JSON and SSE responses
                if 'application/json' in response.headers.get('content-type', ''):
                    data = response.json()
                    print("📋 JSON Response:")
                    print(json.dumps(data, indent=2))
                elif 'text/event-stream' in response.headers.get('content-type', ''):
                    print("📋 SSE Response:")
                    print(response.text)
                    # Parse SSE data
                    lines = response.text.strip().split('\n')
                    for line in lines:
                        if line.startswith('data: '):
                            json_data = line[6:]  # Remove 'data: '
                            try:
                                parsed = json.loads(json_data)
                                print("Parsed JSON from SSE:")
                                print(json.dumps(parsed, indent=2))
                            except:
                                print(f"Raw data: {json_data}")
                else:
                    print(f"📋 Raw Response: {response.text}")
                    
            except Exception as e:
                print(f"Response parsing error: {e}")
                print(f"Raw response: {response.text}")
                
        elif response.status_code == 406:
            print("❌ Still 406 - headers still not accepted")
            print(f"   Response: {response.text}")
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - server not running locally")
        print("   Start server with: python src/server.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
        
    return response.status_code == 200

if __name__ == "__main__":
    success = test_poke_headers()
    print("\n" + "=" * 50)
    if success:
        print("✅ READY FOR POKE!")
        print("🚀 Server accepts Poke-style headers")
    else:
        print("❌ Still needs fixes for Poke compatibility")