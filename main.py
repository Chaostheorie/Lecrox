from app import app
from db_setup import init_db, db_session
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

def add_snippet(input):
        if input["description"] == "":
            print(input)
            snippet = snippets (
            name = input["name"],
            type = input["type"],
            content = input["content"],
            )
            db.session.add(snippet)
            db.session.commit()
        else:
            print(input)
            snippet = snippets (
            name = input["name"],
            type = input["type"],
            content = input["content"],
            description = input["description"])
            db.session.add(snippet)
            db.session.commit()
            flash("Der Eintrag: " + str(input["name"]) + " Erfolgreich eingetragen!")
        return_url = request.referrer or '/'
        return redirect(return_url)


# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    search = make_dict(request)
    if request.method == 'POST':
        input = make_dict(request)
        return search_results(search)

    return render_template('index.html')

@app.route('/results')
def search_results(search):
    input = make_dict(request)
    text = ""
    # debug
    print("Peng")
    print(input)
    print(search)
    if input["type"]=="snippet":
        snippets.reindex()
        results = query, total = snippets.search(input["search"], 1, 100)
        if input['search'] == '':
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
        if input['search'] == '':
                qry = db_session.query(plans)
                results = qry.all()
                if len(plans.query.all()) > 1:
                    text = " Es wurden " + str(len(plans.query.all())) + " Ergebnisse gefunden:"
                else:
                    text = "Es wurde" + str(len(plans.query.all())) + " Ergebniss gefunden: "
                return render_template("results.html", results=results)

    if results[1] > 1:
        text = "Es wurden " + str(total) + " Ergebnisse für den Suchbegriff " + input["search"] + " gefunden:"
    elif results[1] == 1:
        text = "Es wurde 1 Ergebniss für den Suchbegriff " + input["search"] + " gefunden:"
    else:
        flash("Kein Ergebniss für den Suchbegriff " + str(input["search"]) + " gefunden")
        return_url = request.referrer or '/'
        return redirect(return_url)
    return render_template('results.html', results=query, text=text)

@app.route("/plans-info")
def plans_info():
    return render_template("plans-info.html")

@app.route("/snippets-info")
def snippets_info():
    return render_template("snippets_info.html")

@app.route("/about-me")
def about_me():
    return render_template("about_me.html")

@app.route("/admin")
@roles_required("Admin")
def admin():
    return render_template("admin/admin.html")

@app.route("/admin/add_snippet", methods=['GET', 'POST'])
@roles_required("Admin")
def add_snippet_view():
    if request.method == 'GET':
        return render_template("admin/add_snippet.html")

    if request.method == 'POST':
        add_snippet(make_dict(request))

# Errorhandler pages
@app.errorhandler(404)
def page_not_found(e):
	return_url = request.referrer or '/'
	return render_template("404.html", return_url=return_url), 404

# Run the application
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
