from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class RouteAddForm(FlaskForm):
    start_street_address = StringField("start_street_address", validators=[DataRequired()])
    start_city_name = StringField("start_city_name", validators=[DataRequired()])
    start_postal_code = StringField("start_postal_code")
    start_country_name = StringField("start_country_name", validators=[DataRequired()])
    stop_street_address = StringField("stop_street_address", validators=[DataRequired()])
    stop_city_name = StringField("stop_city_name", validators=[DataRequired()])
    stop_postal_code = StringField("stop_postal_code")
    stop_country_name = StringField("stop_country_name", validators=[DataRequired()])
