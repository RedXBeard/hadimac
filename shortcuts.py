#-*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

import re

def r(template_name, dictionary, request):
    return render_to_response(template_name,
                              dictionary,
                              context_instance=RequestContext(request))

def rs(template_name, dictionary, request = None):
    if request:
        return render_to_string(template_name,
                                dictionary,
                                context_instance=RequestContext(request))
    else:
        return render_to_string(template_name,
                                dictionary)
