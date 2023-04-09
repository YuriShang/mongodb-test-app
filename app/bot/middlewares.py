import json
from json.decoder import JSONDecodeError
from pydantic import ValidationError
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from app.models.models import InputData


def _is_valid_json(msg):
    try:
        json_data = json.loads(msg)
        dict(json_data)
        InputData(**json_data)
    except JSONDecodeError:
        return
    except ValidationError as e:
        for err in e.errors():
            if 'group_type' in err["loc"]:
                return "Поле 'group_type' должно содержать одно из следующих значений: " \
                       "hour, day, month"
        return
    except TypeError:
        return
    return json_data["group_type"], json_data["dt_from"], json_data["dt_upto"],


class JsonMessageMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        msg_text = data["event_update"].message.text
        msg_check = _is_valid_json(msg_text)

        if isinstance(msg_check, str):
            data["error"] = msg_check

        if isinstance(msg_check, tuple):
            data["group_type"], data["dt_from"], data["dt_upto"] = msg_check

        return await handler(event, data)
