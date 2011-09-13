from django.db import models
from django.db.models import Q, Max
from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.http import HttpResponseNotFound
from django.template import loader, RequestContext
from django.template.defaultfilters import slugify
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import delete_object
from django.contrib.auth.decorators import login_required

from survey.models import Survey, Answer, Question, Choice
from django.contrib.auth.decorators import login_required
from survey.grids import SurveyGrid, QuestionGrid, ChoiceGrid
from django.utils import simplejson as json
from extjs import utils

from api_forms import QuestionForm, ChoiceForm, SurveyForm
import api_utils

def base(request):
    raise Http404

@login_required
def surveys(request, survey_id=None):
    if request.method == 'GET':
        qs = Survey.objects.all()
        return api_utils.response(request, qs, SurveyGrid)
    elif request.method == 'POST':
        form = api_utils.load_form(request, SurveyForm)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.created_by = request.user
            survey.editable_by = request.user
            survey.visible = True
            survey.public = False
            survey.allows_multiple_interviews = False
            survey.save()
            qs = Survey.objects.filter(id=survey.id)
            return api_utils.response(request, qs, SurveyGrid)
        else:
            return api_utils.response_error(request, form)
    elif request.method == 'DELETE':
        survey = get_object_or_404(Survey, id=survey_id)
        #survey.delete()
        return api_utils.success()
    raise Http404

@login_required
def questions(request, survey_id, question_id=None):
    survey = get_object_or_404(Survey, id=survey_id)
    if request.method == 'GET':
        qs = Question.objects.filter(survey__id=survey_id).order_by('order', 'id')
        return api_utils.response(request, qs, QuestionGrid)
    elif request.method == 'POST':
        form = api_utils.load_form(request, QuestionForm)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            if question.order is None:
                res = Question.objects.filter(survey__id=survey_id).aggregate(Max('order'))
                max_order = res['order__max']
                if max_order:
                    question.order = max_order + 1
                else:
                    question.order = 0
            question.save()
            qs = Question.objects.filter(id=question.id)
            return api_utils.response(request, qs, QuestionGrid)
        else:
            return api_utils.response_error(request, form)
    elif request.method == 'DELETE':
        question = get_object_or_404(Question, id=question_id)
        question.delete()
        return api_utils.success()
    raise Http404

@login_required   
def edit_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    if request.method == 'GET':
        form = SurveyForm(instance=survey)
        info = {'id': survey.id,
        }
        data = {'info': info,
                'form' : form.as_customized_extjs(survey),
        }
        json_data = json.JSONEncoder(ensure_ascii=False).encode({
            'success':True,
            'data': data 
        })
        return utils.JsonResponse(json_data)
    elif request.method == 'POST':
        form = SurveyForm(request.REQUEST, instance=survey)
        if form.is_valid():
            survey = form.save()
            return api_utils.success()
        else:
            return utils.JsonResponse(form.as_extjsdata())          
    raise Http404


@login_required
def question_recalculate_orders(request, survey_id):
    qs = Question.objects.filter(survey__id=survey_id).order_by('order', 'id')
    for i, question in enumerate(qs):
        question.order = i
        question.save()
    return api_utils.success()
    
 
@login_required   
def edit_question(request, survey_id, question_id=None):
    survey = get_object_or_404(Survey, id=survey_id)
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'GET':
        form = QuestionForm(instance=question)
        info = {'id': question.id,
        }
        data = {'info': info,
                'form' : form.as_customized_extjs(question),
        }
        json_data = json.JSONEncoder(ensure_ascii=False).encode({
            'success':True,
            'data': data 
        })
        return utils.JsonResponse(json_data)
    elif request.method == 'POST':
        form = QuestionForm(request.REQUEST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.save()
            return api_utils.success()
        else:
            return utils.JsonResponse(form.as_extjsdata())          
    raise Http404

def choices(request, survey_id, question_id, choice_id=None):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'GET':
        qs = Choice.objects.filter(question__id=question_id).order_by('order', 'id')
        return api_utils.response(request, qs, ChoiceGrid)
    elif request.method == 'POST':
        form = api_utils.load_form(request, ChoiceForm)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question
            if choice.order is None:
                res = Choice.objects.filter(question__id=question_id).aggregate(Max('order'))
                max_order = res['order__max']
                if max_order:
                    choice.order = max_order + 1
                else:
                    choice.order = 0
            choice.save()
            qs = Choice.objects.filter(id=choice.id)
            return api_utils.response(request, qs, ChoiceGrid)
        else:
            return api_utils.response_error(request, form)
    elif request.method == 'PUT':
        api_utils.coerce_put_post(request)

        choice = get_object_or_404(Choice, id=choice_id)
        json_data = request.REQUEST.get('data', [])
        decoded_data = json.loads(json_data)
        if 'text' in decoded_data:
            choice.text = decoded_data['text']
        if 'order' in decoded_data:
            choice.order = int(decoded_data['order'])
        choice.save()
        return api_utils.success()
    elif request.method == 'DELETE':
        choice = get_object_or_404(Choice, id=choice_id)
        choice.delete()
        return api_utils.success()
    raise Http404

@login_required
def choice_recalculate_orders(request, survey_id, question_id):
    qs = Choice.objects.filter(question__id=question_id).order_by('order', 'id')
    for i, choice in enumerate(qs):
        choice.order = i
        choice.save()
    return api_utils.success()