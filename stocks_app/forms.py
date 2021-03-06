from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL
from stocks_app.models import User, Stock, MutualFund

class MutualFundForm(FlaskForm):
    """Form for creating a new mutual fund"""

    name = StringField('Fund Name', validators=[DataRequired()])
    desc = StringField('Description', validators=[DataRequired()])
    value = FloatField('Price per share $', validators=[DataRequired()])
    submit = SubmitField('Submit')

class StockForm(FlaskForm):
    """Form for creating a new stock"""

    name = StringField('Stock Name', validators=[DataRequired()])
    desc = StringField('Description', validators=[DataRequired()])
    value = FloatField('Price per share $', validators=[DataRequired()])
    mutual_fund = QuerySelectField('Mutual Fund (if any)', query_factory=lambda: MutualFund.query, allow_blank=True)
    submit = SubmitField('Submit')

class SignUpForm(FlaskForm):
    """Form for signing up"""

    username = StringField('User Name', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    """Form for logging in"""

    username = StringField('User Name', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class WatchForm(FlaskForm):
    submit = SubmitField('Add to Watch List')

class MutualFundForm2(FlaskForm):
    mutual_fund = QuerySelectField('Mutual Fund', query_factory=lambda: MutualFund.query, allow_blank=False)
    submit = SubmitField('Add to Mutual Fund')