from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    disc = db.Column(db.String(500), nullable=False)
    my_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}:{self.disc}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        disc = request.form['disc']

        todo = Todo(title=title, disc=disc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    print(alltodo)
    return render_template('index.html', alltodo=alltodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    dtodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(dtodo)
    db.session.commit()
    return redirect("/")
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/updates/<int:sno>',methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        disc=request.form['disc']
        utodo = Todo.query.filter_by(sno=sno).first()
        utodo.title=title
        utodo.disc=disc
        db.session.add(utodo)
        db.session.commit()
        return redirect("/")
    
    utodo = Todo.query.filter_by(sno=sno).first()
    return render_template('updates.html', utodo=utodo)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
