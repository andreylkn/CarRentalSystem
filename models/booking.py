class Booking:
    def __init__(self, booking_id, car_id, user_id, start_date, end_date, total_cost, status='pending'):
        self._booking_id = booking_id
        self._car_id = car_id
        self._user_id = user_id
        self._start_date = start_date
        self._end_date = end_date
        self._total_cost = total_cost
        self._status = status

    @property
    def booking_id(self):
        return self._booking_id

    @property
    def car_id(self):
        return self._car_id

    @property
    def user_id(self):
        return self._user_id

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def total_cost(self):
        return self._total_cost

    @property
    def status(self):
        return self._status