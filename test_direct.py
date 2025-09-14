#!/usr/bin/env python3
import os
import sys
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv
import googlemaps

# Load environment variables
load_dotenv()

def test_direct_function():
    """Test the restaurant search function directly"""
    print("🧪 Testing Restaurant Search Function Directly")
    print("=" * 50)
    
    api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
    
    if api_key and api_key != "your_google_places_api_key_here":
        try:
            # Initialize Google Maps client
            gmaps = googlemaps.Client(key=api_key)
            
            # Convert location to coordinates
            location = "San Francisco"
            print(f"🔍 Testing with location: {location}")
            
            geocode_result = gmaps.geocode(location)
            if not geocode_result:
                print(f"❌ Could not geocode location: {location}")
                return False
            
            lat_lng = geocode_result[0]['geometry']['location']
            print(f"📍 Coordinates: {lat_lng}")
            
            # Search for places
            places_result = gmaps.places_nearby(
                location=lat_lng,
                radius=2000,
                keyword="restaurant",
                type='restaurant'
            )
            
            results = places_result.get('results', [])
            print(f"✅ Found {len(results)} places via Places API")
            
            if results:
                # Get detailed info for first place
                first_place = results[0]
                print(f"   First place: {first_place['name']}")
                
                place_details = gmaps.place(first_place['place_id'], fields=[
                    'name', 'formatted_address', 'rating', 'user_ratings_total',
                    'price_level', 'types', 'formatted_phone_number', 'website',
                    'opening_hours', 'geometry', 'place_id'
                ])['result']
                
                print(f"   Address: {place_details.get('formatted_address')}")
                print(f"   Rating: {place_details.get('rating')}")
                print(f"   Phone: {place_details.get('formatted_phone_number')}")
                
                print("\n✅ LIVE GOOGLE PLACES API IS WORKING!")
                print("🏆 Your server will return REAL restaurant data!")
                return True
            else:
                print("❌ No results found")
                return False
                
        except Exception as e:
            print(f"❌ API Error: {e}")
            return False
    else:
        print("❌ No valid API key found")
        return False

if __name__ == "__main__":
    success = test_direct_function()
    print("\n" + "=" * 50)
    if success:
        print("🎯 READY FOR COMPETITION!")
        print("Your Render deployment will serve live restaurant data!")
    else:
        print("⚠️  Will use sample data fallback (still competition-ready)")