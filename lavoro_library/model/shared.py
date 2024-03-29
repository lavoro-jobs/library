import inspect

from typing import Annotated

from fastapi import Form
from pydantic import BaseModel, model_validator


def as_form(cls):
    new_params = [
        inspect.Parameter(
            field_name,
            inspect.Parameter.POSITIONAL_ONLY,
            default=model_field.default,
            annotation=Annotated[model_field.annotation, model_field.metadata, Form()],
        )
        for field_name, model_field in cls.model_fields.items()
    ]

    cls.__signature__ = cls.__signature__.replace(parameters=new_params)

    return cls


class Point(BaseModel):
    longitude: float
    latitude: float

    @model_validator(mode="before")
    def parse_point_string(cls, data):
        if isinstance(data, str):
            data = data.strip("()")
            longitude, latitude = map(float, data.split(","))
            return {"longitude": longitude, "latitude": latitude}
        return data
