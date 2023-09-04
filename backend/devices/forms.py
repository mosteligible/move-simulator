from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class DeviceAddForm(FlaskForm):
    device_id = StringField("device_id", validators=[DataRequired()])
