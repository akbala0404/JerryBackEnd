from fastapi import APIRouter, Depends, status
from app.utils import AppModel, BaseModel
from pydantic import Field
from typing import Any
from ..service import Service, get_service
from . import router
import json
import logging
import string
import ast


class ChatRequest(AppModel):
    prompt: str

class ChatResponse(AppModel):
    response: str


@router.post("/chat", response_model=ChatResponse)
def chat_with_ai(
    request: ChatRequest,
    svc: Service = Depends(get_service),
) -> ChatResponse:
    prompt = request.prompt
    response = svc.chat_service.get_response(prompt)
    content_text = response["content"]
    return ChatResponse(response=content_text)

@router.post("/editUsersPrompt", response_model=ChatResponse)
def editUserPrompt(
    request: ChatRequest,
    svc: Service = Depends(get_service),
) -> ChatResponse:
    prompt = request.prompt
    response = svc.chat_service.editUserPrompt(prompt)
    content_text = response["content"]
    return ChatResponse(response=content_text)

