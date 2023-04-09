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
        err = e.errors()
        if len(err) == 1:
            if 'group_type' in err[0]["loc"]:
                return err[0]["msg"]
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
