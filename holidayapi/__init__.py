import requests
import datetime


OUTPUT_DATE_FORMAT = "%d/%m/%Y"


class UnknownErrorException(BaseException):
    pass


class NoApiKeyException(BaseException):
    pass


class InvalidApiKeyException(BaseException):
    pass


class NoApiPermissionError(BaseException):
    pass


class NoCountryException(BaseException):
    pass


class NoYearException(BaseException):
    pass


class PaidAccountRequiredException(BaseException):
    pass


class NoMonthException(BaseException):
    pass


class NoDayException(BaseException):
    pass


class NoHolidayException(BaseException):
    pass


class MalformedResponseException(BaseException):
    pass


def parse_date(d_string):
    return (datetime
            .datetime
            .strptime(d_string, "%Y-%m-%d")
            .date())


class Holiday:
    def __init__(self, name, date, observed, public):
        self.name = name
        self.date = parse_date(date)
        self.observed = parse_date(observed)
        self.public = bool(public)

    def __str__(self):
        s = "{}: {}".format(self.name, self.date.strftime(OUTPUT_DATE_FORMAT))
        if self.observed != self.date:
            s += " (observed on {})".format(self.observed.strftime(OUTPUT_DATE_FORMAT))
        s += " ("
        s += "not " if not self.public else ""
        s += "public)"
        return s

    def __repr__(self):
        return "<Holiday object ({}) at 0x1022c1be0>".format(self.name)


class Api:
    key = None

    def __init__(self, key):
        self.key = key

    def request(self, **kwargs):
        url = 'https://holidayapi.com/v1/holidays?'
        kwargs  ['key'] = self.key

        r = requests.get(url, params=kwargs)
        json = r.json()

        if r.status_code != 200:
            try:
                error = json["error"]
            except KeyError:
                raise UnknownErrorException

            if error == "The API key parameter is required.":
                raise NoApiKeyException
            if error == "Invalid API key":
                raise InvalidApiKeyException
            if error == "The country parameter is required.":
                raise NoCountryException
            if error == "The year parameter is required.":
                raise NoYearException
            if error.startswith("Free accounts are limited to historical data."):
                raise PaidAccountRequiredException
            if error == "The month parameter is required when requesting upcoming holidays.":
                raise NoMonthException
            if error == "The day parameter is required when requesting upcoming holidays.":
                raise NoDayException

        return json

    def first_upcoming(self, country):
        d = datetime.datetime.now().date()
        r = self.request(country=country, year=d.year, month=d.month, day=d.day, upcoming=True)

        try:
            holidays = r["holidays"]
        except KeyError:
            raise MalformedResponseException

        try:
            holiday = holidays[0]
        except IndexError:
            raise NoHolidayException

        return Holiday(**holiday)
