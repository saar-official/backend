import re
import json
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from summary.utils import (check_if_text_already_exists,
                           fetch_summary_and_key_highlights,
                           scrape_data_from_url)

from .models import Summary
from .serializers import SummarySerializer


import string
import random


def generate_unique_code():
    length = 6
    while True:
        code = random.randint(0, 1000)
        if Summary.objects.filter(id=code).count() == 0:
            break
    return code


# Create your views here.
headers = {
    "User-Agent": "PostmanRuntime/7.29.0",
    "Accept": "*/*",
    "Postman-Token": "a977868d-1e05-4443-921b-6b8951176242",
    "Host": "localhost:8000",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Content-Length": "742",
    "Content-type": "application/json",
    "Cookie": "csrftoken=175ZmNkNuf0iwW2mK936pvZsiZ05LeiixKXiMjlhdcRgq2lMV4BhCEFI57RWIE1L",
}


class ListSummaryView(generics.ListAPIView):
    """
    api to list all summaries created so far
    """
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer


class GetSummaryFromTextView(generics.CreateAPIView):
    serializer_class = SummarySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CreateSummaryView(generics.CreateAPIView):
    """
    api to create a summary from text or link
    """
    serializer_class = SummarySerializer
    queryset = Summary.objects.all()

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        if data.get("link", False):
            check_if_text_already_exists(text)
            text = scrape_data_from_url(data["link"])
            summary, highlights = fetch_summary_and_key_highlights(text)
            data["text"] = text
            data["summary"] = summary
            data["highlights"] = highlights
        elif data.get("text", False):
            text_obj = check_if_text_already_exists(data.get("text"))
            if text_obj:
                return Response(text_obj, status=status.HTTP_3)
            summary, highlights = fetch_summary_and_key_highlights(
                data["text"])
            data["summary"] = summary
            data["highlights"] = highlights
        else:
            return Response({'text': 'At least one of text or link should have a value.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SummaryFromTextView(APIView):
    def post(self, request):
        data = request.data
        try:
            summary, highlights = fetch_summary_and_key_highlights(
                text=data["text"], headers=headers)
            response = {"summary": summary, "highlights": highlights}
            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response({"error": "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SummaryFromLinkView(generics.CreateAPIView):
    serializer_class = SummarySerializer
    model = Summary

    def post(self, request):
        data = request.data
        try:
            scraped_data = scrape_data_from_url(
                url=data['link'], headers=headers)
            summary, highlights = fetch_summary_and_key_highlights(
                text=scraped_data['text'], headers=headers)
            # response = {"summary": summary, "highlights": highlights}

            # populate database

            s_data = {}
            s_data['text'] = scraped_data['text']
            s_data['link'] = scraped_data['link']
            s_data['summary'] = summary
            s_data['highlights'] = f"{highlights}"
            s_data['heading'] = scraped_data['text'][:250]
            s_data['slug'] = "-".join([word.upper()
                                      for word in re.split(',| |_|-|!|\?|\.|"', scraped_data['text'][:250])])[:50]
            s_data['ministry'] = "CENTRAL MINISTRY"
            s_data['assets'] = f"{scraped_data['assets']}"
            # summary_object = Summary.objects.create(**s_data)
            serializer = self.get_serializer(data=s_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetParticularSummaryView(generics.RetrieveAPIView):
    """
    api to retrieve summary from `id`
    """
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        try:
            data['highlights'] = eval(data['highlights'])
            data['assets'] = eval(data['assets'])
        except:
            print('cannot evaluate highlights')
        return Response(data)


class PopulateView(APIView):
    def get(self, request):
        with open("summary/data.json") as json_file:
            data = json.load(json_file)
            for ministry, val in data.items():
                for summary in val:
                    # summary['id'] = generate_unique_code()
                    summary['ministry'] = ministry
                    summary['summary'] = summary['text'][:300]
                    summary['slug'] = "-".join([word.upper()
                                                for word in summary['heading'].split()])
                    summary_obj = Summary(summary)
                    # summary_obj.save()
                    summary_serializer = SummarySerializer(data=summary)
                    if summary_serializer.is_valid():
                        summary_serializer.save()
        return Response({"success": Summary.objects.all()}, status=status.HTTP_200_OK)
