from calendar import HTMLCalendar, monthrange
from users.models import MyUser
import datetime 


class CustomCal(HTMLCalendar):
    cssclass_month = 'text-center month'

    def colour_calendar(pk, month, year):
        # get user object that this dashboard is specific to
        the_user = MyUser.objects.get(pk=pk)

        cal = CustomCal().formatmonth(year, month)

        # Add border to all days
        num_of_days = monthrange(year, month)[1]
        for day in range(num_of_days + 1):
            cal = cal.replace('>%i<'%day, 'style="border:solid; border-color:#383b40;">%i<'%day)

        # if in current month give a different colour to today's date and make it bold
        today = datetime.date.today()
        if month == today.month:
            cal = cal.replace('>%i<'%today.day, 'bgcolor="#FFF7C0"><b>%i</b><'%today.day)

        # iterate through all LoginDate objects of the user
        date_objects = the_user.login_dates.all()
        # get the login_date from each
        dates = []
        for date_object in date_objects:
            dates.append(date_object.login_date)
        
        # add to days list if in current month
        days = []
        for date in dates:
            if date.month == month:
                days.append(date.day)

        # change colour if in days list
        for day in days:
            if day != today.day:
                cal = cal.replace('>%i<'%day, 'bgcolor="#99D3DF";>%i<'%day)
        
        return cal
    
    def calendar_list(pk, ):
         # iterate through all LoginDate objects of the user
        the_user = MyUser.objects.get(pk=pk)
        date_objects = the_user.login_dates.all()

        # get the login_date from each
        dates = []
        for date_object in date_objects:
            dates.append(date_object.login_date)

        # get all month-year combos that appear 
        month_year_strs = []
        for date in dates:
            month_year = f'{date.month}-{date.year}'
            if month_year not in month_year_strs:
                month_year_strs.append(month_year)
        
        cals=[]
        # iterate through month-years and make cals
        for month_year in month_year_strs:
            month_year_list = month_year.split('-')
            month = int(month_year_list[0])
            year = int(month_year_list[1])
            cal = CustomCal.colour_calendar(pk, month, year)
            cals.append(cal)

        return cals
    

        

