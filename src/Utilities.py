def convertToDecimal(time):

    if len(time) == 4:
        hour = int(time[0])
    else:
        hour = int(time[0:2])
        
    minutes = (int(time[-2:]))/60

    return round(hour + minutes, 2)