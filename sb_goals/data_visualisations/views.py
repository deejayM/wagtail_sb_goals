import pandas as pd
import altair as alt
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

User = get_user_model()

class DataVisualisationsView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts.html', {"customers": 10})  # fix the path here.


def get_data(request, *args, **kwargs):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data)  # http response


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = ['Users', 'Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
        qs_count = User.objects.all().count()
        data = {
            "labels": labels,
            "default": [2, 12, 3, 7, 10, 9, 4]
        }
        return Response(data)
