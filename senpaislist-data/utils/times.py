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
    