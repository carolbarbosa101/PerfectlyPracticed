from django.conf.urls import url
from django.http import response
from django.test import TestCase
from users.models import MyUser
from users.models import LoginDate
from users.tests import RegisterLoginTest as utest
from dashboard.views import dashboard
from dashboard.models import Goal
import datetime

class DashboardTest(TestCase):

    def just_sign_up(self):
        self.client.post('/sign_up', data={'email': 
        'user2@test.com', 'first_name':'User', 'last_name':'Test',
        'password1':'PassTest123', 'password2':'PassTest123'})
        url = '/dashboard/1/'
        return url

    def sign_up_and_login(self):
        self.client.post('/sign_up', data={'email': 
        'user2@test.com', 'first_name':'User', 'last_name':'Test',
        'password1':'PassTest123', 'password2':'PassTest123'})
        success_reponse = self.client.post('/', data={'username': 
        'user2@test.com','password':'PassTest123'})
        dashboard_response = self.client.get(success_reponse.url)
        url = f'/{dashboard_response.url}'
        return url
    
    def goal_post(self, goal_input, date_input, goal_value, date_value, url):
        response = self.client.get(url)
        response = self.client.post(url, data={goal_input : goal_value, 
        date_input : date_value})
        return response
    
    def test_login_required_to_access_dashboard(self):
        url = self.just_sign_up()
        redirect_response = self.client.get(url)
        login_url = redirect_response.url
        login_response = self.client.get(login_url)
        self.assertTemplateUsed(login_response, 'users/login.html')

    def test_successful_login_uses_dashboard_template(self):
        url = self.sign_up_and_login()
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'dashboard/base_dashboard.html')
    
    def test_goal_saved_after_post(self):
        url = self.sign_up_and_login()
        self.goal_post('goal_input', 'date_input', 'Learn the song Starman', 
        '2021-08-01', url)
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
        url = self.sign_up_and_login()
        self.goal_post('goal_input', 'date_input', 'Master G Major Scale 1st Position', 
        '2021-09-15', url)
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
        url = self.sign_up_and_login()
        self.goal_post('goal_input', 'date_input', 'Learn the F barre chord', 
        '', url)
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
        url = self.sign_up_and_login()
        self.goal_post('goal_input', 'date_input', '', 
        '', url)
        self.assertEqual(Goal.objects.count(), 0)
    
    def test_background_color_of_today_changed(self):
        pass

    def test_login_day_of_user_stored(self):
        # sign up and login
        url = self.sign_up_and_login()
        self.client.get(url)
        # get pk of user logged in
        pk = 0
        for s in url.split('/'):
            if s.isdigit():
                pk = s
        # get login dates of the user and check there is only one added 
        # for the one login that has occured
        the_user = MyUser.objects.get(pk=pk)
        last_login_date = datetime.datetime.date(the_user.last_login)
        self.assertEqual(LoginDate.objects.filter(user = the_user).count(), 1)

    def test_login_again_on_same_day_still_one_date_present(self):
        self.test_login_day_of_user_stored
        self.test_login_day_of_user_stored
    

    def test_multiple_consecutive_login_days_of_user_stored(self):
        # 1st login - today
        url = self.sign_up_and_login()
        self.client.get(url)
        pk = 0
        for s in url.split('/'):
            if s.isdigit():
                pk = s
        the_user = MyUser.objects.get(pk=pk)
        today = datetime.datetime.date(the_user.last_login)
        self.assertEqual(LoginDate.objects.filter(user = the_user).count(), 1)
        self.assertTrue(LoginDate.objects.get(login_date = today))

        # 2nd login - yesterday (artificially adding to pretend user logged in yesterday too)
        yesterday = today - datetime.timedelta(days=1)
        LoginDate.objects.create(user=the_user, login_date=yesterday)
        self.assertEqual(LoginDate.objects.filter(user = the_user).count(), 2)
        self.assertTrue(LoginDate.objects.get(login_date = yesterday))


        # 3rd day login - day before yesterday
        day_before_yesterday= today - datetime.timedelta(days=2)
        LoginDate.objects.create(user=the_user, login_date=day_before_yesterday)
        self.assertEqual(LoginDate.objects.filter(user = the_user).count(), 3)
        self.assertTrue(LoginDate.objects.get(login_date = day_before_yesterday))
