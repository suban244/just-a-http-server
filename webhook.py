from fastapi.routing import APIRouter
from pydantic import BaseModel
import pystache
import httpx


from typing_extensions import Literal


from enum import Enum
from typing import Literal

from pydantic import BaseModel
httpx_client = httpx.AsyncClient()


class ResourceType(str, Enum):
    question_answer = "question_answer"
    snippet = "snippet"
    document = "document"
    webpage = "webpage"

class HttpAction(BaseModel):
    type: Literal["http_action"]
    callback_event: str
    description: str | None = None

    required_slots: list[str]
    result_slots: str

    url: str
    method: str
    body: dict | str | None = None
    headers: list[dict]
    params: list[dict]

Action = HttpAction

class ResourceEventWebhookData(BaseModel):
    id: str
    type: ResourceType
    project_id: str
    index_status: bool


class ActionWebhookData(BaseModel):
    flow_id: str
    action_name: str
    action: Action
    params: dict


WebhookData = ResourceEventWebhookData | ActionWebhookData


class WebhookEvent(BaseModel):
    eventType: str
    data: WebhookData

class WebhookResponse(BaseModel):
    status: Literal["OK", "ERROR"]
    message: str | None = None
    data: dict | None = None
    slots: dict | None = None

router = APIRouter()

async def do_http_call(action: HttpAction, params: dict) -> WebhookResponse:
    # Do http call here
    url = pystache.render(action.url, params)

    body_type = type(action.body) # [dict, str, None]
    body = pystache.render(action.body, params) if action.body else None

    headers: dict[str, str] = action.headers # type: ignore

    match action.method:
        case "GET":
            response = await httpx_client.get(url, headers=headers)
            response.raise_for_status()
            
            return WebhookResponse(status="OK", data=response.json())

        case "POST":
            match action.body:
                case None:
                    response = await httpx_client.post(url, headers=headers)
                case str():
                    response = await httpx_client.post(url, headers=headers, content=body)
                case dict():
                    response = await httpx_client.post(url, headers=headers, json=body)
            response.raise_for_status()
            return WebhookResponse(status="OK", data=response.json())

        case _:
            pass
    return WebhookResponse(status="ERROR")

@router.post(path="/")
async def webhooks(event: WebhookEvent) -> WebhookResponse:
    match event:
        case ActionWebhookData():
            match event.action:
                case HttpAction():
                    return do_http_call(action=event.action, params=event.params)
    
    return WebhookResponse(status="ERROR")
    
