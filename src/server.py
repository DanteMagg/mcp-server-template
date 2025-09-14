#!/usr/bin/env python3
import os
import sys
from typing import List, Dict, Optional, Any
from fastmcp import FastMCP
from dotenv import load_dotenv
import googlemaps
import requests

# Load environment variables
load_dotenv()

mcp = FastMCP("Smart Food & Coffee MCP Server")

@mcp.tool(description="Greet a user by name with a welcome message from the MCP server")
def greet(name: str) -> str:
    return f"Hello, {name}! Welcome to our Smart Food & Coffee MCP server!"

@mcp.tool(description="Get information about the MCP server including name, version, environment, and Python version")
def get_server_info() -> dict:
    return {
        "server_name": "Smart Food & Coffee MCP Server",
        "version": "1.0.0",
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "python_version": os.sys.version.split()[0]
    }

@mcp.tool(description="Search for nearby restaurants based on location and food preferences")
def search_restaurants(
    location: str,
    food_type: str = "restaurant",
    radius_meters: int = 5000,
    price_level: Optional[str] = None,
    open_now: bool = False
) -> Dict[str, Any]:
    """
    Search for nearby restaurants using Google Places API with fallback to sample data
    
    Args:
        location: Address, city, or "latitude,longitude" format
        food_type: Type of food/restaurant (coffee, lunch, dinner, pizza, etc.)
        radius_meters: Search radius in meters (default 5000m = ~3 miles)
        price_level: Price level filter (free, inexpensive, moderate, expensive, very_expensive)
        open_now: Filter for currently open restaurants
        
    Returns:
        Dictionary with restaurant results and metadata
    """
    
    api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
    
    if api_key and api_key != "your_google_places_api_key_here":
        try:
            # Initialize Google Maps client
            gmaps = googlemaps.Client(key=api_key)
            
            # Convert location to coordinates if needed
            geocode_result = gmaps.geocode(location)
            if not geocode_result:
                raise Exception(f"Could not geocode location: {location}")
            
            lat_lng = geocode_result[0]['geometry']['location']
            
            # Build search query
            query = food_type if food_type != "restaurant" else "restaurant"
            
            # Search for places
            places_result = gmaps.places_nearby(
                location=lat_lng,
                radius=radius_meters,
                keyword=query,
                type='restaurant',
                open_now=open_now if open_now else None
            )
            
            restaurants = []
            for place in places_result.get('results', [])[:10]:  # Limit to 10 results
                # Get detailed place info
                place_details = gmaps.place(place['place_id'], fields=[
                    'name', 'formatted_address', 'rating', 'user_ratings_total',
                    'price_level', 'type', 'formatted_phone_number', 'website',
                    'opening_hours', 'geometry', 'place_id'
                ])['result']
                
                # Map price level numbers to strings
                price_mapping = {0: "free", 1: "inexpensive", 2: "moderate", 3: "expensive", 4: "very_expensive"}
                place_price = price_mapping.get(place_details.get('price_level'), "unknown")
                
                # Skip if price level filter doesn't match
                if price_level and place_price != price_level:
                    continue
                
                restaurant = {
                    "place_id": place_details.get('place_id'),
                    "name": place_details.get('name'),
                    "address": place_details.get('formatted_address'),
                    "rating": place_details.get('rating'),
                    "user_ratings_total": place_details.get('user_ratings_total'),
                    "price_level": place_price,
                    "types": place_details.get('type', []),
                    "phone": place_details.get('formatted_phone_number'),
                    "website": place_details.get('website'),
                    "currently_open": place_details.get('opening_hours', {}).get('open_now', None),
                    "opening_hours": place_details.get('opening_hours', {}).get('weekday_text', []),
                    "delivery_available": "meal_delivery" in place_details.get('types', []),
                    "takeout_available": "meal_takeaway" in place_details.get('types', []),
                    "location": place_details.get('geometry', {}).get('location', {}),
                    "google_maps_url": f"https://www.google.com/maps/place/?q=place_id:{place_details.get('place_id')}",
                    "note": "Live Google Places data"
                }
                restaurants.append(restaurant)
            
            return {
                "status": "success",
                "data_type": "live_google_places",
                "message": "Live restaurant data from Google Places API",
                "location": {
                    "query": location,
                    "coordinates": lat_lng
                },
                "search_params": {
                    "food_type": food_type,
                    "radius_meters": radius_meters,
                    "price_level": price_level,
                    "open_now": open_now
                },
                "results": restaurants,
                "total_found": len(restaurants),
                "automation_examples": [
                    f"Live data for: 'Find {food_type} in {location}'",
                    f"Real results for: 'I need {food_type} for lunch'",
                    f"Actual places for: 'Show me {price_level or 'good'} {food_type} options'"
                ]
            }
            
        except Exception as e:
            print(f"Google Places API error: {e}")
            # Return error - no fallback, live data only
            return {
                "status": "error",
                "data_type": "api_error",
                "message": f"Google Places API error: {str(e)}",
                "location": {"query": location},
                "search_params": {
                    "food_type": food_type,
                    "radius_meters": radius_meters,
                    "price_level": price_level,
                    "open_now": open_now
                },
                "results": [],
                "total_found": 0,
                "error": str(e)
            }
    
    # No API key configured
    return {
        "status": "error",
        "data_type": "no_api_key",
        "message": "Google Places API key not configured",
        "location": {"query": location},
        "search_params": {
            "food_type": food_type,
            "radius_meters": radius_meters,
            "price_level": price_level,
            "open_now": open_now
        },
        "results": [],
        "total_found": 0,
        "error": "API key missing or invalid"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print(f"Starting Smart Food & Coffee MCP server on {host}:{port}")
    
    mcp.run(
        transport="http",
        host=host,
        port=port
    )