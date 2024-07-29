from django.db import models


class CustomerUser(models.Model):
    user_id = models.CharField(max_length=150, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    group_name = models.CharField(max_length=50)
    address = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    registration_date = models.DateTimeField(blank=True, null=True)
   
    def __str__(self):
        return self.user_id
   
   
class ComeAndWent(models.Model):
    user = models.ForeignKey(CustomerUser, related_name='come_and_went_records', on_delete=models.CASCADE)
    time_to_come = models.DateTimeField(blank=True, null=True)
    time_to_go = models.DateTimeField(blank=True, null=True)
    absent_reason = models.TextField(blank=True, null=True)
    late_reason = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user_id
    

class Feedback(models.Model):
    feedback_text = models.TextField(blank=True, null=True)
    submission_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user = models.ForeignKey(CustomerUser, related_name='feedbacks', on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id



