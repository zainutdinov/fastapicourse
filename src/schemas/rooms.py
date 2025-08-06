from pydantic import BaseModel, Field


class Room(BaseModel):
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int


class RoomAdd(Room):
    hotel_id: int


class RoomPATCH(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
