from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.utils.pdf_export import export_to_pdf
from datetime import datetime
import logging
from functools import wraps

app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')
app.secret_key = 'your_secret_key_change_this_in_production'

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Global database instance
db = None

def init_database():
    """Initialize database connection"""
    global db
    try:
        from backend.models.database import Database
        db = Database()
        if db.connect():
            db.create_tables()
            return True
        else:
            print("Failed to connect to database. Using fallback authentication.")
            return False
    except Exception as e:
        print(f"Database initialization error: {e}")
        print("Using fallback authentication.")
        return False

def is_logged_in():
    return session.get('logged_in', False)

def get_user_role():
    return session.get('role', 'student')

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def require_role(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not is_logged_in():
                return redirect(url_for('login'))
            if get_user_role() != required_role and get_user_role() != 'admin':
                flash('Access denied. Insufficient permissions.')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def fallback_auth(username, password):
    """Fallback authentication when database is not available"""
    return username == 'admin' and password == 'admin123'

def get_client_ip():
    """Get client IP address"""
    return request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

def get_user_agent():
    """Get user agent"""
    return request.headers.get('User-Agent', '')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        role = request.form.get('role', 'student')  # Default to student
        
        # Validation
        if not all([username, email, password, confirm_password, full_name]):
            flash('All fields are required.')
            return redirect(url_for('signup'))
        
        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('signup'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.')
            return redirect(url_for('signup'))
        
        # Try to create user in database
        if db and db.connection and db.connection.is_connected():
            success, message = db.create_user(username, email, password, full_name, role)
            if success:
                flash('Account created successfully! Please login.')
                return redirect(url_for('login'))
            else:
                flash(message)
                return redirect(url_for('signup'))
        else:
            flash('Database not available. Please contact administrator.')
            return redirect(url_for('signup'))
    
    return render_template('signup/signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Try database authentication first
        if db and db.connection and db.connection.is_connected():
            user = db.authenticate_user(username, password)
            if user:
                # Handle both tuple and dictionary formats
                if isinstance(user, tuple):
                    # Assuming tuple format: (id, username, email, full_name, role, ...)
                    user_id, user_name, email, full_name, role = user[:5]
                    session['logged_in'] = True
                    session['user_id'] = user_id
                    session['username'] = user_name
                    session['full_name'] = user_name
                    session['role'] = role
                elif isinstance(user, dict):
                    # Dictionary format
                    session['logged_in'] = True
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['full_name'] = user['full_name']
                    session['role'] = user['role']
                
                # Log successful login
                if db:
                    db.log_activity(session['user_id'], 'LOGIN', f"User {username} logged in", get_client_ip(), get_user_agent())
                
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials.')
                return redirect(url_for('login'))
        else:
            # Fallback authentication
            if fallback_auth(username, password):
                session['logged_in'] = True
                session['user_id'] = 1  # Default admin ID
                session['username'] = username
                session['full_name'] = 'Administrator'
                session['role'] = 'admin'
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials.')
                return redirect(url_for('login'))
    
    return render_template('login/login.html')

@app.route('/logout')
def logout():
    # Log logout activity
    if db and session.get('user_id'):
        db.log_activity(session.get('user_id'), 'LOGOUT', f"User {session.get('username')} logged out")
    
    session.clear()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

@app.route('/dashboard')
@require_login
def dashboard():
    user_role = get_user_role()
    stats = {}
    
    if db and db.connection and db.connection.is_connected():
        user_id = session.get('user_id')
        
        # Get user's PDF history count
        pdf_history = db.get_user_pdf_history(user_id)
        stats['total_pdfs'] = len(pdf_history)
        
        # Get recent activity
        recent_activity = db.get_activity_logs(user_id, 5)
        stats['recent_activity'] = recent_activity
        
        # Admin-specific stats
        if user_role == 'admin':
            all_users = db.get_users_by_role()
            stats['total_users'] = len(all_users)
            stats['admin_count'] = len([u for u in all_users if u['role'] == 'admin'])
            stats['faculty_count'] = len([u for u in all_users if u['role'] == 'faculty'])
            stats['student_count'] = len([u for u in all_users if u['role'] == 'student'])
    
    return render_template('dashboard/dashboard.html', stats=stats, user_role=user_role)

@app.route('/settings', methods=['GET', 'POST'])
@require_login
def settings():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'change_password':
            old_password = request.form.get('old_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if new_password != confirm_password:
                flash('New passwords do not match.')
                return redirect(url_for('settings'))
            
            if db and db.connection and db.connection.is_connected():
                user_id = session.get('user_id')
                success, message = db.change_password(user_id, old_password, new_password)
                flash(message)
            else:
                flash('Database not available.')
            
            return redirect(url_for('settings'))
        
        elif action == 'update_system_settings' and get_user_role() == 'admin':
            # Update system settings
            settings_to_update = [
                'students_per_desk', 'include_detained', 'default_building',
                'session_timeout', 'max_login_attempts', 'email_notifications',
                'password_min_length', 'pdf_retention_days'
            ]
            
            if db and db.connection and db.connection.is_connected():
                user_id = session.get('user_id')
                for setting in settings_to_update:
                    value = request.form.get(setting)
                    if value is not None:
                        db.update_setting(setting, value, user_id)
                
                flash('System settings updated successfully.')
            else:
                flash('Database not available.')
            
            return redirect(url_for('settings'))
    
    # Get current settings
    current_settings = {}
    if db and db.connection and db.connection.is_connected():
        settings_keys = [
            'students_per_desk', 'include_detained', 'default_building',
            'session_timeout', 'max_login_attempts', 'email_notifications',
            'password_min_length', 'pdf_retention_days'
        ]
        
        for key in settings_keys:
            current_settings[key] = db.get_setting(key, '')
    
    return render_template('settings/settings.html', current_settings=current_settings, user_role=get_user_role())

@app.route('/admin')
@require_role('admin')
def admin_panel():
    if not db or not db.connection or not db.connection.is_connected():
        flash('Database not available.')
        return redirect(url_for('dashboard'))
    
    # Get all users
    all_users = db.get_users_by_role()
    
    # Get recent activity logs
    recent_logs = db.get_activity_logs(limit=20)
    
    return render_template('admin/admin.html', users=all_users, recent_logs=recent_logs)

@app.route('/admin/users')
@require_role('admin')
def manage_users():
    if not db or not db.connection or not db.connection.is_connected():
        flash('Database not available.')
        return redirect(url_for('dashboard'))
    
    all_users = db.get_users_by_role()
    return render_template('manage_users.html', users=all_users)

@app.route('/admin/update_role', methods=['POST'])
@require_role('admin')
def update_user_role():
    if not db or not db.connection or not db.connection.is_connected():
        flash('Database not available.')
        return redirect(url_for('admin_panel'))
    
    user_id = request.form.get('user_id')
    new_role = request.form.get('new_role')
    
    if user_id and new_role in ['admin', 'faculty', 'student']:
        updated_by = session.get('user_id')
        success = db.update_user_role(user_id, new_role, updated_by)
        
        if success:
            flash(f'User role updated to {new_role} successfully.')
        else:
            flash('Failed to update user role.')
    else:
        flash('Invalid user or role.')
    
    return redirect(url_for('manage_users'))

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        
        if db and db.connection and db.connection.is_connected():
            success, result = db.create_password_reset_token(email)
            
            if success:
                # In a real application, you would send an email with the reset link
                # For now, we'll just show a success message
                flash('If the email exists, a password reset link has been sent.')
                
                # Log the password reset request
                db.log_activity(None, 'PASSWORD_RESET_REQUEST', f"Password reset requested for email: {email}")
            else:
                flash('If the email exists, a password reset link has been sent.')
        else:
            flash('Database not available.')
        
        return redirect(url_for('login'))
    
    return render_template('reset password/reset_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_with_token(token):
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('reset_password_with_token', token=token))
        
        if db and db.connection and db.connection.is_connected():
            success, message = db.reset_password_with_token(token, new_password)
            flash(message)
            
            if success:
                return redirect(url_for('login'))
        else:
            flash('Database not available.')
        
        return redirect(url_for('reset_password_with_token', token=token))
    
    return render_template('reset password/reset_password_form.html', token=token)

@app.route('/pdf_history', methods=['GET', 'POST'])
@require_login
def pdf_history():
    if not db or not db.connection or not db.connection.is_connected():
        flash('Database not available.')
        return redirect(url_for('dashboard'))
    
    try:
        # Ensure tables are properly created/updated
        db.create_tables()
        
        # Get PDF history from database
        user_id = session.get('user_id')
        pdf_history_data = db.get_user_pdf_history(user_id)
        
        # Calculate stats
        total_students = sum(pdf.get('student_count', 0) for pdf in pdf_history_data)
        total_rooms = sum(pdf.get('room_count', 0) for pdf in pdf_history_data)
        
        # Log activity
        db.log_activity(user_id, 'PDF_HISTORY_VIEW', "User viewed PDF history")
        
        return render_template('pdf history/pdf_history.html',
                             pdf_history=pdf_history_data,
                             total_students=total_students,
                             total_rooms=total_rooms)
    
    except Exception as e:
        app.logger.error(f"Error fetching PDF history: {e}")
        print(f"Error fetching PDF history: {e}")  # Also print to console
        flash('Error loading PDF history. Please try again.')
        return redirect(url_for('dashboard'))

@app.route('/download_history_pdf/<int:pdf_id>')
@require_login
def download_history_pdf(pdf_id):
    if not db or not db.connection or not db.connection.is_connected():
        flash('Database not available.')
        return redirect(url_for('pdf_history'))
    
    try:
        user_id = session.get('user_id')
        file_path = db.get_pdf_file_path(pdf_id, user_id)
        
        if file_path and os.path.exists(file_path):
            # Log download activity
            db.log_activity(user_id, 'PDF_DOWNLOAD', f"Downloaded PDF ID: {pdf_id}")
            return send_file(file_path, as_attachment=True)
        else:
            flash('PDF file not found.')
            return redirect(url_for('pdf_history'))
    
    except Exception as e:
        app.logger.error(f"Error downloading PDF {pdf_id}: {e}")
        flash('Error downloading PDF file.')
        return redirect(url_for('pdf_history'))

@app.route('/', methods=['GET', 'POST'])
@require_login
def index():
    return redirect(url_for('dashboard'))

@app.route('/generate_plan', methods=['GET', 'POST'])
@require_login
def generate_plan():
    if request.method == 'POST':
        student_file = request.files.get('student_csv')
        room_file = request.files.get('room_csv')
        students_per_desk = int(request.form.get('students_per_desk', 1))
        include_detained = request.form.get('include_detained', 'off') == 'on'
        building = request.form.get('building', 'Main Building')
        
        if not student_file or not room_file:
            flash('Please upload both CSV files.')
            return redirect(url_for('generate_plan'))
        
        # Save files to uploads folder
        upload_folder = '../data/uploads'
        os.makedirs(upload_folder, exist_ok=True)
        
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        student_filename = f"students_{timestamp}_{student_file.filename}"
        room_filename = f"rooms_{timestamp}_{room_file.filename}"
        
        student_path = os.path.join(upload_folder, student_filename)
        room_path = os.path.join(upload_folder, room_filename)
        student_file.save(student_path)
        room_file.save(room_path)
        
        # Store file paths in session for PDF generation
        session['last_student_file'] = student_path
        session['last_room_file'] = room_path
        session['last_students_per_desk'] = students_per_desk
        session['last_include_detained'] = include_detained
        session['last_building'] = building

        # Import students into the database
        if db and db.connection and db.connection.is_connected():
            inserted = db.import_students_from_csv(student_path)
            print(f"Imported {inserted} students from CSV into the database.")
        
        from backend.utils.seating import generate_seating_plan
        seating_plan, unseated_students, error = generate_seating_plan(student_path, room_path, students_per_desk, include_detained)
        
        if error:
            flash(error)
            return redirect(url_for('generate_plan'))
        
        # Log activity
        if db and db.connection and db.connection.is_connected():
            user_id = session.get('user_id')
            student_count = sum(
                sum(1 for seat in row if seat is not None)
                for room in seating_plan
                for row in room.get('seats', [])
            )
            room_count = len(seating_plan)
            db.log_activity(user_id, 'SEATING_PLAN_GENERATED', 
                          f"Generated seating plan with {student_count} students in {room_count} rooms")
        
        return render_template('seating plan/seating_plan.html', seating_plan=seating_plan, unseated_students=unseated_students, building=building)
    
    # Get default settings
    default_settings = {}
    if db and db.connection and db.connection.is_connected():
        default_settings['students_per_desk'] = int(db.get_setting('students_per_desk', '1'))
        default_settings['include_detained'] = db.get_setting('include_detained', 'false') == 'true'
        default_settings['default_building'] = db.get_setting('default_building', 'Main Building')
    
    return render_template('generate plan/generate_plan.html', default_settings=default_settings)

@app.route('/download_pdf', methods=['GET', 'POST'])
@require_login
def download_pdf():
    # Get the last uploaded files from session
    student_csv = session.get('last_student_file')
    room_csv = session.get('last_room_file')
    students_per_desk = session.get('last_students_per_desk', 1)
    include_detained = session.get('last_include_detained', False)
    building = session.get('last_building', 'Main Building')
    
    if not student_csv or not room_csv:
        flash('No files found for PDF export. Please upload CSV files first.')
        return redirect(url_for('generate_plan'))
    
    if not os.path.exists(student_csv) or not os.path.exists(room_csv):
        flash('CSV files not found for PDF export. Please upload files again.')
        return redirect(url_for('generate_plan'))
    
    from backend.utils.seating import generate_seating_plan
    seating_plan, unseated_students, error = generate_seating_plan(student_csv, room_csv, students_per_desk, include_detained)
    
    if error:
        flash(f'Error generating seating plan: {error}')
        return redirect(url_for('generate_plan'))
    
    try:
        # Use absolute path for pdf_folder
        base_dir = os.path.abspath(os.path.dirname(__file__))
        pdf_folder = os.path.join(base_dir, '..', 'data', 'pdfs')
        pdf_folder = os.path.abspath(pdf_folder)
        os.makedirs(pdf_folder, exist_ok=True)

        # Generate PDF with unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = f"seating_plan_{timestamp}.pdf"

        pdf_path = export_to_pdf(seating_plan, pdf_filename, pdf_folder)

        # Save to database if available
        if db and db.connection and db.connection.is_connected():
            user_id = session.get('user_id')

            # Count students and rooms
            student_count = sum(
                sum(1 for seat in row if seat is not None)
                for room in seating_plan
                for row in room.get('seats', [])
            )
            room_count = len(seating_plan)

            db.save_pdf_history(
                user_id, pdf_filename, pdf_path, 
                student_count, room_count, 
                students_per_desk, include_detained, building
            )

        # Send email notification after PDF generation
        email_results = []
        # Get faculty users - fixed method call
        if db and db.connection and db.connection.is_connected():
            all_users = db.get_users_by_role()
            faculty_users = [user for user in all_users if user.get('role') == 'faculty']
            recipients = [user['email'] for user in faculty_users]
            
            for email in recipients:
                subject = "Exam Seating Plan"
                body = f"""
                <h2>Exam Seating Plan</h2>
                <p>Please find attached the exam seating plan generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.</p>
                <p>Best regards,<br>Exam Management System</p>
                """
                success, error_msg = db.send_email(email, subject, body)
                if success:
                    db.log_activity(user_id, 'EMAIL_SENT', f"Seating plan sent to {email}")
                    email_results.append(f"Email sent to {email}")
                else:
                    email_results.append(f"Failed to send email to {email}: {error_msg}")
        
        if email_results:
            for msg in email_results:
                flash(msg)
        else:
            flash('No recipients found for email notifications.')
            
        return send_file(pdf_path, as_attachment=True, download_name=pdf_filename)
        
    except Exception as e:
        app.logger.error(f"Error generating PDF: {str(e)}")
        flash(f'Error generating PDF: {str(e)}')
        return redirect(url_for('generate_plan'))

@app.route('/send_email_notifications', methods=['POST'])
@require_login
def send_email_notifications():
    if not db or not db.connection or not db.connection.is_connected():
        flash('Database not available.')
        return redirect(url_for('pdf_history'))
    
    try:
        pdf_id = request.form.get('pdf_id')
        recipient_type = request.form.get('recipient_type')
        
        if not pdf_id or not recipient_type:
            flash('Invalid request parameters.')
            return redirect(url_for('pdf_history'))
        
        # Get PDF details
        user_id = session.get('user_id')
        pdf_path = db.get_pdf_file_path(pdf_id, user_id)
        
        if not pdf_path or not os.path.exists(pdf_path):
            flash('PDF file not found.')
            return redirect(url_for('pdf_history'))
        
        # Get email addresses based on recipient type
        recipients = []
        
        # First try to get emails from CSV files (session or sample)
        csv_emails = []
        
        # Try session stored file first
        last_student_file = session.get('last_student_file')
        if last_student_file:
            csv_emails = db.get_student_emails_from_session_file(last_student_file)
            app.logger.info(f"Found {len(csv_emails)} emails from session file: {last_student_file}")
        
        # If no session file or no emails found, try sample file
        if not csv_emails:
            sample_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'samples', 'sample_students.csv')
            sample_file_path = os.path.abspath(sample_file_path)
            
            if os.path.exists(sample_file_path):
                csv_emails = db.get_emails_from_csv_data(sample_file_path)
                app.logger.info(f"Found {len(csv_emails)} emails from sample file: {sample_file_path}")
            else:
                app.logger.warning(f"Sample file not found: {sample_file_path}")
        
        if recipient_type == 'students':
            # Try database first, then CSV
            db_emails = db.get_all_emails_by_role('student')
            if db_emails:
                recipients = db_emails
                app.logger.info(f"Using {len(db_emails)} database student emails")
            else:
                recipients = csv_emails
                app.logger.info(f"Using {len(csv_emails)} CSV student emails")
                
        elif recipient_type == 'faculty':
            # Only use database for faculty
            recipients = db.get_all_emails_by_role('faculty')
            app.logger.info(f"Using {len(recipients)} database faculty emails")
            
        elif recipient_type == 'both':
            # Get students from CSV or database
            student_emails = db.get_all_emails_by_role('student')
            if not student_emails:
                student_emails = csv_emails
                
            # Get faculty from database only
            faculty_emails = db.get_all_emails_by_role('faculty')
            recipients = student_emails + faculty_emails
            
            app.logger.info(f"Using {len(student_emails)} student + {len(faculty_emails)} faculty emails")
        
        # Remove duplicates and filter empty emails
        recipients = list(set([email for email in recipients if email and email.strip() and '@' in email]))
        
        # Debug logging
        app.logger.info(f"Recipient type: {recipient_type}")
        app.logger.info(f"Final recipients ({len(recipients)}): {recipients}")
        
        if not recipients:
            error_msg = f'No email addresses found for {recipient_type}.'
            if recipient_type == 'students':
                error_msg += ' Ensure your CSV file has an "email" column with valid email addresses.'
            else:
                error_msg += ' Ensure database has users with the appropriate role.'
            
            flash(error_msg)
            return redirect(url_for('pdf_history'))
        
        # Send emails (simulated)
        success_count = 0
        error_count = 0
        
        for email in recipients:
            subject = "Exam Seating Plan Notification"
            body = f"""
            <h2>Exam Seating Plan</h2>
            <p>Dear Student/Faculty,</p>
            <p>Please find the exam seating plan generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.</p>
            <p>Please review the seating arrangement and contact the administration if you have any questions.</p>
            <p>Best regards,<br>Exam Management System</p>
            """
            
            success, error_msg = db.send_email(email, subject, body, pdf_path=pdf_path)
            
            if success:
                success_count += 1
                db.log_activity(user_id, 'EMAIL_SENT', f"Seating plan sent to {email}")
            else:
                error_count += 1
                app.logger.error(f"Failed to send email to {email}: {error_msg}")
        
        # Provide feedback to user
        if success_count > 0:
            flash(f'Successfully sent {success_count} email notification(s) to: {", ".join(recipients[:3])}{"..." if len(recipients) > 3 else ""}')
        
        if success_count == 0:
            flash('No emails could be sent. Please check the logs.')
            
    except Exception as e:
        app.logger.error(f"Error in send_email_notifications: {e}")
        flash(f'Error sending email notifications: {str(e)}')
    
    return redirect(url_for('pdf_history'))

# Add debug route to check CSV emails
@app.route('/debug/csv_emails')
@require_login
def debug_csv_emails():
    """Debug route to check CSV email extraction"""
    try:
        results = {}
        
        # Check session file
        last_student_file = session.get('last_student_file')
        if last_student_file:
            session_emails = db.get_student_emails_from_session_file(last_student_file)
            results['session_file'] = last_student_file
            results['session_emails'] = session_emails
        else:
            results['session_file'] = 'None'
            results['session_emails'] = []
        
        # Check sample file
        sample_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'samples', 'sample_students.csv')
        sample_file_path = os.path.abspath(sample_file_path)
        
        if os.path.exists(sample_file_path):
            sample_emails = db.get_emails_from_csv_data(sample_file_path)
            results['sample_file'] = sample_file_path
            results['sample_emails'] = sample_emails
        else:
            results['sample_file'] = f'Not found: {sample_file_path}'
            results['sample_emails'] = []
        
        # Check database emails
        db_student_emails = db.get_all_emails_by_role('student')
        db_faculty_emails = db.get_all_emails_by_role('faculty')
        
        results['db_student_emails'] = db_student_emails
        results['db_faculty_emails'] = db_faculty_emails
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)})

# ...existing code...

if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Log application startup information
    print("=" * 60)
    print("🚀 EXAM SEATING PLAN GENERATOR - STARTING UP")
    print("=" * 60)
    print(f"📍 Application URL: http://localhost:5000")
    print(f"📍 Local Network URL: http://0.0.0.0:5000")
    print(f"🔧 Debug Mode: Enabled")
    print(f"📁 Project Directory: {os.getcwd()}")
    print("=" * 60)
    print("🌐 Available Routes:")
    print("   • Login: http://localhost:5000/login")
    print("   • Signup: http://localhost:5000/signup")
    print("   • Dashboard: http://localhost:5000/dashboard")
    print("   • Admin Panel: http://localhost:5000/admin")
    print("=" * 60)
    
    # Change host to your desired IP, e.g., '0.0.0.0' for all interfaces or your LAN IP
    app.run(host='0.0.0.0', port=5000, debug=True)
