from array import array

from fastapi import APIRouter, Depends, status, HTTPException
from app.utils import AppModel, BaseModel
from pydantic import Field
from typing import Any, List, Dict, Optional
from ..service import Service, get_service
from . import router
import requests
import json
import logging
import string
import ast

logging.basicConfig(
    level=logging.INFO,  # Set the logging level as needed
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)

class PlaceSearchRequest(BaseModel):
    query: str
    place_type: Optional[str] = None

class RouteRequest(BaseModel):
    origin: str
    destination: str
    mode: str = "driving"

class RouteResponse(BaseModel):
    route: str

class AutocompleteRequest(BaseModel):
    input: str
    language: str = "en"

class FindPlaceRequest(BaseModel):
    input: str
    language: str = "en"

class Place(BaseModel):
    type: str
    name: str
    address: str = ""
    description: str = ""

class PlacesResponse(BaseModel):
    places: str

@router.post("/route", response_model=RouteResponse)
def get_route(request: RouteRequest) -> RouteResponse:
    route_data = get_google_maps_route(request.origin, request.destination, request.mode)

    if not route_data:
        raise HTTPException(status_code=400, detail="Could not fetch route")

    return RouteResponse(route=json.dumps(route_data))


@router.post("/autocomplete", response_model=PlacesResponse)
def autocomplete(request: AutocompleteRequest):
    autocomplete_data = get_google_maps_autocomplete(request.input, request.language)

    # For simplicity, let's assume that the autocomplete data gives us a list of names.
    # You might need to adapt this extraction depending on the actual structure of the returned data.
    names = [prediction['description'] for prediction in autocomplete_data.get('predictions', [])]

    # For your format, you probably need to use the name to find the type, address, etc.
    # This is a mocked way to generate the response you provided:
    places = [Place(type="unknown", name=name) for name in
              names]  # Here, "unknown" is just a placeholder. You'd need a way to map names to types.
    return PlacesResponse(places=json.dumps(autocomplete_data))


@router.post("/findplace", response_model=PlacesResponse)
def find_place(request: FindPlaceRequest):
    place_data = get_google_maps_findplace(request.input, request.language)

    # You'd extract necessary info from place_data, but for this mock, let's assume you get a single place name.
    # Again, adapt this based on the actual structure of the returned data.
    name = place_data.get('candidates', [{}])[0].get('name', "")

    # Construct the Place based on the found name.
    place = Place(type="unknown", name=name)  # "unknown" is a placeholder again.
    return PlacesResponse(places=json.dumps(place_data))


@router.post("/search_places")
def search_places(request_data: PlaceSearchRequest):
    params = {
        "query": request_data.query,
        "type": request_data.place_type,
        "key": "AIzaSyDOtiS_ckxQn7JoyhUjLdasDTU9iL4F2Zc"
    }
    
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise HTTPException(status_code=400, detail="Failed to retrieve data from Google Maps API")
    
def get_google_maps_route(origin: str, destination: str, mode: str) -> dict:
    GOOGLE_MAPS_API_KEY = "AIzaSyDOtiS_ckxQn7JoyhUjLdasDTU9iL4F2Zc"
    base_url = "https://maps.googleapis.com/maps/api/directions/json?"
    params = {
        "origin": origin,
        "destination": destination,
        "key": GOOGLE_MAPS_API_KEY
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if "routes" not in data or not data["routes"]:
        return None

    return data

def get_google_maps_autocomplete(input: str, language: str = "en") -> dict:
    GOOGLE_MAPS_API_KEY = "AIzaSyDOtiS_ckxQn7JoyhUjLdasDTU9iL4F2Zc"
    base_url = "https://maps.googleapis.com/maps/api/place/queryautocomplete/json?"
    params = {
        "input": input,
        "language": language,
        "key": GOOGLE_MAPS_API_KEY
    }

    response = requests.get(base_url, params=params)
    return response.json()

def get_google_maps_findplace(input: str, language: str = "en") -> dict:
    GOOGLE_MAPS_API_KEY = "AIzaSyDOtiS_ckxQn7JoyhUjLdasDTU9iL4F2Zc"
    base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
    params = {
        "input": input,
        "inputtype": "textquery",
        "language": language,
        "key": GOOGLE_MAPS_API_KEY
    }

    response = requests.get(base_url, params=params)
    return response.json()


