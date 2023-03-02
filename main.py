from tinydb import TinyDB, Query
from flask import Flask, render_template, url_for, request, redirect, flash, session
from datetime import date

app = Flask(__name__)
db = TinyDB('db.json')

app.config['SECRET_KEY'] = '(*7gjyG&67Y87b 98Y98N*UHkiuYiug*(B'

@app.route('/', methods=["POST", "GET"])
@app.route('/read', methods=["POST", "GET"])
def index():
    od = sorted(db.all(), key=lambda k: (k['date'], k['tstart'], k['class']))   # СОРТИРОВКА ЗАПИСЕЙ
    if od:
        dstart = od[0]["date"]
        dend = od[-1]["date"]
    else:
        dstart = None
        dend = None
    if request.method == "POST":
        dstart = request.form["dstart"]
        dend = request.form["dend"]
        if dstart > dend:
            flash("Начальная дата не может быть позже конечной!")
        else:
            od = [x for x in od if x['date'] >= dstart and x['date'] <= dend]   # ПОЛУЧЕНИЕ ЗАПИСЕЙ СООТВЕТСТВУЮЩИХ ФИЛЬТРУ
        if "clear" in request.form:         # СБРОС ДАННЫХ В ФИЛЬТРАХ
            if '_flashes' in session:
                session['_flashes'].clear()
            return redirect('/')


    return render_template('index.html', db=od, dstart=dstart, dend=dend)

@app.route('/create', methods=["POST", "GET"])
def create():
    if request.method == "POST":
        if request.form["date"] < str(date.today()):
            flash("Нельзя сделать бронь на дату в прошлом!")
        elif request.form["tstart"] >= request.form["tend"]:
            flash("Начальное время не может быть позже конечного!")
        else:
            db.insert({"class": request.form["class"], "date": request.form["date"], "tstart": request.form["tstart"], "tend": request.form["tend"], "topic": request.form["topic"], "teacher": request.form["teacher"]})
            return redirect('/')

    return render_template('create.html')


@app.route('/delete/<int:id>')
def delete(id):
    db.remove(doc_ids=[id])
    return redirect('/')

@app.route('/edit/<int:id>', methods=["POST", "GET"])
def edit(id):
    item = db.get(doc_id=id)

    if request.method == "POST":
        if request.form["date"] < str(date.today()):
            flash("Нельзя сделать бронь на дату в прошлом!")
        elif request.form["tstart"] >= request.form["tend"]:
            flash("Начальное время не может быть позже конечного!")
        else:
            db.update({"class": request.form["class"], "date": request.form["date"], "tstart": request.form["tstart"], "tend": request.form["tend"], "topic": request.form["topic"], "teacher": request.form["teacher"]}, doc_ids=[id])
            return redirect('/')

    return render_template('edit.html', item=item)

if __name__ == '__main__':
    app.run()