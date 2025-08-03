import datetime
import pytz

def calculate_time_difference(input_date, input_time):
    print(input_time)
    input_datetime = datetime.datetime.strptime(f"{input_date} {input_time}", "%Y-%m-%d %H:%M")
    print(input_datetime)
    cst_timezone = pytz.timezone('America/Chicago')
    print(cst_timezone)
    input_datetime = cst_timezone.localize(input_datetime)
    print(input_datetime)
    current_time = datetime.datetime.now(tz=cst_timezone)
    print(current_time)
    time_difference = round((input_datetime - current_time).total_seconds())
    print(time_difference)
    if time_difference < 0:
        return -1
    return time_difference