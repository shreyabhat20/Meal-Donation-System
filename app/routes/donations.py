from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.models.models import db, User, FoodDonation, DonationRequest

donations_bp = Blueprint('donations', __name__)

@donations_bp.route('/filter_donations', methods=['GET'])
def filter_donations():
    if 'user_id' not in session or session['role'] != 'charity':
        flash("Unauthorized access.", "danger")
        return redirect(url_for('auth.login'))

    unique_cities = sorted([row[0] for row in db.session.query(FoodDonation.city).distinct()])
    hosts = User.query.filter_by(role="host").all()

    city = request.args.get('city')
    host_id = request.args.get('host_id')

    query = FoodDonation.query.filter_by(status="available")
    if city:
        query = query.filter_by(city=city)
    if host_id:
        query = query.filter_by(host_id=host_id)

    donations = query.all()
    return render_template('donations/donations.html', donations=donations, cities=unique_cities, hosts=hosts)

@donations_bp.route('/request_donation/<int:donation_id>', methods=['POST'])
def request_donation(donation_id):
    if session.get('role') == 'charity':
        donation = FoodDonation.query.get_or_404(donation_id)

        if donation.status != "available":
            flash("This donation is no longer available.", "danger")
            return redirect(url_for('dashboard.dashboard'))

        new_request = DonationRequest(charity_id=session['user_id'], donation_id=donation_id)
        donation.status = "requested"
        donation.charity_id = session['user_id']
        db.session.add(new_request)
        db.session.commit()

        flash('Donation request submitted!', 'success')
    else:
        flash("Unauthorized access.", "danger")
    return redirect(url_for('dashboard.dashboard'))

@donations_bp.route('/cancel_request', methods=['POST'])
def cancel_request():
    if session.get('role') == 'charity':
        donation_id = request.form.get('donation_id')
        donation = FoodDonation.query.get_or_404(donation_id)
        
        if donation.charity_id == session['user_id']:
            donation.status = "available"
            donation.charity_id = None
            DonationRequest.query.filter_by(donation_id=donation_id, charity_id=session['user_id']).delete()
            db.session.commit()
            flash('Request cancelled successfully!', 'success')
        else:
            flash("Unauthorized action.", "danger")
    return redirect(url_for('dashboard.dashboard'))

@donations_bp.route('/donations_history')
def history():
    if 'user_id' not in session:
        flash("Please log in to view the history.", "danger")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    role = session['role']

    if role == "host":
        donations = FoodDonation.query.filter_by(host_id=user_id).all()
    elif role == "charity":
        donations = db.session.query(
            FoodDonation, DonationRequest, User.username
        ).join(DonationRequest, FoodDonation.id == DonationRequest.donation_id)\
        .join(User, FoodDonation.host_id == User.id)\
        .filter(DonationRequest.charity_id == user_id).all()
    else:
        donations = []

    return render_template('donations/donations_history.html', donations=donations, role=role)