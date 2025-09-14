#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def debug_google_places_api():
    """Debug Google Places API issues"""
    api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
    
    print("🔍 DEBUG: Google Places API Configuration")
    print("=" * 50)
    
    # Check API key
    if not api_key:
        print("❌ No API key found in environment")
        return False
    
    print(f"✅ API key found: {api_key[:15]}...{api_key[-5:]}")
    
    # Test with direct HTTP request first (simpler than googlemaps library)
    print("\n🧪 Testing Places API with direct HTTP request...")
    
    # Test 1: Text Search API (simpler endpoint)
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': 'restaurants in San Francisco',
        'key': api_key
    }
    
    try:
        print(f"🌐 Making request to: {url}")
        response = requests.get(url, params=params)
        data = response.json()
        
        print(f"📡 Response status: {response.status_code}")
        print(f"📋 Response data: {data}")
        
        if response.status_code == 200:
            if data.get('status') == 'OK':
                print("✅ Places API is working!")
                results = data.get('results', [])
                print(f"📍 Found {len(results)} places")
                if results:
                    print(f"   First result: {results[0]['name']}")
                return True
            else:
                print(f"❌ API Error Status: {data.get('status')}")
                print(f"   Error message: {data.get('error_message', 'No message')}")
                
                # Specific error handling
                if data.get('status') == 'REQUEST_DENIED':
                    print("\n💡 REQUEST_DENIED means:")
                    print("   1. Places API is not enabled for this project")
                    print("   2. API key doesn't have Places API permissions")
                    print("   3. Billing is not set up")
                    
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def check_api_key_permissions():
    """Check what APIs this key has access to"""
    api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
    
    print("\n🔑 Checking API Key Permissions...")
    
    # Test different Google APIs to see what's enabled
    apis_to_test = [
        ("Geocoding", "https://maps.googleapis.com/maps/api/geocode/json", {"address": "San Francisco"}),
        ("Places Nearby", "https://maps.googleapis.com/maps/api/place/nearbysearch/json", 
         {"location": "37.7749,-122.4194", "radius": "1000", "type": "restaurant"}),
        ("Places Text Search", "https://maps.googleapis.com/maps/api/place/textsearch/json", 
         {"query": "restaurants in San Francisco"}),
    ]
    
    for api_name, url, params in apis_to_test:
        params['key'] = api_key
        try:
            response = requests.get(url, params=params)
            data = response.json()
            status = data.get('status', 'UNKNOWN')
            
            if status == 'OK':
                print(f"   ✅ {api_name}: Working")
            elif status == 'REQUEST_DENIED':
                print(f"   ❌ {api_name}: REQUEST_DENIED (not enabled)")
            else:
                print(f"   ⚠️  {api_name}: {status}")
                
        except Exception as e:
            print(f"   ❌ {api_name}: Error - {e}")

if __name__ == "__main__":
    debug_google_places_api()
    check_api_key_permissions()
    print("\n" + "=" * 50)
    print("🎯 Next Steps:")
    print("1. Go to: https://console.cloud.google.com/apis/library")
    print("2. Search for 'Places API' and enable it")
    print("3. Make sure billing is enabled")
    print("4. Wait 2-3 minutes and test again")