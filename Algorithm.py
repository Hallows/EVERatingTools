def seconds_to_hms(total_seconds):
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)