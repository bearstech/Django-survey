from django import forms
from django.utils.translation import ugettext_lazy as _
from models import Question, Choice
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

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('id', 'order', 'text')
extjs.register(ChoiceForm)   