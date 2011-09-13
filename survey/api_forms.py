from django import forms
from django.utils.translation import ugettext_lazy as _
from models import Survey, Question, Choice
import extjs



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('id', 'order', 'text', 'qstyle', 'qtype')
        
    def as_customized_extjs(self, question):
        fields = self.as_extjsfields(["text",
                                      "order",
                                      "qstyle",
                                      "qtype"])
        id = {'xtype': 'hidden',
              'name': 'id',
              'value': question.id}
        
        fields['text'].update({'anchor': '-20'})
        fields['qstyle'].update({'anchor': '-20'})
        
        desc = {'xtype': 'panel',
                'layout': 'form',
                'frame': True,
                'border': False,
                'items': [
                    id,
                    fields['order'],
                    fields['qtype'],
                    fields['text'],
                    fields['qstyle'],
                    ]}
        return desc
extjs.register(QuestionForm)   

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ('id', 'title', 'slug', 'description', 'opens', 'closes')
        
    def as_customized_extjs(self, survey):
        fields = self.as_extjsfields(["title",
                                      "description",
                                      "opens",
                                      "closes",
                                      "slug"])
        id = {'xtype': 'hidden',
              'name': 'id',
              'value': survey.id}
        
        fields['title'].update({'anchor': '-20'})
        fields['description'].update({'anchor': '-20'})
        
        # we don't care about time
        fields['opens'].update({'value': fields['opens']['value'][:10]});
        fields['closes'].update({'value': fields['closes']['value'][:10]});
        desc = {'xtype': 'panel',
                'layout': 'form',
                'frame': True,
                'border': False,
                'items': [
                    id,
                    fields['title'],
                    fields['slug'],
                    fields['description'],
                    fields['opens'],
                    fields['closes'],
                    ]}
        return desc
extjs.register(SurveyForm)   

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('id', 'order', 'text')
extjs.register(ChoiceForm)   