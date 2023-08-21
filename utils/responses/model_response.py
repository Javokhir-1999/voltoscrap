import typing

from pydantic import BaseModel
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse

class ModelResponse(JSONResponse):

    def __init__(
            self,
            dto_model: BaseModel,
            status_code: int = 200,
            headers: typing.Optional[typing.Dict[str, str]] = None,
            media_type: typing.Optional[str] = None,
            background: typing.Optional[BackgroundTask] = None,
    ):
        content = self._to_dict(dto_model)
        super().__init__(content, status_code, headers, media_type, background)

    def _to_dict(self, instance:BaseModel) -> dict[str, typing.Any]:
        return instance.dict()
