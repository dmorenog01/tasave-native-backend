from datetime import datetime

class Rate():

    def __init__(self, rate: float, rate_date: datetime, acquired_date: datetime, from_currency: str, to_currency: str, unique_name: str) -> None:
        self.rate = rate
        self.rate_date = rate_date
        self.acquired_date = acquired_date
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.unique_name = unique_name
    
    def to_dict(self) -> dict:
        return vars(self)