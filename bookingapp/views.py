from django.shortcuts import render
from rest_framework.generics import GenericAPIView,RetrieveAPIView
from rest_framework import mixins
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from . serializers import advisorviewserializer, advisorregserializer,advisorbookserializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from.models import advisor
from userapp.models  import User
from rest_framework.response import Response



# Create your views here.

# for Creating Advisor---------------------------------------------------------------------------------
class advisorgeneric(GenericAPIView,mixins.CreateModelMixin):
    serializer_class = advisorregserializer
    permission_classes = (AllowAny,)
    def post(self,request):
        return self.create(request,status=status.HTTP_200_OK)



# for allowing user with JWT to see (GET)advisor list

class advisorview(RetrieveAPIView):
    authentication_class = JSONWebTokenAuthentication
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        user1 = User.objects.get(id=id)
        if (user1 == request.user):                           # checking the userid passed on url  is equal to authorised id
            advisor1=advisor.objects.all()
            serailizer=advisorviewserializer(advisor1,many=True)
            return Response(serailizer.data,status=status.HTTP_200_OK)
        else: return Response(status=status.HTTP_400_BAD_REQUEST)




# To allow user with JWT to book advisor------------------------------------------------>

class advisorbooking(GenericAPIView,mixins.UpdateModelMixin):
    print("I ma in class")
    serializer_class = advisorbookserializer
    authentication_class = JSONWebTokenAuthentication
    permission_classes = [IsAuthenticated]
    queryset = advisor.objects.all()
    lookup_field = 'id'

    def post(self,request,id1=None,id=None):
        user1 = User.objects.get(id=id1)
        print(request.data)                    # this brings bookingtime data--- set {"bookingtime":"{{current_timestamp}}"} in POSTMAN for current datetime
        if(user1 == request.user):             #var current_timestamp = new Date();               in POSTMAN prerequest scripts for posting current time in booking time
                                               #postman.setEnvironmentVariable("current_timestamp", current_timestamp.toISOString());
            print(request.user)                # this is authorised user to the request
            ad = advisor.objects.get(id=id)
            print("advisor object", ad.first_name, self.request.data)
            return self.update(self.request, id, status=status.HTTP_201_CREATED)
        else: return Response(status=status.HTTP_400_BAD_REQUEST)



# To show all booked advisors-----------------------------

class advisorbookingview(RetrieveAPIView):
    authentication_class = JSONWebTokenAuthentication
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        user1 = User.objects.get(id=id)
        if (user1 == request.user):          # checking the userid passed on url  is equal to authorised id
            advisor1=advisor.objects.exclude(bookingtime =None)
            #print(advisor1)
            serailizer=advisorviewserializer(advisor1,many=True)
            return Response(serailizer.data,status=status.HTTP_200_OK)
        else: return Response(status=status.HTTP_400_BAD_REQUEST)
