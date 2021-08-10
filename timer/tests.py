from timer.models import Task
from django.test import TestCase
from users.models import MyUser
from users.tests import RegisterLoginTest as rl

class TimerTest(TestCase):

    def task_post(self, task_input, time_input, colour_input, task_value, time_value, colour_value, url):
        self.client.get(url)
        response = self.client.post(url, data={task_input : task_value, 
        time_input : time_value, colour_input : colour_value})
        return response
    
    def check_task_and_time(self, actual_task, actual_time, predicted_task, predicted_time):
        self.assertEqual(actual_task, predicted_task)
        self.assertEqual(actual_time, predicted_time)

    def test_timer_template_used(self):
        rl.sign_up_and_login(self)
        response = self.client.get('/timer/1/')
        self.assertTemplateUsed(response, 'timer/base_timer.html')

    def test_task_and_time_input_saved(self):
        rl.sign_up_and_login(self)
        self.client.get('/timer/1/')
        self.task_post('task_input', 'time_input', 'colour_input', 'Starman chords', 15, '#ff0000', '/timer/1/')
        new_item = Task.objects.first()
        self.check_task_and_time(new_item.text, new_item.time, 'Starman chords', 15)
    
    def test_multiple_inputs_saved(self):
        rl.sign_up_and_login(self)
        self.client.get('/timer/1/')
        self.task_post('task_input', 'time_input', 'colour_input', 'Starman chords', 15, '#ff0000', '/timer/1/')
        new_item = Task.objects.get(text = 'Starman chords')
        self.check_task_and_time(new_item.text, new_item.time, 'Starman chords', 15)
        self.task_post('task_input', 'time_input', 'colour_input', 'G Major Scale', 10, '#00ff00', '/timer/1/')
        new_item = Task.objects.get(text = 'G Major Scale')
        self.check_task_and_time(new_item.text, new_item.time, 'G Major Scale', 10)
    
    def test_colour_input_saved(self):
        self.test_task_and_time_input_saved()
        new_item = Task.objects.first()
        self.assertEqual(new_item.colour, '#ff0000')
    
    def test_task_deletion(self):
        self.test_multiple_inputs_saved()
        the_user = MyUser.objects.get(pk=1)
        tasks = Task.objects.filter(user=the_user)
        self.assertEqual(tasks.count(), 2)
        self.client.post('/timer/1/task_delete/2/')
        self.assertEqual(tasks.count(), 1)
    



    


         




