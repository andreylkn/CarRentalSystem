class Car:
    def __init__(self, car_id, make, model, year, mileage, available, min_rent_period, max_rent_period):
        self._car_id = car_id
        self._make = make
        self._model = model
        self._year = year
        self._mileage = mileage
        self._available = available
        self._min_rent_period = min_rent_period
        self._max_rent_period = max_rent_period

    def __str__(self):
        return f"{self._car_id}: {self._make} {self._model} ({self._year})"

    @property
    def id(self):
        return self._car_id

    @property
    def make(self):
        return self._make

    @property
    def model(self):
        return self._model

    @property
    def year(self):
        return self._year

    @property
    def mileage(self):
        return self._mileage

    @property
    def available(self):
        return self._available

    @property
    def min_rent_period(self):
        return self._min_rent_period

    @property
    def max_rent_period(self):
        return self._max_rent_period

    def print_full_details(self):
        print(self._get_car_details() + f" | Available: {self.available}")

    def print_short_details(self):
        print(self._get_car_details())

    def _get_car_details(self):
        return f"ID: {self.id} | {self.make} {self.model} ({self.year}) | Mileage: {self.mileage} | Min rent period: {self.min_rent_period}; Max rent period: {self.max_rent_period}"