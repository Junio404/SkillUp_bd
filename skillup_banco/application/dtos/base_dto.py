from pydantic import BaseModel, ConfigDict


class BaseRequestDTO(BaseModel):
    model_config = ConfigDict(use_enum_values=True)


class BaseResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

