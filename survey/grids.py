from extjs import grids
from models import Survey
from survey.models import Question, Choice

class SurveyGrid(grids.ModelGrid):  
    model = Survey
    list_mapping = ['id', 'title']

class QuestionGrid(grids.ModelGrid):  
    model = Question
    fields = ['id', 'text', 'qstyle', 'qtype', 'required', 'order', 'survey_id']
    list_mapping = ['id', 'text', 'qstyle', 'qtype', 'required', 'order',]
    mapping = {
        'survey_id' : 'survey__id',
    }

class ChoiceGrid(grids.ModelGrid):  
    model = Choice
    fields = ['id', 'text', 'order', 'question_id', 'survey_id']
    list_mapping = ['id', 'text', 'order', ]
    mapping = {
        'survey_id' : 'question__survey__id',
        'question_id' : 'question__id',
    }
