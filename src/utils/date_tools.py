from datetime import datetime, time


def determine_shift_type(dt: datetime) -> str:
    hour_minute = dt.time()

    if time(6, 0) <= hour_minute < time(15, 0):
        return "day"
    else:
        return "night"
