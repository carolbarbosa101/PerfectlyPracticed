from calendar import HTMLCalendar

class CustomCal(HTMLCalendar):
    cssclass_month_head = "text-center month-head"
    cssclass_month = "text-center month"
    cssclass_year = "text-italic lead"
