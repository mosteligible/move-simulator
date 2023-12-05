from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class DeviceAddForm(FlaskForm):
    device_id = StringField("device_id", validators=[DataRequired()])
    user_name = StringField("user_id", validators=[DataRequired()])
