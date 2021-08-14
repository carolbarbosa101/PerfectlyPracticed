from django.conf.urls import url
from django.http import response
from django.test import TestCase
from users.models import MyUser
from users.models import LoginDate
from users.tests import RegisterLoginTest as utest
from dashboard.views import dashboard
from dashboard.models import Goal
import datetime

class GoalsTest(TestCase):

    def sign_up_and_login_url(self):
        self.client.post('/sign_up', data={'email': 
        'user2@test.com', 'first_name':'User', 'last_name':'Test',
        'password1':'PassTest123', 'password2':'PassTest123'})
        success_reponse = self.client.post('/', data={'username': 
        'user2@test.com','password':'PassTest123'})
        dashboard_response = self.client.get(success_reponse.url)
        url = f'/{dashboard_response.url}'
        return url
    
    def goal_post(self, goal_input, date_input, goal_value, date_value, url):
        self.client.get(url)
        response = self.client.post(url, data={goal_input : goal_value, 
        date_input : date_value})
        return response
    
    def check_goal_and_date(self, actual_goal, actual_date, predicted_goal, predicted_date):
        self.assertEqual(actual_goal, predicted_goal)
        self.assertEqual(actual_date, predicted_date)
    
    def get_user_pk_from_url(self, url):
        self.client.get(url)
        # get pk of user logged in
        pk = 0
        for s in url.split('/'):
            if s.isdigit():
                pk = s
        
        return pk
    
    def test_login_required_to_access_dashboard(self):
        # just sign up, don't login
        self.client.post('/sign_up', data={'email': 
        'user2@test.com', 'first_name':'User', 'last_name':'Test',
        'password1':'PassTest123', 'password2':'PassTest123'})
        # after trying to access without login, we are redirected to the login page
        redirect_response = self.client.get('/dashboard/1/')
        login_url = redirect_response.url
        login_response = self.client.get(login_url)
        self.assertTemplateUsed(login_response, 'users/login.html')

    def test_successful_login_uses_dashboard_template(self):
        url = self.sign_up_and_login_url()
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'dashboard/base_dashboard.html')
    
    def test_goal_saved_after_post(self):
        url = self.sign_up_and_login_url()
        self.goal_post('goal_input', 'date_input', 'Learn the song Starman', 
        '2021-08-01', url)
        self.assertEqual(Goal.objects.count(), 1)
        new_goal = Goal.objects.first()
        self.check_goal_and_date(new_goal.text, new_goal.due_date, 'Learn the song Starman', datetime.date(2021, 8, 1))

    def test_goal_edited_after_post(self):
        self.test_goal_saved_after_post()
        self.assertEqual(Goal.objects.count(), 1)
        self.goal_post('goal_cell_edit', 'date_cell_edit', 'Learn the song Heroes', 
        '2021-08-31', '/dashboard/1/goal_edit/1/')
        edit_goal = Goal.objects.first()
        self.check_goal_and_date(edit_goal.text, edit_goal.due_date, 'Learn the song Heroes', datetime.date(2021, 8, 31))
    
    def test_second_goal_added(self):
        self.test_goal_saved_after_post()
        url = self.sign_up_and_login_url()
        self.goal_post('goal_input', 'date_input', 'Master G Major Scale 1st Position', 
        '2021-09-15', url)
        self.assertEqual(Goal.objects.count(), 2)
        new_goal = Goal.objects.get(pk=2)
        self.check_goal_and_date(new_goal.text, new_goal.due_date, 'Master G Major Scale 1st Position', datetime.date(2021, 9, 15))
    
    def test_goal_ticked(self):
        self.test_second_goal_added()
        self.client.post('/dashboard/1/goal_tick/1/')
        completed_goal = Goal.objects.get(pk=1)
        self.assertTrue(completed_goal.completed)

    def test_blank_due_date_inserted(self):
        url = self.sign_up_and_login_url()
        self.goal_post('goal_input', 'date_input', 'Learn the F barre chord', 
        '', url)
        new_goal = Goal.objects.first()
        self.check_goal_and_date(new_goal.text, new_goal.due_date, 'Learn the F barre chord', None)

    def test_blank_due_date_edited(self):
        self.test_blank_due_date_inserted()
        self.goal_post('goal_cell_edit', 'date_cell_edit', 'Learn the F barre chord', 
        '2021-12-31', '/dashboard/1/goal_edit/1/')
        edit_goal = Goal.objects.first()
        self.check_goal_and_date(edit_goal.text, edit_goal.due_date, 'Learn the F barre chord', datetime.date(2021, 12, 31))

    def test_no_blank_goal_inserted(self):
        url = self.sign_up_and_login_url()
        self.goal_post('goal_input', 'date_input', '', 
        '', url)
        self.assertEqual(Goal.objects.count(), 0)
    
    def test_goals_unique_to_each_user(self):
        # user2@test.com signed up and logged in 
        url1 = self.sign_up_and_login_url()
        self.client.get(url1)

        # different user, testing@user.com signed up and logged in
        self.client.post('/sign_up', data={'email': 
        'testing@user.com', 'first_name':'Testing', 'last_name':'User',
        'password1':'PassTest123', 'password2':'PassTest123'})
        success_reponse = self.client.post('/', data={'username': 
        'testing@user.com','password':'PassTest123'})
        dashboard_response = self.client.get(success_reponse.url)
        url2 = f'/{dashboard_response.url}'

        # post different goals for each user and test if both are present/absent from both users
        self.goal_post('goal_input', 'date_input', 'Learn the song Starman', 
        '2021-08-01', url1)
        self.goal_post('goal_input', 'date_input', 'Learn the song Life on Mars', 
        '2021-08-01', url2)

        pk1 = self.get_user_pk_from_url(url1)
        user1 = MyUser.objects.get(pk=pk1)
        goal1 = Goal.objects.get(user = user1)
        self.assertEqual(goal1.text, 'Learn the song Starman')

        pk2 = self.get_user_pk_from_url(url2)
        user2 = MyUser.objects.get(pk=pk2)
        goal2 = Goal.objects.get(user = user2)
        self.assertEqual(goal2.text, 'Learn the song Life on Mars')
    

   
    
class CalendarTest(TestCase):

    def test_login_day_of_user_stored(self):
        # sign up and login
        url = GoalsTest.sign_up_and_login_url(self)
        self.client.get(url)
        # get pk of user logged in
        pk = GoalsTest.get_user_pk_from_url(self, url)
        # get login dates of the user and check there is only one added 
        # for the one login that has occured
        the_user = MyUser.objects.get(pk=pk)
        today = datetime.datetime.date(the_user.last_login)
        self.assertEqual(LoginDate.objects.filter(user = the_user).count(), 1)
        self.assertTrue(LoginDate.objects.get(login_date = today))


    def test_login_again_on_same_day_still_one_date_present(self):
        self.test_login_day_of_user_stored()

        success_reponse = self.client.post('/', data={'username': 
        'user2@test.com','password':'PassTest123'})
        dashboard_response = self.client.get(success_reponse.url)
        url = f'/{dashboard_response.url}'
        self.client.get(url)
        pk = GoalsTest.get_user_pk_from_url(self, url)
        the_user = MyUser.objects.get(pk=pk)

        self.assertEqual(LoginDate.objects.filter(user = the_user).count(), 1)
    

    def test_multiple_consecutive_login_days_of_user_stored(self):
        # 1st login - today
        url = GoalsTest.sign_up_and_login_url(self)
        self.client.get(url)
        pk = GoalsTest.get_user_pk_from_url(self, url)

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

    
    def test_cal_unique_to_each_user(self):
        # Have different users sign in on different days and see different login dates stored
        today = datetime.datetime.today()
                
        # user2@test.com 
        url1 = GoalsTest.sign_up_and_login_url(self)
        self.client.get(url1)

        pk1 = GoalsTest.get_user_pk_from_url(self, url1)
        user1 = MyUser.objects.get(pk=pk1)
        yesterday = today - datetime.timedelta(days=1)
        LoginDate.objects.create(user=user1, login_date=yesterday)

        # different user, testing@user.com 
        self.client.post('/sign_up', data={'email': 
        'testing@user.com', 'first_name':'Testing', 'last_name':'User',
        'password1':'PassTest123', 'password2':'PassTest123'})
        success_reponse = self.client.post('/', data={'username': 
        'testing@user.com','password':'PassTest123'})
        dashboard_response = self.client.get(success_reponse.url)
        url2 = f'/{dashboard_response.url}'
        self.client.get(url2)

        pk2 = GoalsTest.get_user_pk_from_url(self, url2)
        user2 = MyUser.objects.get(pk=pk2)
        past_date = today - datetime.timedelta(days=5)
        LoginDate.objects.create(user=user2, login_date=past_date)

        # compare what dates for each user
        dates1 = LoginDate.objects.filter(user = user1)
        self.assertIn(LoginDate.objects.get(login_date = yesterday), dates1)
        self.assertNotIn(LoginDate.objects.get(login_date = past_date), dates1)

        dates2 = LoginDate.objects.filter(user = user2)
        self.assertIn(LoginDate.objects.get(login_date = past_date), dates2)
        self.assertNotIn(LoginDate.objects.get(login_date = yesterday), dates2)
