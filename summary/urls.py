from django.urls import path

from .views import (CreateSummaryView, GetParticularSummaryView, ListSummaryView, PopulateView,
                    SummaryFromLinkView, SummaryFromTextView)

urlpatterns = [
    path('get-all/', ListSummaryView.as_view()),
    path('create/', CreateSummaryView.as_view()),
    path('get/<int:id>', GetParticularSummaryView.as_view()),
    path('get-summary-from-text/', SummaryFromTextView.as_view()),
    path('get-summary-from-link/', SummaryFromLinkView.as_view()),
    path('populate/', PopulateView.as_view()),
]
