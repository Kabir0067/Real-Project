from rest_framework import serializers
from .models import CustomerUser, ComeAndWent, Feedback

class ComeAndWentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComeAndWent
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        

class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = '__all__' 


class CustomerStudentSerializer(serializers.ModelSerializer):
    come_and_went_records = ComeAndWentSerializer(many=True, read_only=True)
    feedbacks = FeedbackSerializer(many=True, read_only=True)
    class Meta:
        model = CustomerUser
        fields = ['user_id', 'first_name', 'last_name', 'username', 'group_name', 'address',
                  'phone_number', 'email', 'date_of_birth', 'is_active', 'registration_date',
                  'come_and_went_records', 'feedbacks']

