from app import app
from db_setup import init_db, db_session
from forms import SnippetSearchForm, snippetForms
from flask import flash, render_template, request, redirect
from models import *
import json
from flask_user import *
from search import *

init_db()

# functions

def make_dict(request):
    values = list(request.form.values())
    keys = list(request.form.keys())
    input = {}
    for i in range(len(keys)):
        value = values[i]
        key = keys[i]
        input.update({key:value})
    return input

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    search = SnippetSearchForm(request.form)
    if request.method == 'POST':
        input = make_dict(request)
        print(input)
        return search_results(search)
    return render_template('index.html')

@app.route('/results')
def search_results(search):
    input = make_dict(request)
    snippets.reindex()
    results = query, total = snippets.search(input["search"], 1, 100)

    if search.data['search'] == '':
        qry = db_session.query(snippets)
        results = qry.all()
        return render_template("results.html", results=results, total=len(snippets.query.all()))

    if not results:
        flash('No results found!')
        return redirect('/')

    else:
        return render_template('results.html', results=query, total=total)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
