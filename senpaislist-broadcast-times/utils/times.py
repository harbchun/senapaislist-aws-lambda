from datetime import datetime

def month_to_season(month: int) -> str:
    if month >= 1 and month <= 3:
        return 'spring'
    elif month >= 4 and month <= 6:
        return 'summer'
    elif month >= 7 and month <= 9:
        return 'fall'
    else:
        return 'winter'

def get_current_year() -> int:
    now = datetime.now()
    return now.year

def get_current_season() -> str:
    now = datetime.now()
    month = now.month
    return month_to_season(month)

def get_last_season() -> str:
    current_season = get_current_season()
    if current_season == 'spring':
        return 'winter'
    elif current_season == 'summer':
        return 'spring'
    elif current_season == 'fall':
        return 'summer'
    else:
        return 'fall'

def get_last_year() -> int:
    current_year = get_current_year()
    last_season = get_last_season()
    if last_season == 'winter':
        return current_year - 1
    return current_year
