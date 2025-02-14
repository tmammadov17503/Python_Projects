def is_leap(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return "Leap Year"
            else:
                return "Not Leap Year"
        else:
            return "Leap Year"
    else:
        return "Not Leap Year"

def days_in_month(year, month):
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    print(is_leap(year))
    if is_leap(year) and month == 2:
        return 29
    else:
        final_month = str(month_days[month - 1])
    return str("There are " + final_month + " days in this month")

year = int(input("Please enter a year:\n"))
month = int(input("Please enter a month:\n"))
days = days_in_month(year, month)
print(days)

