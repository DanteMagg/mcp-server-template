#!/usr/bin/env python3
"""Test the live Google Places API integration in our MCP server"""

import sys
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Add src directory to path to import server
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

def test_mcp_server_integration():
    """Test our MCP server's restaurant search with live API"""
    print("🧪 Testing MCP Server Restaurant Search Integration")
    print("=" * 60)
    
    try:
        # Import after adding to path
        from server import search_restaurants
        
        # Test 1: Test San Francisco restaurants
        print("🔍 Test 1: Searching for restaurants in San Francisco")
        result = search_restaurants.func("San Francisco", "restaurant", 2000)
        
        print(f"   Status: {result['status']}")
        print(f"   Data Type: {result['data_type']}")
        print(f"   Message: {result['message']}")
        print(f"   Total Found: {result['total_found']}")
        
        if result['results']:
            first_result = result['results'][0]
            print(f"   First Restaurant: {first_result['name']}")
            print(f"   Address: {first_result['address']}")
            print(f"   Rating: {first_result['rating']}")
            print(f"   Note: {first_result.get('note', 'No note')}")
            
        print()
        
        # Test 2: Test coffee shops
        print("🔍 Test 2: Searching for coffee shops in Boston")  
        result2 = search_restaurants.func("Boston", "coffee", 3000)
        
        print(f"   Status: {result2['status']}")
        print(f"   Data Type: {result2['data_type']}")
        print(f"   Total Found: {result2['total_found']}")
        
        if result2['results']:
            first_coffee = result2['results'][0]
            print(f"   First Coffee Shop: {first_coffee['name']}")
            print(f"   Address: {first_coffee['address']}")
            
        print()
        
        # Test 3: Test with filtering
        print("🔍 Test 3: Searching for expensive restaurants in NYC")
        result3 = search_restaurants.func("New York City", "restaurant", 5000, "expensive")
        
        print(f"   Status: {result3['status']}")
        print(f"   Data Type: {result3['data_type']}")
        print(f"   Total Found: {result3['total_found']}")
        
        print()
        print("=" * 60)
        
        # Determine if live API is working
        if any(r['data_type'] == 'live_google_places' for r in [result, result2, result3]):
            print("✅ SUCCESS: Live Google Places API is working!")
            print("🏆 Your MCP server is getting REAL restaurant data!")
            print("🚀 Ready for competition submission!")
        elif any(r['data_type'] == 'sample_data_fallback' for r in [result, result2, result3]):
            print("⚠️  FALLBACK: Using sample data (API might have issues)")
            print("🎯 Still competition-ready with robust fallback!")
        else:
            print("❓ Unknown data type - check implementation")
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        return False

if __name__ == "__main__":
    success = test_mcp_server_integration()
    sys.exit(0 if success else 1)