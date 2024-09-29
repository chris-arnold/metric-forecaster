from datetime import datetime, UTC
from sqlmodel import Field, SQLModel
from typing import Optional
from pydantic import model_validator, ConfigDict
from pydantic.json_schema import SkipJsonSchema


def nowutc():
    return datetime.now(UTC)


class CreatedUpdatedAt(SQLModel):
    created_at: datetime = Field(default_factory=nowutc)
    updated_at: datetime = Field(default_factory=nowutc)

    model_config = ConfigDict(
        validate_assignment=True,
    )

    @classmethod
    @model_validator(mode="after")
    def update_updated_at(cls, obj: "CreatedUpdatedAt") -> "CreatedUpdatedAt":
        """Update updated_at field."""
        # must disable validation to avoid infinite loop
        obj.model_config["validate_assignment"] = False

        # update updated_at field
        obj.updated_at = nowutc()

        # enable validation again
        obj.model_config["validate_assignment"] = True
        return obj


class Watch(CreatedUpdatedAt, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    enabled: bool
    team: str
    backend_type: str
    query: str
    forecast_frequency_minutes: int

