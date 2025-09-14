#!/usr/bin/env python3
"""Deep debug for Geocoding API issues"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def debug_geocoding_specific():
    """Debug Geocoding API specifically"""
    api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
    
    print("🔍 GEOCODING API DEEP DEBUG")
    print("=" * 50)
    print(f"API Key: {api_key[:15]}...{api_key[-5:]}")
    print()
    
    # Test with minimal request
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': 'San Francisco',
        'key': api_key
    }
    
    print(f"🧪 Testing Geocoding API:")
    print(f"   URL: {url}")
    print(f"   Params: address=San Francisco, key=***")
    print()
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        print(f"📡 Response Status Code: {response.status_code}")
        print(f"📋 Response Body:")
        print(f"   Status: {data.get('status')}")
        print(f"   Error Message: {data.get('error_message', 'None')}")
        
        if data.get('status') == 'REQUEST_DENIED':
            print()
            print("🚨 REQUEST_DENIED Analysis:")
            error_msg = data.get('error_message', '').lower()
            
            if 'billing' in error_msg:
                print("   💳 ISSUE: Billing not enabled")
                print("   🔧 FIX: Enable billing in Google Cloud Console")
                print("   👉 https://console.cloud.google.com/billing")
                
            elif 'api key not valid' in error_msg or 'api_key_invalid' in error_msg:
                print("   🔑 ISSUE: Invalid API key")
                print("   🔧 FIX: Check API key is correct")
                
            elif 'api not enabled' in error_msg or 'not authorized' in error_msg:
                print("   🚫 ISSUE: Geocoding API not enabled")
                print("   🔧 FIX: Enable Geocoding API")
                print("   👉 https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com")
                
            else:
                print(f"   ❓ UNKNOWN ERROR: {data.get('error_message')}")
            
            print()
            print("🎯 RECOMMENDED ACTIONS:")
            print("1. Check billing is enabled: https://console.cloud.google.com/billing")
            print("2. Enable Geocoding API: https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com")
            print("3. Wait 5 minutes for propagation")
            print("4. Test again")
            
        elif data.get('status') == 'OK':
            print("   ✅ SUCCESS! Geocoding API is working!")
            results = data.get('results', [])
            if results:
                location = results[0]['geometry']['location']
                print(f"   📍 San Francisco coordinates: {location}")
            
        else:
            print(f"   ⚠️  Unexpected status: {data.get('status')}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    print()
    print("=" * 50)

def check_billing_status():
    """Try to detect if billing is the issue"""
    print("💳 CHECKING BILLING INDICATORS")
    print("=" * 30)
    
    api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
    
    # Test a free API vs paid API
    free_api_test = {
        "name": "Maps Static API (has free tier)",
        "url": "https://maps.googleapis.com/maps/api/staticmap",
        "params": {"center": "San Francisco", "zoom": "10", "size": "400x400", "key": api_key}
    }
    
    print("🆓 Testing free-tier API to check if billing is the issue...")
    
    try:
        response = requests.get(free_api_test["url"], params=free_api_test["params"])
        
        if response.status_code == 200:
            print("   ✅ Free API works - billing likely OK")
        else:
            print(f"   ❌ Free API failed - Status: {response.status_code}")
            if response.headers.get('content-type', '').startswith('application/json'):
                data = response.json()
                print(f"   Error: {data}")
    
    except Exception as e:
        print(f"   ❌ Test failed: {e}")

if __name__ == "__main__":
    debug_geocoding_specific()
    print()
    check_billing_status()