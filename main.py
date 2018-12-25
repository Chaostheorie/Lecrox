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
@app.route("/add_snippet", methods=["Post"])
@login_required
def add_snippet():
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    values = list(request.form.values())
    keys = list(request.form.keys())
    new_snippet = {}
    for i in range(len(keys)):
        value = values[i]
        key = keys[i]
        new_snippet.update({key:value})
    print(new_snippet)
    snippet = snippets (
    name = new_snippet["name"],
    type = new_snippet["type"],
    content = new_snippet["content"],
    description = new_snippet["description"],
    )
    db_session.add(snippet)
    # commit the data to the database
    db_session.commit()
    flash('Added successfully!')
    return redirect(request.referrer or '/')

# Routes
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    search = SnippetSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    all_columns = json.load(open("static/json/snippets_columns.json", "r"))
    return render_template('index.html', form=search, columns=all_columns)

@app.route('/results')
@login_required
def search_results(search):
    values = list(request.form.values())
    keys = list(request.form.keys())
    input = {}
    for i in range(len(keys)):
        value = values[i]
        key = keys[i]
        input.update({key:value})
    kwargs = {input["type"]:input["search"]}
    print(kwargs)
    for snippet in snippets.query.all():
        add_to_index('snippets_index', snippet)
    res = str(query_index(snippets_index, input["search"], 1, 100)[0])[1]
    result = []
    for i in len(id):
        res_1 = snippets.query.filter_by(id=id[i]).all()
        result.append(res_1)

    if search.data['search'] == '':
        qry = db_session.query(snippets)
        results = qry.all()
        return render_template("results.html", results=results)

    if not result:
        flash('No results found!')
        return redirect('/')

    else:
        results = snippets.query.filter_by(**kwargs).all()
        return render_template('results.html', results=result)

@app.route('/new_snippet', methods=['GET', 'POST'])
@login_required
def new_snippet():
    form = snippetForms(request.form)
    if request.method == 'POST' and form.validate():
        # save the snippet

        flash('Snippet created successfully!')
        return redirect('/')

    all_types = json.load(open("static/json/types.json", "r"))
    print(all_types)
    return render_template('new_snippet.html', types=all_types)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
