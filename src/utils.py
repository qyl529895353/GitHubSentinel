from datetime import datetime, timedelta


def time_range(**kwargs):
    print(kwargs)
    time_start = kwargs.get("time_start")
    time_end = kwargs.get("time_end")
    gitlab_time = kwargs["gitlab_time"]
    gitlab_time_str_no_tz = gitlab_time.split('+')[0]
    gitlab_datetime = datetime.strptime(gitlab_time_str_no_tz, '%Y-%m-%dT%H:%M:%S')
    print(time_start, time_end)
    if not time_start and not time_end:
        return True
    if time_start:
        time_start = datetime.strptime(time_start, '%Y-%m-%dT%H:%M:%S') + timedelta(1)
    else:
        time_start = -1
    if time_end:
        time_end = datetime.strptime(time_end, '%Y-%m-%dT%H:%M:%S') + timedelta(-1)
    else:
        time_end = datetime.now() + timedelta(days=1000)

    if time_start <= gitlab_datetime <= time_end:
        return True
    return False


def match_record(result, time_start, time_end):
    match_list = []
    for res in result:
        try:
            code = time_range(time_start=time_start, time_end=time_end, gitlab_time=res["created_at"])
        except Exception as e:
            code = False
            print(e)
        if not code:
            continue
        match_list.append(res)
    return match_list


