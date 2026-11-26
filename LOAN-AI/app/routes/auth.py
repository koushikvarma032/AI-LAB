from datetime import datetime
from decimal import Decimal
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.utils.extensions import db
from app.models.user import User
from app.utils.validators import validate_pan, validate_aadhaar

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        phone = request.form.get("phone", "").strip()

        if not username or not email or not password:
            flash("Username, email, and password are required.", "danger")
            return render_template("auth/register.html")

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Username or email already exists.", "warning")
            return render_template("auth/register.html")

        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role="customer"
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    
    if request.method == "POST":
        identifier = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier.lower())
        ).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f"Welcome back, {user.full_name}!", "success")
            next_page = request.args.get("next")
            if user.role == "admin":
                return redirect(next_page or url_for("admin.dashboard"))
            return redirect(next_page or url_for("main.dashboard"))
        
        flash("Invalid username or password.", "danger")

    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been signed out.", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        current_user.first_name = request.form.get("first_name", "").strip()
        current_user.last_name = request.form.get("last_name", "").strip()
        current_user.phone = request.form.get("phone", "").strip()
        
        pan = request.form.get("pan_number", "").strip().upper()
        if pan:
            if not validate_pan(pan):
                flash("Invalid PAN card format (e.g., ABCDE1234F).", "warning")
                return render_template("auth/profile.html")
            current_user.pan_number = pan

        aadhaar = request.form.get("aadhaar_number", "").strip()
        if aadhaar:
            if not validate_aadhaar(aadhaar):
                flash("Invalid Aadhaar format (must be 12 numeric digits).", "warning")
                return render_template("auth/profile.html")
            current_user.aadhaar_number = "".join(aadhaar.split())

        dob_str = request.form.get("date_of_birth")
        if dob_str:
            try:
                current_user.date_of_birth = datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                pass

        try:
            current_user.monthly_income = Decimal(request.form.get("monthly_income") or "0")
            current_user.current_obligations = Decimal(request.form.get("current_obligations") or "0")
        except Exception:
            pass

        db.session.commit()
        flash("Profile information updated successfully.", "success")
        return redirect(url_for("auth.profile"))

    return render_template("auth/profile.html")
