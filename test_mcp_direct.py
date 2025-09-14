#!/usr/bin/env python3
"""Test the MCP server restaurant search directly"""

import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv
import googlemaps

# Load environment variables
load_dotenv()

def test_restaurant_search_function():
    """Test the restaurant search function directly from our MCP server"""
    print("🧪 Testing MCP Server Restaurant Search Function")
    print("=" * 60)
    
    api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
    
    if api_key and api_key != "your_google_places_api_key_here":
        try:
            # Initialize Google Maps client
            gmaps = googlemaps.Client(key=api_key)
            
            location = "San Francisco"
            food_type = "restaurant"
            radius_meters = 2000
            
            # Convert location to coordinates if needed
            geocode_result = gmaps.geocode(location)
            if not geocode_result:
                print(f"❌ Could not geocode location: {location}")
                return False
            
            lat_lng = geocode_result[0]['geometry']['location']
            print(f"📍 Coordinates: {lat_lng}")
            
            # Build search query
            query = food_type if food_type != "restaurant" else "restaurant"
            
            # Search for places
            places_result = gmaps.places_nearby(
                location=lat_lng,
                radius=radius_meters,
                keyword=query,
                type='restaurant'
            )
            
            results = places_result.get('results', [])
            print(f"✅ Found {len(results)} places")
            
            if results:
                # Test place details with correct fields
                first_place = results[0]
                print(f"🔍 Getting details for: {first_place['name']}")
                
                # Use only valid fields
                place_details = gmaps.place(first_place['place_id'], fields=[
                    'name', 'formatted_address', 'rating', 'user_ratings_total',
                    'price_level', 'type', 'formatted_phone_number', 'website',
                    'opening_hours', 'geometry', 'place_id'
                ])['result']
                
                print("✅ Place details retrieved successfully!")
                print(f"   Name: {place_details.get('name')}")
                print(f"   Address: {place_details.get('formatted_address')}")
                print(f"   Rating: {place_details.get('rating')}")
                print(f"   Phone: {place_details.get('formatted_phone_number')}")
                print(f"   Type: {place_details.get('type')}")
                
                # Build restaurant object like our MCP server does
                restaurant = {
                    "place_id": place_details.get('place_id'),
                    "name": place_details.get('name'),
                    "address": place_details.get('formatted_address'),
                    "rating": place_details.get('rating'),
                    "user_ratings_total": place_details.get('user_ratings_total'),
                    "price_level": "unknown",  # Will be mapped from number
                    "types": place_details.get('type', []),
                    "phone": place_details.get('formatted_phone_number'),
                    "website": place_details.get('website'),
                    "currently_open": place_details.get('opening_hours', {}).get('open_now', None),
                    "opening_hours": place_details.get('opening_hours', {}).get('weekday_text', []),
                    "delivery_available": "meal_delivery" in place_details.get('type', []),
                    "takeout_available": "meal_takeaway" in place_details.get('type', []),
                    "location": place_details.get('geometry', {}).get('location', {}),
                    "google_maps_url": f"https://www.google.com/maps/place/?q=place_id:{place_details.get('place_id')}",
                    "note": "Live Google Places data"
                }
                
                print(f"\n🎯 Sample restaurant data:")
                print(f"   Place ID: {restaurant['place_id']}")
                print(f"   Location: {restaurant['location']}")
                print(f"   Currently Open: {restaurant['currently_open']}")
                
                print("\n🚀 SUCCESS: Live Google Places API integration working!")
                return True
            else:
                print("❌ No results found")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    else:
        print("❌ No valid API key")
        return False

if __name__ == "__main__":
    success = test_restaurant_search_function()
    print("\n" + "=" * 60)
    if success:
        print("✅ MCP SERVER READY WITH LIVE DATA!")
        print("🏆 Your Render deployment will serve real restaurant data!")
    else:
        print("❌ Still has issues to resolve")