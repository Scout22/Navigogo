#!/usr/bin/env python3
# coding: utf-8

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

from wtforms import validators

from database_interface import UserRecord, add_user
from download_attestation import check_user_id_and_token
from text_generator import success_email
from send_email import send_email


class ContactForm(FlaskForm):
    first_name = StringField("Prénom", [validators.DataRequired("Merci de remplir ce champ.")])
    last_name = StringField("Nom", [validators.DataRequired("Merci de remplir ce champ.")])
    email = StringField("Email", [validators.DataRequired("Merci de remplir ce champ."),
                                  validators.email("Addresse email invalide")])
    navigo_token = StringField("Cookie Navigo", [validators.DataRequired("Merci de remplir ce champ.")])
    navigo_id = IntegerField("Numéro d'attestation", [validators.DataRequired("Merci de remplir ce champ.")])
    submit = SubmitField("Valider")


app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/register', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            token_valid, user_id_valid = check_user_id_and_token(form.navigo_id.data, form.navigo_token.data)
            errors = False
            if not token_valid:
                form.navigo_token.errors.append("Token invalid")
                errors = True
            if not token_valid:
                form.navigo_id.errors.append("Numéro d'attestation invalid")
                errors = True
            if not errors:
                if not add_user(UserRecord(first_name=form.first_name.data, last_name=form.last_name.data,
                                           email=form.email.data, navigo_id=form.navigo_id.data,
                                           navigo_token=form.navigo_token.data, user_id=0)):
                    return render_template('/unexpected_error')
                body, subject = success_email()
                send_email(subject, body, [form.email.data])
                return render_template('success.html')
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
