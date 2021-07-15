import datetime 

now = datetime.datetime.now()

def get_current_year():
    return now.year

def get_current_season():
    month = now.month
    if month in ('January', 'February', 'March'):
	    return 'winter'
    elif month in ('April', 'May', 'June'):
        return 'spring'
    elif month in ('July', 'August', 'September'):
        return 'summer'
    else:
        return 'fall'
 