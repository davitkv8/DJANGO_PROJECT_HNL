from datetime import date
import calendar

# list1 = ["wednesday1", "monday2", "sunday3", "tuesday23"]

def find_nearest_lecture_time(list1):
    my_date = date.today()
    index_today = my_date.weekday()

    sorted_list = []; sorted_list2 = []; sorted_list3 = []; sorted_list4 = []; sorted_list5 = []; sorted_list6 = [];\
                                                                                                         sorted_list7 = []
    for c in list1:
        if "monday" in c[0:-1].split(",") or "tuesday" in c[0:-2].split(","):
            sorted_list.append(c)
        elif "tuesday" in c[0:-1].split(",") or "tuesday" in c[0:-2].split(","):
            sorted_list2.append(c)
        elif "wednesday" in c[0:-1].split(",") or "wednesday" in c[0:-2].split(","):
            sorted_list3.append(c)
        elif "thursday" in c[0:-1].split(",") or "thursday" in c[0:-2].split(","):
            sorted_list4.append(c)
        elif "friday" in c[0:-1].split(",") or "friday" in c[0:-2].split(","):
            sorted_list5.append(c)
        elif "saturday" in c[0:-1].split(",") or "saturday" in c[0:-2].split(","):
            sorted_list6.append(c)
        elif "sunday" in c[0:-1].split(",") or "sunday" in c[0:-2].split(","):
            sorted_list.append(c)

    full_sorted = sorted(sorted_list) + sorted(sorted_list2) + sorted(sorted_list3) + sorted(sorted_list4) +\
                  sorted(sorted_list5) + sorted(sorted_list6) + sorted(sorted_list7)

    nearest_day = ""
    started_index = index_today
    first_day = 0
    while index_today < started_index+7:

        for c in full_sorted:
            day = (calendar.day_name[index_today]).lower()
            if day in c[0:-1].split(",") or day in c[0:-2].split(","):
                nearest_day = c
                if nearest_day:
                    break
        if nearest_day:
            break
        index_today += 1
        if index_today == 6:
            while first_day <= 6 - (6 - started_index):
                for c in full_sorted:
                    day = (calendar.day_name[first_day]).lower()
                    if day in c[0:-1].split(",") or day in c[0:-2].split(","):
                        nearest_day = c
                        if nearest_day:
                            break
                if nearest_day:
                    break
                first_day += 1

    return date_converter(nearest_day)


def date_converter(weekday):
    try:
        k = int(weekday[-2:])
        print(k)
    except ValueError:
        k = int(weekday[-1:])
        print(k)
    finally:
        if str(k).__len__() < 2:
            remake = weekday[0].upper() + weekday[1:-str(k).__len__()] + " - 0" + str(k) + ":00"
        return remake

