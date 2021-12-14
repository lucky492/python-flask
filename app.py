from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class user(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(200), nullable=True)
    desc = db.Column(db.String(500), nullable=True)
    date_time = db.Column(db.DateTime , default=datetime.utcnow)

    def __repr__(self):
        return f"{self.id} {self.title} {self.todo} {self.date_created}"

@app.route('/', methods = ['GET','POST'])
def hello_world():
    if request.method=='POST':
        print("post","-",request.form['todo'],request.form['desc'])
        todo = request.form['todo']
        desc = request.form['desc']

        todo =user(todo=todo,desc=desc)
        db.session.add(todo)
        db.session.commit()

    # retrive data from database and store it in todo
    todo = user.query.all()
    return render_template('index.html',todo=todo)


# @app.route('/show')
# def hello():
#     return "hello world.This is second route of this page."


@app.route('/update/<int:sno>' , methods = ['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['todo']
        desc = request.form['desc']
        print("3 now--", title, "-AND-", desc)

        update = user.query.filter_by(sno=sno).first()
        print("1 access- ",update.todo , "-AND-", update.desc)
        update.todo = title
        update.desc = desc
        print("2 NOW --- ",title , "-AND-" , desc)
        db.session.add(update)
        db.session.commit()

        return redirect("/")


    todo = user.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)


# our delete value will take an integer.In documentation we will see how to delete.
@app.route('/delete/<int:sno>')
def delete(sno):
    todo = user.query.filter_by(sno=sno).first()
    print("delete - ",todo.todo,"&",todo.desc)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)