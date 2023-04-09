from datetime import datetime
from pydantic import BaseModel, validator


class InputData(BaseModel):
    dt_from: datetime
    dt_upto: datetime
    group_type: str

    @validator('group_type')
    def group_type_check(cls, v):
        if not any([v == 'hour', v == 'day', v == 'month']):
            raise ValueError('Поле "group_type" должно содержать одно из следующих значений: hour, day, month')
        return v
