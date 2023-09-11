from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, URL, NumberRange
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = ''
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps', validators=[DataRequired(), URL()])
    open_time = StringField('Opening time', validators=[DataRequired()])
    closing_time = StringField('Closing name', validators=[DataRequired()])
    coffee_rating = IntegerField('Coffee rating', validators=[DataRequired(), NumberRange(min=0, max=5)])
    wifi_rating = IntegerField('Wifi Strength', validators=[DataRequired(),NumberRange(min=0, max=5)])
    power_rating = IntegerField('Power Socket Ability', validators=[DataRequired(),NumberRange(min=0, max=5)])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if request.method == "POST" and form.validate_on_submit():
        # Get the form data
        cafe_name = f"{form.cafe.data}"
        location = f"{form.location.data}"
        open_time = f"{form.open_time.data}"
        close_time = f"{form.closing_time.data}"
        coffee = f"{form.coffee_rating.data}"
        wifi = f"{form.wifi_rating.data}"
        power = f"{form.power_rating.data}"

        # Open the CSV file in append mode and write the form data as a new row
        with open("cafe-data.csv", mode="a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([cafe_name, location, open_time, close_time, coffee, wifi, power])

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
