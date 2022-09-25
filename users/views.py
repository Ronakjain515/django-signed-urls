from rest_framework import status
from users.utils import ResponseInfo
from .utils import get_pre_signed_url
from .cookie import get_signed_cookie
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView


class RetrieveSignedTokenURLAPIView(RetrieveAPIView):
	"""
	Class for creating api for retrieve Signed token based url.
	"""
	permission_classes = ()
	authentication_classes = ()
	serializer_class = None

	def __init__(self, **kwargs):
		"""
		 Constructor function for formatting the web response to return.
		"""
		self.response_format = ResponseInfo().response
		super(RetrieveSignedTokenURLAPIView, self).__init__(**kwargs)

	def get(self, request, *args, **kwargs):
		"""
		GET Method for retrieve Signed token based url.
		"""
		data = {
			"signed_token_url": get_pre_signed_url("dummy-folder/dummy.pdf")
		}
		self.response_format["data"] = data
		self.response_format["error"] = None
		self.response_format["status_code"] = status.HTTP_200_OK
		self.response_format["message"] = ["Success."]
		return Response(self.response_format)


class RetrieveSignedCookieURLAPIView(RetrieveAPIView):
	"""
	Class for creating api for retrieve Signed Cookie based url.
	"""
	permission_classes = ()
	authentication_classes = ()
	serializer_class = None

	def __init__(self, **kwargs):
		"""
		 Constructor function for formatting the web response to return.
		"""
		self.response_format = ResponseInfo().response
		super(RetrieveSignedCookieURLAPIView, self).__init__(**kwargs)

	def get(self, request, *args, **kwargs):
		"""
		GET Method for retrieve Signed Cookie based url.
		"""
		data = {
			"signed_token_url": get_signed_cookie("dummy-folder/*", "dummy-folder/dummy.m3u8")
		}
		self.response_format["data"] = data
		self.response_format["error"] = None
		self.response_format["status_code"] = status.HTTP_200_OK
		self.response_format["message"] = ["Success."]
		return Response(self.response_format)
