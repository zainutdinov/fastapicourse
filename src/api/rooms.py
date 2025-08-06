from fastapi import APIRouter, Body, Path

from repositories.rooms import RoomsRepository
from src.database import async_session_maker
from src.schemas.rooms import Room, RoomAdd, RoomPATCH

router = APIRouter(tags=["Номера"])


@router.get("/hotels/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int = Path(..., ge=1, description="ID отеля, к которому относятся номера")
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id
        )


@router.post("/hotels/{hotel_id}/rooms")
async def create_rooms(
    hotel_id: int = Path(..., ge=1, description="ID отеля, к которому относятся номера"),
    room_data: Room = Body(openapi_examples={
    "1": {
        "summary": "Luxe Room",
        "value": {
            "title": "Luxe",
            "description": "",
            "price": "1000",
            "quantity": "2",
        }
    },
    "2": {
        "summary": "Standart Room",
        "value": {
            "title": "Standart",
            "description": "Обычный номер",
            "price": "500",
            "quantity": "5",
        }
    },
})
):
    async with async_session_maker() as session:
        room_add_data = RoomAdd(**room_data.dict(), hotel_id=hotel_id)
        room = await RoomsRepository(session).add(room_add_data)
        await session.commit()
        return {"status": "OK", "data": room}


@router.put("/hotels/{hotel_id}/rooms/{room_id}")
async def edit_room(
    room_data: Room,
    hotel_id: int = Path(..., ge=1, description="ID отеля, к которому относятся номера"),
    room_id: int = Path(..., ge=1, description="ID номера, который нужно изменить")
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, hotel_id=hotel_id, id=room_id)
        await session.commit()
        return {"status": "OK"}


@router.patch("/hotels/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    room_data: RoomPATCH,
    hotel_id: int = Path(..., ge=1, description="ID отеля, к которому относятся номера"),
    room_id: int = Path(..., ge=1, description="ID номера, который нужно изменить")
):
    async with async_session_maker() as session:
        await (RoomsRepository(session)
               .edit(room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id))
        await session.commit()
        return {"status": "OK"}


@router.delete("/hotels/{hotel_id}/rooms/{room_id}")
async def delete_hotel(
    hotel_id: int = Path(..., ge=1, description="ID отеля, к которому относятся номера"),
    room_id: int = Path(..., ge=1, description="ID номера, который нужно удалить")
):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
        return {"status": "OK"}
