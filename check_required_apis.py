#!/usr/bin/env python3
"""Check which Google APIs need to be enabled for our MCP server"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def check_google_apis():
    """Check which Google APIs we need and their status"""
    api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
    
    print("🔍 GOOGLE PLACES API REQUIREMENTS ANALYSIS")
    print("=" * 60)
    print(f"API Key: {api_key[:15]}...{api_key[-5:]}")
    print()
    
    # Required APIs for our restaurant search functionality
    required_apis = [
        {
            "name": "Geocoding API",
            "description": "Convert addresses to coordinates",
            "url": "https://maps.googleapis.com/maps/api/geocode/json",
            "test_params": {"address": "San Francisco, CA"},
            "enable_url": "https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com"
        },
        {
            "name": "Places API (New)",
            "description": "Search for places and get details",
            "url": "https://maps.googleapis.com/maps/api/place/textsearch/json",
            "test_params": {"query": "restaurants in San Francisco"},
            "enable_url": "https://console.cloud.google.com/apis/library/places-backend.googleapis.com"
        },
        {
            "name": "Places API - Nearby Search",
            "description": "Find nearby places by location",
            "url": "https://maps.googleapis.com/maps/api/place/nearbysearch/json", 
            "test_params": {"location": "37.7749,-122.4194", "radius": "1000", "type": "restaurant"},
            "enable_url": "https://console.cloud.google.com/apis/library/places-backend.googleapis.com"
        },
        {
            "name": "Places API - Place Details",
            "description": "Get detailed info about a place",
            "url": "https://maps.googleapis.com/maps/api/place/details/json",
            "test_params": {"place_id": "ChIJIQBpAG2ahYAR_6128GcTUEo", "fields": "name,rating,formatted_phone_number"},
            "enable_url": "https://console.cloud.google.com/apis/library/places-backend.googleapis.com"
        }
    ]
    
    results = []
    
    for api in required_apis:
        print(f"🧪 Testing: {api['name']}")
        print(f"   Purpose: {api['description']}")
        
        params = api['test_params'].copy()
        params['key'] = api_key
        
        try:
            response = requests.get(api['url'], params=params, timeout=10)
            data = response.json()
            status = data.get('status', 'UNKNOWN')
            
            if status == 'OK':
                print(f"   ✅ WORKING - {status}")
                results.append({"name": api['name'], "status": "working", "url": api['enable_url']})
            elif status == 'REQUEST_DENIED':
                print(f"   ❌ BLOCKED - {status}")
                print(f"   🔧 Enable at: {api['enable_url']}")
                results.append({"name": api['name'], "status": "blocked", "url": api['enable_url']})
            elif status == 'ZERO_RESULTS':
                print(f"   ✅ API WORKING (no results for test query)")
                results.append({"name": api['name'], "status": "working", "url": api['enable_url']})
            else:
                print(f"   ⚠️  UNKNOWN - {status}")
                error_msg = data.get('error_message', '')
                if error_msg:
                    print(f"   Error: {error_msg}")
                results.append({"name": api['name'], "status": "unknown", "url": api['enable_url']})
                
        except Exception as e:
            print(f"   ❌ ERROR - {str(e)}")
            results.append({"name": api['name'], "status": "error", "url": api['enable_url']})
        
        print()
    
    # Summary
    print("=" * 60)
    print("📋 SUMMARY & ACTION REQUIRED")
    print("=" * 60)
    
    blocked_apis = [r for r in results if r['status'] == 'blocked']
    working_apis = [r for r in results if r['status'] == 'working']
    
    print(f"✅ Working APIs: {len(working_apis)}")
    for api in working_apis:
        print(f"   • {api['name']}")
    
    if blocked_apis:
        print(f"\n❌ Blocked APIs: {len(blocked_apis)}")
        print("🔧 YOU NEED TO ENABLE THESE:")
        for api in blocked_apis:
            print(f"   • {api['name']}")
            print(f"     👉 {api['url']}")
        
        print(f"\n🎯 QUICK ENABLE ALL PLACES APIs:")
        print("👉 https://console.cloud.google.com/apis/library/places-backend.googleapis.com")
        print("👉 https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com") 
        print("\n📋 Steps:")
        print("1. Click the links above")
        print("2. Click 'ENABLE' button for each API")
        print("3. Wait 2-3 minutes for activation")
        print("4. Test again")
        
    else:
        print("\n🎉 ALL APIS WORKING! Ready for live-only mode!")
    
    return len(blocked_apis) == 0

if __name__ == "__main__":
    all_working = check_google_apis()
    print(f"\n🏆 Ready for competition: {'YES' if all_working else 'AFTER enabling APIs'}")