from __future__ import unicode_literals
from ..LR.models import User
from django.db import models
from datetime import datetime,date

class TravelManager(models.Manager):
    def add_plan(self, userData, user_id):

        errors = []
        if not len(userData['destination']):
            errors.append('Destination is required')

        if not len(userData['start_date']):
            errors.append('You did not select start date!')

        if not len(userData['end_date']):
            errors.append('You did not select end date!')

        if not len(userData['description']):
            errors.append('Tell me about the Travel!')

        if userData['start_date'] and userData['end_date']:
            today = datetime.now().date()
            print today
            start_date_select = datetime.strptime(userData['start_date'],'%Y-%m-%d').date()
            end_date_select = datetime.strptime(userData['end_date'],'%Y-%m-%d').date()
            if start_date_select < today:
                errors.append('Your startdate must to selected future date!')
            if start_date_select > end_date_select:
                errors.append('Your end date cannot before start date!')
            print start_date_select
            print end_date_select
        modelsResponse = {}

        if errors:
            modelsResponse['isRegistered'] = False
            modelsResponse['errors'] = errors

        else:
            LoginUser = User.objects.get(id=user_id)
            travel = self.create(destination = userData['destination'],description = userData['description'], creator = LoginUser, start_date = userData['start_date'], end_date = userData['end_date'])
            travel.travel_join.add(LoginUser)
            travel.save()
            modelsResponse['isRegistered'] = True
            modelsResponse['travel'] = travel

        return modelsResponse

    def join_travel(self, travel, user_id):
        LoginUser= User.objects.get(id=user_id)
        Travel_join = travel
        Travel_join.travel_join.add(LoginUser)
        Travel_join.save()

class Travel(models.Model):
    destination = models.CharField(max_length = 200)
    description = models.TextField()
    creator = models.ForeignKey(User, related_name="travel_owner")
    travel_join = models.ManyToManyField(User, related_name="travel_user")
    start_date = models.DateField(auto_now = False, auto_now_add = False)
    end_date = models.DateField(auto_now = False, auto_now_add = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TravelManager()
