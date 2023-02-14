# //bin/env python
from flask import render_template, flash, redirect, url_for
from flask_mail import Message, Mail
 
mail = Mail()

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message(subject='Contact Form Submission',
                      recipients=['you@example.com'],
                      sender=form.email.data)
        msg.body = f"Name: {form.name.data}\n\nEmail: {form.email.data}\n\nMessage: {form.message.data}"
        mail.send(msg)
        flash('Your message has been sent!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

