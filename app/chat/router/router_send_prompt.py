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

# from langchain.document_loaders import TextLoader
# from langchain.indexes import VectorstoreIndexCreator

# logging.basicConfig(level=logging.DEBUG)

# loader = TextLoader('FairytaleInstructions.txt')
# index = VectorstoreIndexCreator().from_loaders([loader])


class UserRequest(AppModel):
    request: str
    # userID: str
class UserResponse(AppModel):
    response: str

class ChatRequest(AppModel):
    prompt: str
    userID: str

class ChatResponse(AppModel):
    response: str

class FairytaleRequest(AppModel):
    childAge: str
    childGenger: str
    storyLength: str
    mainCharacter: str
    description: str
    moralOfStory: str

class FairytaleResponse(BaseModel):
    titleOfTheFairyTale: str
    readingTime: str
    contentOfTheFairyTale: str

class ChildVocabRequest(AppModel):
    childAge: str
    childGenger: str
    term: str

class GameDevRequest(AppModel):
    childAge: str
    childGenger: str
    hobbi: str
    gameFormat: str
    result: str
    place: str

class GameDevResponse(BaseModel):
    titleOfGame: str
    timeSpending: str
    ageLimit: str
    memberCount: str
    benefitsForChild: str
    description: str
    instructions: str

@router.post("/chat", response_model=ChatResponse)
def chat_with_ai(
    request: ChatRequest,
    svc: Service = Depends(get_service),
) -> ChatResponse:
    prompt = request.prompt
    response = svc.chat_service.get_response(prompt)
    content_text = response["content"]
    return ChatResponse(response=content_text)\

@router.post("/user_request", response_model=UserResponse)
def user_request(
    request: UserRequest,
) -> UserResponse:
    response = request.request
    return UserResponse(response=response)


@router.post("/createGame", response_model=GameDevResponse)
def chat_to_createGame(
    request: GameDevRequest,
    svc: Service = Depends(get_service),
) -> GameDevResponse:
    # prompt = request.prompt
    prompt = f"Я- родитель, и хочу придумать игры для моего ребенка: {request.childAge}, {request.childGenger}" \
             f"Ребенок увлекается {request.hobbi}" \
             f"Я ищу {request.gameFormat} игру, которая увлечет моего ребенка и поможет ему усвоить навыки {request.result}." \
             f"Игра будет проходить {request.place}." \
             f"response in JSON format"  \

    systemPromt = '''
    {
    "titleOfGame": "string",
    "timeSpending": "string",
    "ageLimit": "string",
    "memberCount": "int",
    "benefitsForChild": "string",
    "description": "string",
    "instructions": "string",
    }
    '''
    response = svc.chat_service.get_game(prompt, systemPromt)
    content_text = response["content"] 

    # content_text = "{\n    \"titleOfTheFairyTale\": \"Человек-паук и его мечта\",\n    \"readingTime\": \"20 минут\",\n    \"contentOfTheFairyTale\": \"\\n\\nЖил-был в маленьком городке юный мальчик по имени Питер\"\n}"
    data_dict = json.loads(content_text)
    game = GameDevResponse(**data_dict)
    return game
    # return ChatResponse(response=content_text)


@router.post("/createFairtale", response_model=ChatResponse)
def chat_to_createFairytale(
    request: ChatRequest,
    svc: Service = Depends(get_service),
) -> ChatResponse:
    prompt = request.prompt
    if "/fairytale" in prompt.lower():
        newPromt = ("Cоздай cказку для моего ребенка")
        systemPromt = ("Учитывай возраст ребенка при генерации сказек. Это очень важно."
                       "При разработке сказки учитывайте следующие аспекты, предоставленные родителем:"
                       "- Возраст и стадия развития ребенка"
                       "- Интересы и увлечения ребенка"
                       "Имя любимого персонажа"
                       "Любимый мультфильм или фильм"
                       "Желаемая тема сказки"
                       "Желаемый урок или смысл, который вы хотели бы, чтобы сказка несла"
                       "Используя эту информацию, предложите концепцию сказки, соответствующую требованиям родителя и приятную для ребенка. Не стесняйтесь запрашивать дополнительные детали или спецификации при необходимости.")

        response = svc.chat_service.get_fairytale(newPromt, systemPromt)
        content_text = response["content"]
    else:
        systemPromt = ("")
        response = svc.chat_service.get_fairytale(prompt, systemPromt)
        content_text = response["content"] 
    return ChatResponse(response=content_text)

@router.post("/createFairtale2", response_model=FairytaleResponse)
def chat_to_createFairytale2(
    request: FairytaleRequest,
    svc: Service = Depends(get_service),
) -> FairytaleResponse:
    prompt = f"Пожалуйста, создайте сказку для ребенка {request.childAge} лет, {request.childGenger}. " \
             f"Сказка должна быть продолжительностью {request.storyLength}. " \
             f"Главным героем должен быть {request.description} по имени {request.mainCharacter}. " \
             f"Мораль истории должна заключаться в том, чтобы {request.moralOfStory}."
    systemPromt = '''
    {
    "titleOfTheFairyTale": "string",
    "readingTime": "string",
    "contentOfTheFairyTale": "string"
    }
    '''
    response = svc.chat_service.get_fairytale(prompt, systemPromt)
    content_text = response["content"]
    # content_text = "{\n    \"titleOfTheFairyTale\": \"Человек-паук и его мечта\",\n    \"readingTime\": \"20 минут\",\n    \"contentOfTheFairyTale\": \"\\n\\nЖил-был в маленьком городке юный мальчик по имени Питер\"\n}"
    data_dict = json.loads(content_text)
    fairy_tale = FairytaleResponse(**data_dict)
    # return ChatResponse(response=content_text)

    return fairy_tale

@router.post("/explainTermsToChild", response_model=ChatResponse)
def chat_to_explainTermsToChild(
    request: ChildVocabRequest,
    svc: Service = Depends(get_service),
) -> ChatResponse:
    prompt = prompt = f"Объясни, что такое {request.term}, моему {request.childGenger}, которому {request.childAge} лет/года."
    systemPromt = ("Ты родитель и тебе нужно обьяснить одну тему для ребенка. Учитывай возраст и пол ребенка при объяснении. Это очень важно.")
    response = svc.chat_service.get_explainToChild(prompt, systemPromt)
    content_text = response["content"]
    return ChatResponse(response=content_text)

@router.post("/explainTermsToParent", response_model=ChatResponse)
def chat_to_explainTermsToParent(
    request: ChatRequest,
    svc: Service = Depends(get_service),
) -> ChatResponse:
    prompt = prompt = f"Объясни, что такое означает подростковый сленг {request.prompt}, родителю."
    systemPromt = ("")
    response = svc.chat_service.get_explainToChild(prompt, systemPromt)
    content_text = response["content"]
    return ChatResponse(response=content_text)

