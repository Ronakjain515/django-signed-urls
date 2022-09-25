from rest_framework.urls import path
from .views import (
				   RetrieveSignedTokenURLAPIView,
				   RetrieveSignedCookieURLAPIView,
				   )

urlpatterns = [
	path("retrieveSignedTokenURL", RetrieveSignedTokenURLAPIView.as_view(), name="retrieve-signed-token-url"),
	path("retrieveSignedCookieURL", RetrieveSignedCookieURLAPIView.as_view(), name="retrieve-signed-Cookie-url"),
]
