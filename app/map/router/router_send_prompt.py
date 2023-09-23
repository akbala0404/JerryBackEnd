from fastapi import APIRouter, Depends, status, HTTPException
from app.utils import AppModel, BaseModel
from pydantic import Field
from typing import Any
from ..service import Service, get_service
from . import router
import requests
import json
import logging
import string
import ast

class RouteRequest(BaseModel):
    origin: str
    destination: str
    mode: str = "driving"

class RouteResponse(BaseModel):
    route: str


@router.post("/route", response_model=RouteResponse)
def get_route(request: RouteRequest) -> RouteResponse:
    route_data = get_google_maps_route(request.origin, request.destination, request.mode)

    if not route_data:
        raise HTTPException(status_code=400, detail="Could not fetch route")

    # You can extract and format the desired data from route_data as needed
    # For simplicity, we'll return the 'summary' of the route.
    return RouteResponse(route=route_data["summary"])

def get_google_maps_route(origin: str, destination: str, mode: str) -> dict:
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

    return data["routes"][0]

