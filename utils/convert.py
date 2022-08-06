from cmath import inf


def convert_str_to_seconds(duration):
    if duration == '1m':
        return 60
    elif duration == '2m':
        return 120
    elif duration == '5m':
        return 300
    elif duration == '15m':
        return 900
    elif duration == '30m':
        return 1800
    elif duration == '60m':
        return 3600
    elif duration == '90m':
        return 5400
    elif duration == '1h':
        return 3600
    elif duration == '1d':
        return 86400
    elif duration == '5d':
        return 432000
    elif duration == '1wk':
        return 604800

def convert_seconds_to_str(duration):
    if duration == 60:
        return '1m'
    elif duration == 120:
        return '2m'
    elif duration == 300:
        return '5m'
    elif duration == 900:
        return '15m'
    elif duration == 3600:
        return '60m'
    elif duration == 5400:
        return '90m'
    elif duration == 86400:
        return '1d'
    elif duration == 432000:
        return '5d'
    elif duration == 604800:
        return '1wk'
    # elif duration == 604800:
    #     return '1mo'
    # elif duration == 604800:
    #     return '3mo'
    # elif duration == 604800:
    #     return '6mo'
    # elif duration == 604800:
    #     return '1yr'
    # elif duration == 604800:
    #     return '2yr'
    # elif duration == 604800:
    #     return '5yr'
    # elif duration == 604800:
    #     return '10yr'
    # elif duration == inf:
    #     return 'max'
    else:


    