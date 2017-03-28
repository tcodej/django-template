import os, utils
from django.conf import settings
from django.core import serializers
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse("")

def feed(request):
	feed = utils.getFeed()
	return JsonResponse(feed, safe=False)

@staff_member_required
def publish(request, dest='test'):
	try:
		feed = utils.getFeed(request.user.username)
		utils.uploadJSON(feed, dest)
		messages.success(request, 'Content was published successfully.')
	except Exception, e:
		messages.error(request, 'Content publish failed. Error: %s' % str(e))
	return redirect(request.META.get('HTTP_REFERER'))
