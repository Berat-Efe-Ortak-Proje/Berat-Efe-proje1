from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from . import db
from .models import User, Club, Event, ClubRequest

# Blueprints
auth_bp = Blueprint('auth', __name__)
club_bp = Blueprint('club', __name__)
event_bp = Blueprint('event', __name__)
main_bp = Blueprint('main', __name__)

# Auth Routes
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Kullanıcı adı zaten kullanılıyor', 'danger')
            return redirect(url_for('auth.register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        
        flash('Kullanıcı adı veya şifre hatalı', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Main Routes
@main_bp.route('/')
def index():
    clubs = Club.query.all()
    return render_template('index.html', clubs=clubs)


@main_bp.route('/about')
def about():
    return render_template('about.html')


@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

@main_bp.route('/admin/users')
@login_required
def list_users():
    if current_user.role != 'admin':
        flash('Bu işlem için yönetici yetkisi gerekiyor.', 'danger')
        return redirect(url_for('main.index'))
    
    users = User.query.all()
    return render_template('admin_users.html', users=users)

# Club Routes
@club_bp.route('/clubs')
def list_clubs():
    clubs = Club.query.all()
    return render_template('clubs.html', clubs=clubs)

@club_bp.route('/club/create', methods=['GET', 'POST'])
@login_required
def create_club():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if current_user.role == 'admin':
            club = Club(name=name, description=description, president_id=current_user.id)
            db.session.add(club)
            db.session.commit()
            flash('Kulüp başarıyla oluşturuldu!', 'success')
        else:
            club_req = ClubRequest(name=name, description=description, user_id=current_user.id)
            db.session.add(club_req)
            db.session.commit()
            flash('Kulüp açma isteğiniz yöneticiye iletildi. Onaylandığında kulübünüz açılacaktır.', 'info')
        
        return redirect(url_for('club.list_clubs'))
    
    return render_template('create_club.html')

@club_bp.route('/admin/requests')
@login_required
def list_requests():
    if current_user.role != 'admin':
        flash('Yetkisiz erişim.', 'danger')
        return redirect(url_for('main.index'))
    
    requests = ClubRequest.query.filter_by(status='pending').all()
    return render_template('admin_requests.html', requests=requests)

@club_bp.route('/admin/request/<int:req_id>/<action>')
@login_required
def handle_request(req_id, action):
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
        
    req = ClubRequest.query.get_or_404(req_id)
    
    if action == 'approve':
        req.status = 'approved'
        # Create the club
        club = Club(name=req.name, description=req.description, president_id=req.user_id)
        db.session.add(club)
        flash(f'{req.name} kulübü onaylandı ve oluşturuldu.', 'success')
    elif action == 'reject':
        req.status = 'rejected'
        flash(f'{req.name} kulübü isteği reddedildi.', 'warning')
        
    db.session.commit()
    return redirect(url_for('club.list_requests'))

@club_bp.route('/club/<int:club_id>')
def view_club(club_id):
    club = Club.query.get_or_404(club_id)
    events = club.events
    return render_template('club_detail.html', club=club, events=events)

@club_bp.route('/club/<int:club_id>/join')
@login_required
def join_club(club_id):
    club = Club.query.get_or_404(club_id)
    if current_user not in club.members:
        club.members.append(current_user)
        db.session.commit()
        flash(f'{club.name} kulübüne başarıyla katıldınız!', 'success')
    else:
        flash(f'Zaten {club.name} kulübünün üyesisiniz.', 'info')
    return redirect(url_for('club.view_club', club_id=club_id))

@club_bp.route('/club/<int:club_id>/leave')
@login_required
def leave_club(club_id):
    club = Club.query.get_or_404(club_id)
    if current_user in club.members:
        club.members.remove(current_user)
        db.session.commit()
        flash(f'{club.name} kulübünden ayrıldınız.', 'warning')
    else:
        flash(f'{club.name} kulübünün üyesi değilsiniz.', 'info')
    return redirect(url_for('club.view_club', club_id=club_id))

@club_bp.route('/club/<int:club_id>/delete', methods=['POST'])
@login_required
def delete_club(club_id):
    if current_user.role != 'admin':
        flash('Bu işlem için yönetici yetkisi gerekiyor.', 'danger')
        return redirect(url_for('club.list_clubs'))
    
    club = Club.query.get_or_404(club_id)
    
    # Delete associated events first
    for event in club.events:
        db.session.delete(event)
        
    db.session.delete(club)
    db.session.commit()
    flash('Kulüp başarıyla silindi.', 'success')
    return redirect(url_for('club.list_clubs'))
    events = Event.query.filter_by(club_id=club_id).all()
    return render_template('club_detail.html', club=club, events=events)

# Event Routes
@event_bp.route('/event/create/<int:club_id>', methods=['GET', 'POST'])
@login_required
def create_event(club_id):
    if current_user.role != 'admin':
        flash('Bu işlem için yönetici yetkisi gerekiyor.', 'danger')
        return redirect(url_for('club.view_club', club_id=club_id))

    club = Club.query.get_or_404(club_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        date_str = request.form.get('date')
        location = request.form.get('location')
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Geçersiz tarih formatı.', 'danger')
            return redirect(url_for('event.create_event', club_id=club_id))

        event = Event(name=name, description=description, date=date, 
                     location=location, club_id=club_id)
        db.session.add(event)
        db.session.commit()
        
        flash('Etkinlik başarıyla oluşturuldu!', 'success')
        return redirect(url_for('club.view_club', club_id=club_id))
    
    return render_template('create_event.html', club=club)

@event_bp.route('/event/<int:event_id>')
def view_event(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event)
