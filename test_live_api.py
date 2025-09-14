#!/usr/bin/env python3
import os
import sys
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv
import googlemaps

# Load environment variables
load_dotenv()

def test_google_places_api():
    """Test Google Places API directly"""
    api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
    
    if not api_key or api_key == "your_google_places_api_key_here":
        print("❌ No valid API key found")
        return False
        
    try:
        print(f"✅ API key found: {api_key[:10]}...")
        
        # Initialize Google Maps client
        gmaps = googlemaps.Client(key=api_key)
        
        # Test geocoding first
        location = "San Francisco"
        print(f"🔍 Testing geocoding for: {location}")
        geocode_result = gmaps.geocode(location)
        
        if not geocode_result:
            print("❌ Geocoding failed")
            return False
            
        lat_lng = geocode_result[0]['geometry']['location']
        print(f"✅ Geocoded to: {lat_lng}")
        
        # Test places search
        print("🔍 Testing Places API search...")
        places_result = gmaps.places_nearby(
            location=lat_lng,
            radius=2000,
            keyword="coffee",
            type='restaurant'
        )
        
        results = places_result.get('results', [])
        print(f"✅ Found {len(results)} places")
        
        if results:
            # Test place details
            first_place = results[0]
            print(f"🔍 Testing place details for: {first_place['name']}")
            
            place_details = gmaps.place(first_place['place_id'], fields=[
                'name', 'formatted_address', 'rating', 'user_ratings_total',
                'price_level', 'types', 'formatted_phone_number', 'website',
                'opening_hours', 'geometry', 'place_id'
            ])
            
            details = place_details['result']
            print(f"✅ Place details retrieved:")
            print(f"   Name: {details.get('name')}")
            print(f"   Address: {details.get('formatted_address')}")
            print(f"   Rating: {details.get('rating')}")
            print(f"   Phone: {details.get('formatted_phone_number')}")
            
        return True
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Google Places API Integration")
    print("=" * 50)
    success = test_google_places_api()
    print("=" * 50)
    if success:
        print("✅ Google Places API is working!")
    else:
        print("❌ Google Places API has issues - will use sample data fallback")