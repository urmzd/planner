def convertTime(time):

    if len(time) == 4:
        hour = int(time[0])
    else:
        hour = int(time[0:2])
        
    minutes = (int(time[-2:]))/60

    return round(hour + minutes, 2)

def isDisjoint(l):

    return len(set(l)) == len(l)

def union(*lists):

    return set().union(*lists)

def intersection(a, b):

    return list(set(a) & set(b))