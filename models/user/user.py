from abc import ABC, abstractmethod

from services.booking_service import BookingService
from services.car_service import CarService

class User(ABC):
    def __init__(self, user_id, username):
        self._user_id = user_id
        self._username = username
        self._car_service = CarService()
        self._booking_service = BookingService()

    @property
    def user_id(self):
        return self._user_id

    @property
    def username(self):
        return self._username

    @abstractmethod
    def view_cars(self):
        pass
