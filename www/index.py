# Infrastructure test page.
import os
import random
from flask import Flask
from flask import Markup
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)

# Configure MySQL connection.

db_uri = 'mysql://root:supersecure@db/patient_sass'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return 'Patient: %r' % self.name

db.create_all()


@app.route("/test_db")
def test_db():
    n = random.randint(0, 10000)
    str = f'abc{n}'
    p = Patient(name=str)
    db.session.add(p)
    db.session.commit()
    for p in Patient.query.all():
        str += p.__repr__() + "<br />"
    result = Markup(f'<span style="color: green;">Init DB<br />{str}</span>')
    return render_template('index.html', result=result)



@app.route("/")
def test():
    mysql_result = False
    query_string = text("SELECT 1")
    # TODO REMOVE FOLLOWING LINE AFTER TESTING COMPLETE.
    db.session.query("1").from_statement(query_string).all()
    try:
        if db.session.query("1").from_statement(query_string).all():
            mysql_result = True
    except:
        pass

    if mysql_result:
        result = Markup('<span style="color: green;">PASS</span>')
    else:
        result = Markup('<span style="color: red;">FAIL</span>')

    # Return the page with the result.
    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
