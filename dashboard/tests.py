from users.models import MyUser
from dashboard.views import dashboard
from django.test import TestCase
from dashboard.models import Goal
import datetime

class DashboardTest(TestCase):

    def test_uses_dashboard_template(self):
        response = self.client.get('/dashboard')
        self.assertTemplateUsed(response, 'dashboard/base_dashboard.html')
    
    def goal_post(self, goal_input, date_input, goal_value, date_value, url):
        response = self.client.get(url)
        response = self.client.post(url, data={goal_input : goal_value, 
        date_input : date_value})
        return response
    
    def test_goal_saved_after_post(self):
        self.goal_post('goal_input', 'date_input', 'Learn the song Starman', 
        '2021-08-01', '/dashboard')
        self.assertEqual(Goal.objects.count(), 1)
        new_goal = Goal.objects.first()
        self.assertEqual(new_goal.text, 'Learn the song Starman')
        self.assertEqual(new_goal.due_date, datetime.date(2021, 8, 1))
    
    def test_goal_edited_after_post(self):
        self.test_goal_saved_after_post()
        self.assertEqual(Goal.objects.count(), 1)
        self.goal_post('goal_cell_edit', 'date_cell_edit', 'Learn the song Heroes', 
        '2021-08-31', '/goal_edit/1/')
        edit_goal = Goal.objects.first()
        self.assertEqual(edit_goal.text, 'Learn the song Heroes')
        self.assertEqual(edit_goal.due_date, datetime.date(2021, 8, 31))
    
    def test_second_goal_added(self):
        self.test_goal_saved_after_post()
        self.goal_post('goal_input', 'date_input', 'Master G Major Scale 1st Position', 
        '2021-09-15', '/dashboard')
        self.assertEqual(Goal.objects.count(), 2)
        new_goal = Goal.objects.get(pk=2)
        self.assertEqual(new_goal.text, 'Master G Major Scale 1st Position')
        self.assertEqual(new_goal.due_date, datetime.date(2021, 9, 15))
    
    def test_goal_ticked(self):
        self.test_second_goal_added()
        self.client.post('/goal_tick/1/')
        completed_goal = Goal.objects.get(pk=1)
        self.assertTrue(completed_goal.completed)

    def test_blank_due_date_inserted(self):
        self.goal_post('goal_input', 'date_input', 'Learn the F barre chord', 
        '', '/dashboard')
        new_goal = Goal.objects.first()
        self.assertEqual(new_goal.text, 'Learn the F barre chord')
        self.assertEqual(new_goal.due_date, None)

    def test_blank_due_date_edited(self):
        self.test_blank_due_date_inserted()
        self.goal_post('goal_cell_edit', 'date_cell_edit', 'Learn the F barre chord', 
        '2021-12-31', '/goal_edit/1/')
        edit_goal = Goal.objects.first()
        self.assertEqual(edit_goal.text, 'Learn the F barre chord')
        self.assertEqual(edit_goal.due_date, datetime.date(2021, 12, 31))

    def test_no_blank_goal_inserted(self):
        self.goal_post('goal_input', 'date_input', '', 
        '', '/dashboard')
        self.assertEqual(Goal.objects.count(), 0)
    
    def test_background_color_of_today_changed(self):
        pass

    def test_login_day_stored_in_list(self):
        # last_login field of user checked
        user = MyUser.objects.first()
        login_dates = LoginDate.all()
        # date field extracted from this
        # date field added to list containing days logged in
        # list contains this day
        pass

    def test_multiple_consecutive_login_days_stored_in_list(self):
        # last_login checked and date added to list
        # last_login updated for next day and added to list
        # last_login updated for next day and added to list
        # list contains all 3 days
        pass
    



