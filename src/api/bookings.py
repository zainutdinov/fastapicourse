from fastapi import Query, APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("/")
async def create_booking(
        db: DBDep,
        user_id: UserIdDep,
        room_id: int,
        date_from: str = Body(),
        date_to: str = Body(),
): 
    room = await db.rooms.get_one_or_none(id=room_id)
    price = room.model_dump().get("price", 0)
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to,
        price=price,
    )
    booking = await db.bookings.add(booking_data)
    await db.commit()

    return {"status": "OK", "data": booking}
