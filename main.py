from tinydb import TinyDB, Query
from flask import Flask, render_template, url_for, request, redirect, flash

app = Flask(__name__)
db = TinyDB('db.json')

app.config['SECRET_KEY'] = '(*7gjyG&67Y87b 98Y98N*UHkiuYiug*(B'

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', db=db)

@app.route('/create', methods=["POST", "GET"])
def create():
    if request.method == "POST":
        db.insert({"name": request.form["name"], "age": request.form["age"], "height": request.form["height"]})
        return redirect('/')

    return render_template('create.html')


@app.route('/delete/<int:id>')
def delete(id):
    db.remove(doc_ids=[id])
    return redirect('/')

@app.route('/edit/<int:id>', methods=["POST", "GET"])
def edit(id):
    user = db.get(doc_id=id)

    if request.method == "POST":
        db.update({"name": request.form["name"], "age": request.form["age"], "height": request.form["height"]}, doc_ids=[id])
        return redirect('/')

    return render_template('edit.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)