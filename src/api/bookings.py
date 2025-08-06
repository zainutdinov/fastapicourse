from fastapi import Query, APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(
        db: DBDep
):
    return await db.bookings.get_all()


@router.get("/me")
async def get_bookings(
        user_id: UserIdDep,
        db: DBDep
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest,
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        **booking_data.model_dump(),
        price=room_price,
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}
