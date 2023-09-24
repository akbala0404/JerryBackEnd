from fastapi import APIRouter, Depends, status, HTTPException
from app.map.router.router_send_prompt import PlaceSearchRequest, get_google_maps_route, RouteRequest
from app.map.router.router_send_prompt import search_places
from app.utils import AppModel, BaseModel
from pydantic import Field
from typing import Any
from ..service import Service, get_service
from . import router
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

class UserRequest(AppModel):
    request: str
    # userID: str
class UserResponse(AppModel):
    response: str

class ChatRequest(AppModel):
    prompt: str

class ChatResponse(AppModel):
    response: str


# @router.post("/chat", response_model=ChatResponse)
# def chat_with_ai(
#     request: ChatRequest,
#     svc: Service = Depends(get_service),
# ) -> ChatResponse:
#     prompt = request.prompt
#     response = svc.chat_service.get_response(prompt)
#     content_text = response["content"]
#     return ChatResponse(response=content_text)\

@router.post("/user_request", response_model=UserResponse)
def user_request(
    request: UserRequest,
) -> UserResponse:
    response = request.request
    return UserResponse(response=response)

import logging


@router.post("/editUsersPrompt")
def editUserPrompt(
        request: ChatRequest,
        svc: Service = Depends(get_service),
):
    try:
        prompt = request.prompt
        response = svc.chat_service.editUserPrompt(prompt)
        content_text = response["content"]
        response_data = json.loads(content_text)

        logging.info(f"User Request Response: {response_data}")

        # Initialize lists to store places and waypoints
        places = []
        waypoints = []

        # Loop through the extracted place information
        for place_info in response_data:
            query = place_info.get("name", "")
            place_type = place_info.get("type", "")

            # Search for places based on the extracted information
            search_request_data = PlaceSearchRequest(
                query=query,
                place_type=place_type
            )
            search_result = search_places(request_data=search_request_data)

            logging.info(f"Search Result: {search_result}")

            # Find the place with the highest rating
            highest_rated_place = None
            highest_rating = 0

            if "results" in search_result and search_result["results"]:
                for result in search_result["results"]:
                    rating = result.get("rating", 0)
                    if rating > highest_rating:
                        highest_rating = rating
                        highest_rated_place = result

            # If we found a place with a rating, add its address to waypoints
            if highest_rated_place:
                address = highest_rated_place.get("formatted_address", "")
                waypoints.append(address)

                # Add the highest-rated place to the places list
                places.append(highest_rated_place)

        # Ensure that origin and destination are provided
        if waypoints:
            origin = waypoints[0]  # Set origin as the first place in the list
            destination = waypoints[-1]  # Set destination as the last place in the list

            waypoints_str = "|".join(waypoints[1:-1])  # Exclude origin and destination from waypoints

            route_request_data = RouteRequest(
                origin=origin,
                destination=destination,
                mode="driving",
                waypoints=waypoints_str
            )

            route_response = get_google_maps_route(
                origin=route_request_data.origin,
                destination=route_request_data.destination,
                mode=route_request_data.mode,
                waypoints=waypoints_str
            )

            logging.info(f"Route Response: {route_response}")

            return {
                "places": places,  # Return the chosen places
                "route": route_response
            }
        else:
            raise HTTPException(status_code=400, detail="No valid places found in the response")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise
