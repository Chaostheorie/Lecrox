# forms.py
from elasticsearch import Elasticsearch
from wtforms import Form, StringField, SelectField

class SnippetSearchForm(Form):
    choices = [('name', 'name'),
                ('type', 'type'),
               ('content', 'content')]
    select = SelectField('Search for snippets:', choices=choices)
    search = StringField('')

class snippetForms(Form):
    snippet_types = [('Praise', 'Praise'),
                   ('Worship', 'Worship'),
                   ('Gospel', 'Gospel'),
                   ('Bible snippet', 'Bible Snippet')
                   ]
    name = StringField('Name')
    type = SelectField('Type', choices=snippet_types)
    content = StringField('Content')
    description = StringField('Description')
