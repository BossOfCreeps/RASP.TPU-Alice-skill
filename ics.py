from datetime import datetime, timedelta, time, date

from icalendar import Calendar, Event

dict_times = {
    0: time(hour=1, minute=30),
    1: time(hour=3, minute=25),
    2: time(hour=5, minute=40),
    3: time(hour=7, minute=35),
    4: time(hour=9, minute=30),
    5: time(hour=11, minute=25),
    6: time(hour=13, minute=20),
}


def get_lesson(file, date_, lesson_time) -> list:
    time_ = dict_times[lesson_time] if lesson_time is not None else None
    out = list()

    with open(file, 'rb') as g:
        cal = Calendar.from_ical(g.read())
        for item in cal.walk():
            if isinstance(item, Event):
                if date_ is None and item['DTSTART'].dt.time() == time_:
                    new_date = item['DTSTART'].dt.date().weekday()+1
                    out.append(f"{new_date} день недели\n{item['DESCRIPTION']}\n\n")

                elif item['DTSTART'].dt.date() == date_ and time_ is None:
                    new_time = (datetime.combine(date.today(), item['DTSTART'].dt.time()) + timedelta(hours=7)).time()
                    out.append(f"{new_time} пара\n{item['DESCRIPTION']}\n\n")

                elif item['DTSTART'].dt.date() == date_ and item['DTSTART'].dt.time() == time_:
                    out.append(f"{item['DESCRIPTION']}\n")
    return out
