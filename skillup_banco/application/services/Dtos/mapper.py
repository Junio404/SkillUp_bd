from __future__ import annotations

import inspect
from dataclasses import is_dataclass
from enum import Enum
from typing import Any, Iterable, TypeVar

from application.services.Dtos.base_dto import BaseRequestDTO, BaseResponseDTO

TResponse = TypeVar("TResponse", bound=BaseResponseDTO)


def _serialize_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    return value


def _entity_as_data(entity: Any) -> dict[str, Any]:
    if is_dataclass(entity):
        raw = vars(entity)
    else:
        raw = entity.__dict__

    data: dict[str, Any] = {}
    for key, value in raw.items():
        clean_key = key[1:] if key.startswith("_") else key
        data[clean_key] = _serialize_value(value)

    if "id" not in data and hasattr(entity, "id"):
        data["id"] = _serialize_value(getattr(entity, "id"))

    return data


def entity_to_response(entity: Any, response_cls: type[TResponse]) -> TResponse:
    data = _entity_as_data(entity)
    allowed_fields = set(response_cls.model_fields.keys())
    filtered = {key: value for key,
                value in data.items() if key in allowed_fields}
    return response_cls.model_validate(filtered)


def to_response_list(entities: Iterable[Any], response_cls: type[TResponse]) -> list[TResponse]:
    return [entity_to_response(entity, response_cls) for entity in entities]


def build_entity(entity_cls: type[Any], request: BaseRequestDTO) -> Any:
    payload = request.model_dump(exclude_none=True)
    signature = inspect.signature(entity_cls)
    kwargs: dict[str, Any] = {}

    for name, param in signature.parameters.items():
        if name == "self":
            continue

        normalized = name[1:] if name.startswith("_") else name

        if name in payload:
            kwargs[name] = payload[name]
        elif normalized in payload:
            kwargs[name] = payload[normalized]
        elif param.default is inspect._empty:
            raise ValueError(f"Campo obrigatorio ausente: {normalized}")

    return entity_cls(**kwargs)


def apply_update(entity: Any, request: BaseRequestDTO) -> Any:
    for key, value in request.model_dump(exclude_unset=True).items():
        if key == "id":
            continue

        internal_name = key if key.startswith("_") else f"_{key}"

        prop = getattr(type(entity), key, None)
        if isinstance(prop, property) and prop.fset is not None:
            setattr(entity, key, value)
            continue

        if hasattr(entity, internal_name):
            setattr(entity, internal_name, value)
            continue

        if hasattr(entity, key):
            setattr(entity, key, value)

    return entity

