from src.models.bookings import BookingsOrm
from src.models.facilities import RoomsFacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm

__all__ = [
    "BookingsOrm",
    "HotelsOrm",          # <-- перемещён выше
    "RoomsFacilitiesOrm",
    "RoomsOrm",
    "UsersOrm",
]