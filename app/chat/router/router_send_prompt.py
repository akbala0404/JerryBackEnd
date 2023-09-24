from fastapi import APIRouter, Depends, status
from app.map.router.router_send_prompt import PlaceSearchRequest
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

@router.post("/editUsersPrompt")
def editUserPrompt(
    request: ChatRequest,
    svc: Service = Depends(get_service),
):
    prompt = request.prompt
    response = svc.chat_service.editUserPrompt(prompt)
    content_text = response["content"]
    response_data = json.loads(content_text)

    logging.info(f"User Request Response: {response_data}")

    query = response_data[0].get("name", "")
    place_type = response_data[0].get("type", "")

    search_request_data = PlaceSearchRequest(
        query=query,
        place_type=place_type
    )
    search_result = search_places(request_data=search_request_data)
    return search_result

# @router.post("/editUsersPromptTest")
# def editUserPrompTest(
#     request: ChatRequest,
#     svc: Service = Depends(get_service),
# ):
#     prompt = request.prompt
#     response = svc.chat_service.editUserPrompt(prompt)
#     content_text = response["content"]
#     response_data = json.loads(content_text)

#     # logging.info(f"User Request Response: {response_data}")

#     # query = response_data[0].get("name", "")
#     # place_type = response_data[0].get("type", "")

#     # search_request_data = PlaceSearchRequest(
#     #     query=query,
#     #     place_type=place_type
#     # )
#     # search_result = search_places(request_data=search_request_data)
#     return response_data

# @router.post("/editUsersPromptTest2")
# def editUserPrompTest2(
#     request: ChatRequest,
#     svc: Service = Depends(get_service),
# ):
#     prompt = request.prompt
#     response = svc.chat_service.editUserPrompt(prompt)
#     content_text = response["content"]
#     response_data = json.loads(content_text)

#     # logging.info(f"User Request Response: {response_data}")

#     # query = response_data[0].get("name", "")
#     # place_type = response_data[0].get("type", "")

#     # search_request_data = PlaceSearchRequest(
#     #     query=query,
#     #     place_type=place_type
#     # )
#     # search_result = search_places(request_data=search_request_data)
#     return response_data