from wtforms import Form, StringField, TextAreaField, validators, EmailField


class ContactUs(Form):
    # validators.Regexp('[a-zA-Z][a-zA-Z ]+[a-zA-Z]$', message="Name must contain only letters and space")]
    name = StringField('Name',[validators.Length(min=1, max=50), validators.DataRequired(),validators.Regexp('[a-zA-Z][a-zA-Z ]+[a-zA-Z]$', message="Name must contain only letters and space")])
    email = EmailField('Email', [validators.Length(min=6, max=35), validators.DataRequired()])
    feedback = TextAreaField('Ask a Question',[validators.Optional()])