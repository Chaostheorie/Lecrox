from app import app
from db_setup import init_db, db_session
from forms import SnippetSearchForm, snippetForms
from flask import flash, render_template, request, redirect
from models import snippets

init_db()
# functions
def save_changes(snippet, form, new=False):
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    snippet = snippets()

    snippet.name = form.name
    snippet.type = form.type
    snippet.content = form.content
    snippet.description = form.description

    if new:
        # Add the new album to the database
        db_session.add(snippet)

    # commit the data to the database
    db_session.commit()

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    search = SnippetSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search)

@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search.data['search'] == '':
        qry = db_session.query(Album)
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', results=results)


@app.route('/new_snippet', methods=['GET', 'POST'])
def new_snippet():
    form = snippetForms(request.form)
    if request.method == 'POST' and form.validate():
        # save the album
        snippet = snippets()
        save_changes(snippet, form, new=True)
        flash('Snippet created successfully!')
        return redirect('/')

    return render_template('new_snippet.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
