from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.models.models import db, User, FoodDonation, DonationRequest
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session['role'] == 'host':
        donations = FoodDonation.query.filter_by(host_id=session['user_id']).all()
        return render_template('dashboard/dashboard.html', donations=donations)

    elif session['role'] == 'charity':
        donations = FoodDonation.query.filter_by(status="available").all()
        cities = [d.city for d in FoodDonation.query.distinct(FoodDonation.city)]
        hosts = User.query.filter_by(role="host").all()
        return render_template('donations/donations.html', donations=donations, hosts=hosts, cities=cities)

@dashboard_bp.route('/add_donation', methods=['POST'])
def add_donation():
    if session.get('role') == 'host':
        food_type = request.form['food_type']
        quantity = int(request.form['quantity'])  
        expiration_date_str = request.form['expiration_date']
        expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d").date()  
        city = request.form['city']

        new_donation = FoodDonation(
            host_id=session['user_id'],
            food_type=food_type,
            quantity=quantity,
            expiration_date=expiration_date,
            city=city
        )
        db.session.add(new_donation)
        db.session.commit()
        flash('Donation added successfully!', 'success')

    return redirect(url_for('dashboard.dashboard'))


@dashboard_bp.route('/update_status/<int:donation_id>', methods=['POST'])
def update_status(donation_id):
    if 'user_id' not in session:
        flash("Please log in to continue.", "danger")
        return redirect(url_for('auth.login'))

    if session.get('role') != 'host':
        flash("Unauthorized access.", "danger")
        return redirect(url_for('dashboard.dashboard'))

    donation = FoodDonation.query.get_or_404(donation_id)
    new_status = request.form.get('status')
    
    if new_status not in ['available', 'requested', 'donated']:
        flash("Invalid status.", "danger")
        return redirect(url_for('dashboard.dashboard'))

    if new_status == 'donated':
        db.session.delete(donation)
        db.session.commit()
    else:
        donation.status = new_status
        db.session.commit()

    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/delete_donation/<int:donation_id>', methods=['POST'])
def delete_donation(donation_id):
    if session.get('role') == 'host':
        donation = FoodDonation.query.get_or_404(donation_id)
        DonationRequest.query.filter_by(donation_id=donation_id).delete()
        db.session.delete(donation)
        db.session.commit()
        flash("Donation deleted successfully!", "success")
    else:
        flash("Unauthorized access.", "danger")
    return redirect(url_for('dashboard.dashboard'))

