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

from chatbots.models import BotMessage

from django.utils import timezone

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


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

