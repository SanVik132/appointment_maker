from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from api.models import *
from api.serializers import *
from rest_framework.authtoken.models import Token
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate,login
from .jwt_token_auth import get_token,decrypt_token
from datetime import datetime as dt

def create_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token


class SignUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    http_method_names = ['post']
    
    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = request.data['email']
            password = request.data['password']
            first_name = request.data['first_name']
            User.objects.create_user(email=email,password=password,first_name=first_name,is_active=True)
            return Response({"status":1,"message":"User added","data":serializer.data})
        if "first_name" in serializer.errors:
            return Response({"status":0,"message":"first_name - " + serializer.errors['first_name'][0]})
        if "email" in serializer.errors:
            if serializer.errors['email'][0] == "user with this email address already exists.":
                return Response({"status":0,"message":"Email is already registered"})
            return Response({"status":0,"message":"email - " + serializer.errors['email'][0]})
        if "password" in serializer.errors:
            return Response({"status":0,"message":"passowrd - " + serializer.errors['password'][0]})
        return Response(serializer.errors)

class LogInViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    http_method_names = ['post']
    def get_user(self,email):
        try:
            user = User.objects.get(email=email)
            return user
        except:
            return 0


    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        current_site = get_current_site(request)
        email = request.data['email']
        password = request.data['password']
        user = self.get_user(email)
        if user:
            if user.is_active :
                auth_status = authenticate(email=email,password=password)
                if auth_status:
                    token = get_token(user)                    
                    data = {"user_id":user.id,"email":user.email,"first_name":user.first_name,"token":token['access_token']}
                    return Response({"status":1,"message":"You have logged in successfully","data":data})
                else:
                    return Response({"status":0,"message":"Unable to log in, please check your password"})
            else:
                return Response({"status":0,"message":"Email is not registered"})


class AppointmentiewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    http_method_names = ['get','post','delete']
    
    def list(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        current_site = get_current_site(request)
        user = decrypt_token(token)
        if user:
            appointment = Appointment.objects.filter(user=user)
            appointment_list = []
            for list_appointment in appointment:
                appointment_list.append({"id":list_appointment.id,"appointment_datetime":list_appointment.datetime,"timestamp":list_appointment.timestamp})
            return Response({"status":1,"message":"success","data":appointment_list})
        else:
            return Response({"status":3,"message":"invalid access token"})
    
    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = request.META.get("HTTP_AUTHORIZATION")
            user = decrypt_token(token)
            if user:
                time = Time.objects.last()
                apt_time = request.data['datetime']
                print(apt_time)
                t = dt.strptime(apt_time, '%Y-%m-%d %H:%M:%S').time()
                print(t)
                
                if time.start < t:
                    return Response({"status":0,"message":"Upload a time between 9-5"})
                elif t > time.end:
                    return Response({"status":0,"message":"Upload a time between 9-5"})
                serializer.save(user=user)
                
                return Response({"status":1,"message":"Uploaded successfully","data":serializer.data})
            else:
                return Response({"status":3,"message":"invalid access token"})
        return Response(serializer.errors)

    def destroy(self, request, pk=None):
        token = request.META.get("HTTP_AUTHORIZATION")
        user = decrypt_token(token)
        if user:
            try:
                kk = Appointment.objects.get(user=user,id=pk)
                kk.delete()
            except:
                return Response({"status":0,"message":"Provide valid Appointment id"})
            return Response({"status":1,"message":"Appointment deleted successfully"})
        else:
            return Response({"status":0,"message":"invalid access token"})