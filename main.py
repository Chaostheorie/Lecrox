from app import app
from db_setup import init_db, db_session
from forms import SnippetSearchForm, snippetForms
from flask import flash, render_template, request, redirect
from models import *
from flask_user import *
from search import *

#init the database out of db_setup.py
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
        return search_results(search)

    return render_template('index.html')

@app.route('/results')
def search_results(search):
    input = make_dict(request)
    # debug
    print("Peng")
    print(input)
    if input["type"]=="snippet":
        snippets.reindex()
        results = query, total = snippets.search(input["search"], 1, 100)
        if search.data['search'] == '':
                qry = db_session.query(snippets)
                results = qry.all()
                if len(snippets.query.all()) > 1:
                    text = " Es wurden " + str(len(snippets.query.all())) + " Ergebnisse gefunden:"
                else:
                    text = "Es wurde" + str(len(snippets.query.all())) + " Ergebniss gefunden: "
                return render_template("results.html", results=results)

    if input["type"]=="plan":
        plans.reindex()
        results = query, total = plans.search(input["search"], 1, 100)
        if search.data['search'] == '':
                qry = db_session.query(plans)
                results = qry.all()
                if len(plans.query.all()) > 1:
                    text = " Es wurden " + str(len(plans.query.all())) + " Ergebnisse gefunden:"
                else:
                    text = "Es wurde" + str(len(plans.query.all())) + " Ergebniss gefunden: "
                return render_template("results.html", results=results)

    if not results:
        flash('No results found!')
        return redirect('/')

    else:
        if results[1] > 1:
            text = "Es wurden " + str(total) + " Ergebnisse für den Suchbegriff " + input["search"] + " gefunden:"
        if results[1] == 1:
            text = "Es wurde 1 Ergebniss für den Suchbegriff " + input["search"] + " gefunden:"
        return render_template('results.html', results=query, text=text)

@app.route("/plans-info")
def plans_info():
    return render_template("plans-info.html")

@app.route("/snippets-info")
def snippets-info():
    return render_template
@app.route("/about-me")
def about_me():
    return render_template("about_me.html")

# Errorhandler pages
@app.errorhandler(404)
def page_not_found(e):
	return_url = request.referrer or '/'
	return render_template("404.html", return_url=return_url), 404

# Run the application
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
