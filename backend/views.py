from django.shortcuts import render
from django.conf import settings

import requests
import logging
import datetime
import json
import hashlib
import urllib
from backend.models import Users
from backend.models import Vote
from backend.serializers import VoteSerializer

from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from django.contrib.auth.hashers import check_password

from rest_auth.registration.views import RegisterView
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model

class VoteList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        userid=request.user
        votes = Vote.objects.all()
        serializer = VoteSerializer(votes,many=True)
        return Response(serializer.data)

class VoteCreate(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        message = {'error': 'Check parameters, name should be unique'}
        return Response(message,status=400)

class VoteUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self, request, id):
        userid=request.user
        vote=Vote.objects.get(id=id)
        data = JSONParser().parse(request)
        serializer = VoteSerializer(vote,data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        message = {'error': 'Check parameters'}
        return Response(message,status=400)

class VoteDelete(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request, id):
        try:
            vote = Vote.objects.get(id=id)
        except vote.DoesNotExist:
            message = {'error': 'Vote doesnt exist'}
            return Response(message,status=404)
        vote.delete()
        message = {'info': 'Vote delete successfully'}
        return Response(message,status=200)

class PetsList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        userid=request.user
        totalVotes = len(Vote.objects.all());
        catsVotes = len(Vote.objects.filter(cats_or_dogs="CATS"));
        dogsVotes = len(Vote.objects.filter(cats_or_dogs="DOGS"));
        catsPercentage = (100/totalVotes)*catsVotes;
        dogsPercentage = (100/totalVotes)*dogsVotes;
        message=[{'name': 'CATS', 'petresult': catsVotes, 'percentage': catsPercentage}, {'name': 'DOGS', 'petresult': dogsVotes, 'percentage': dogsPercentage}];
        return Response(message,status=200)

class ColorsList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        userid=request.user
        totalVotes = len(Vote.objects.all());
        redVotes = len(Vote.objects.filter(color="RED"));
        greenVotes = len(Vote.objects.filter(color="GREEN"));
        yellowVotes = len(Vote.objects.filter(color="YELLOW"));
        blueVotes = len(Vote.objects.filter(color="BLUE"));
        redPercentage = (100/totalVotes)*redVotes;
        greenPercentage = (100/totalVotes)*greenVotes;
        yellowPercentage = (100/totalVotes)*yellowVotes;
        bluePercentage = (100/totalVotes)*blueVotes;
        message=[{'name': 'RED', 'colorresult': redVotes, 'percentage': redPercentage},
          {'name': 'BLUE', 'colorresult': blueVotes, 'percentage': bluePercentage},
          {'name': 'YELLOW', 'colorresult': yellowVotes, 'percentage': yellowPercentage},
          {'name': 'GREEN', 'colorresult': greenVotes, 'percentage': greenPercentage}];
        return Response(message,status=200)
