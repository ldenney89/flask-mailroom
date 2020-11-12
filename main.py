import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/creating', methods=['GET', 'POST'])
def creating():
    #TODO
    if request.method == 'POST':
        try:
            donor = request.form['donor']
            donation = int(request.form['donation'])
            try:
                #get donor with said name
                donor_record = Donor.select().where(Donor.name == donor).get()
                Donation(donor=donor_record, value=donation).save()
            except Donor.DoesNotExist:
                #if no donor
                print(donor)
                new_donor = Donor(name=donor)
                new_donor.save()
                new_donation=Donation(donor=new_donor, value=donation)
                new_donation.save()

            return redirect(url_for('home'))
        except ValueError:
            return render_template('creating.jinja2', error= "Please enter a valid donation amount.")

    else:
        return render_template('creating.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
