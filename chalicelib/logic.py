import numpy as np

week_days = ['Monday', 'Tuesday', 'Wednesday',
             'Thursday', 'Friday', 'Saturday', 'Sunday']

WEEK_DAY_MAP = {d: i for i, d in enumerate(week_days)}


def to_sec(time):
    hourmin = time[:-1]
    hour, min = hourmin.split(':')
    ampm = time[-1]
    return (int(hour) + (12 if ampm == 'P' else 0)) * 3600 + int(min) * 60


def mk_happening_now_filter(now_time, now_day):
    def thunk(times):
        for time in times:
            if np.nan in [time['start_day'], time['end_day'], time['start_time'], time['end_time']]:
                continue
            if (WEEK_DAY_MAP[time['start_day']] <= WEEK_DAY_MAP[now_day]
                and WEEK_DAY_MAP[time['end_day']] >= WEEK_DAY_MAP[now_day]
                and to_sec(time['start_time']) <= to_sec(now_time)
                    and to_sec(time['end_time']) > to_sec(now_time)):
                return True
        return False
    return thunk


def happening_now(day, time, places_json):
    filter = mk_happening_now_filter(time, day)
    return {place_id: place
            for place_id, place in list(places_json.items())
            if filter(place['times'])}


def sub_5dollar_meal(deals):
    food = [deal for deal in deals
            if deal['type'] == 'food' and deal['discount_marker'] == '$']
    drink = [deal for deal in deals
             if deal['type'] == 'drink' and deal['discount_marker'] == '$']
    return (len(food) > 0 and len(drink) > 0
            and
            (min([int(deal['discount_amount']) for deal in food])
            + min([int(deal['discount_amount']) for deal in drink])
            <= 5))
