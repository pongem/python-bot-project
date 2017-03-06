# -*- coding: utf-8 -*-
# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from chatbots.models import BotMessage
from chatbots.mod_SET_Helper import *

import json
import urllib2

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def pong(request):

	# test add new message
	# p = BotMessage(message_text="What's your name?", intent_text="check_botinfo", intent_arg1="None", intent_arg2="None", intent_arg3="None", pub_date=timezone.now())
	# p.save()

	return render(request, "index.html", 
		{ 
		'unicode_test' : 'ทดสอบภาษาไทย', 
		'welcome_title': 'Hello, django'
		})


def bot(request):

	# get bot messages
	arrBotMessages = BotMessage.objects.all()

	return render(request, "bot.html", 
		{ 
		'welcome_title': 'This is bot messages:',
		'bot_messages' : arrBotMessages
		})

@csrf_exempt
def botcallback(request):

	token = None

	if request.method == 'POST':
		token = _getTokenFromRequestBody(request.body)
		data = json.dumps({
			"replyToken":token,
			"messages":[{
				"type":"text",
				"text": "test"
			}]
		})

		_postback(data, token)
	else :
		HttpResponseNotAllowed("Method Not Allowed")

	return HttpResponse("token: %s" % token)

def price(request):
	symbol = request.GET.get('symbol')
	print ("query string: %s" % symbol)
	if not symbol :
		symbol = "CPF"
	else:
		symbol = symbol.upper()
	print ("symbol: %s" % symbol)
	helper = SETFetch()
	price = helper.fetchCurrentStockInfo( symbol )
	return HttpResponse("%s price: %s" % (symbol,price))



def _getTokenFromRequestBody(body):

	try:

		json_request = json.loads(body)

		events_obj = json_request['events']
		event_obj = events_obj[0]
		token = event_obj['replyToken']
		return token

	except KeyError:
		HttpResponseServerError("Malformed data!")

def _postback(data, token):
	url = 'https://api.line.me/v2/bot/message/reply'
	opener = urllib2.build_opener(urllib2.HTTPHandler)
	request = urllib2.Request(url, data=json.dumps(data))
	request.add_header("Content-Type", "application/json; charset=UTF-8")
	request.add_header("Authorization", "Bearer %s" % token)                                   
	opener.open(request)



