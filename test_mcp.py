#!/usr/bin/env python3
"""
Test script for Smart Food & Coffee MCP Server
"""
import requests
import json
import time
from typing import Dict, Any

def test_mcp_connection():
    """Test basic MCP connection"""
    url = "http://localhost:8000/mcp"
    
    # Test initialize
    init_payload = {
        "jsonrpc": "2.0",
        "id": "test-init",
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
    
    try:
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            json=init_payload,
            timeout=10
        )
        
        print(f"✅ Initialize Response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Server capabilities: {data.get('result', {}).get('capabilities', {})}")
            return True
        else:
            print(f"❌ Initialize failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_list_tools():
    """Test listing available tools"""
    url = "http://localhost:8000/mcp"
    
    payload = {
        "jsonrpc": "2.0",
        "id": "test-tools",
        "method": "tools/list"
    }
    
    try:
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            json=payload,
            timeout=10
        )
        
        print(f"✅ List Tools Response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            tools = data.get('result', {}).get('tools', [])
            print(f"Available tools: {len(tools)}")
            for tool in tools:
                print(f"  - {tool.get('name')}: {tool.get('description')}")
            return tools
        else:
            print(f"❌ List tools failed: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ List tools failed: {e}")
        return []

def test_restaurant_search():
    """Test restaurant search functionality"""
    url = "http://localhost:8000/mcp"
    
    payload = {
        "jsonrpc": "2.0",
        "id": "test-search",
        "method": "tools/call",
        "params": {
            "name": "search_restaurants",
            "arguments": {
                "location": "San Francisco, CA",
                "food_type": "coffee",
                "radius_meters": 2000,
                "open_now": True
            }
        }
    }
    
    try:
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            json=payload,
            timeout=30  # Restaurant search might take longer
        )
        
        print(f"✅ Restaurant Search Response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            result = data.get('result')
            if result and isinstance(result, list) and len(result) > 0:
                content = result[0].get('content', [])
                if content:
                    search_result = json.loads(content[0].get('text', '{}'))
                    print(f"Search status: {search_result.get('status')}")
                    results = search_result.get('results', [])
                    print(f"Found {len(results)} restaurants")
                    
                    if results:
                        # Show first result
                        first = results[0]
                        print(f"Sample: {first.get('name')} - {first.get('rating')}⭐ - {first.get('address')}")
                        return True
                return True
        else:
            print(f"❌ Restaurant search failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Restaurant search failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Smart Food & Coffee MCP Server")
    print("=" * 50)
    
    # Test 1: Basic connection
    print("\n1. Testing MCP Connection...")
    conn_ok = test_mcp_connection()
    
    # Test 2: List tools
    print("\n2. Testing Tool Discovery...")
    tools = test_list_tools()
    
    # Test 3: Restaurant search
    print("\n3. Testing Restaurant Search...")
    search_ok = test_restaurant_search()
    
    print("\n" + "=" * 50)
    print("🏆 Test Results:")
    print(f"Connection: {'✅' if conn_ok else '❌'}")
    print(f"Tools Available: {'✅' if len(tools) >= 3 else '❌'} ({len(tools)} tools)")
    print(f"Restaurant Search: {'✅' if search_ok else '❌'}")
    
    if conn_ok and len(tools) >= 3 and search_ok:
        print("\n🎉 ALL TESTS PASSED! Ready for deployment!")
    else:
        print("\n⚠️  Some tests failed. Check issues above.")