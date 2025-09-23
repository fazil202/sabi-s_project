from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import os
from pdf_export import export_to_pdf

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/download_pdf', methods=['GET', 'POST'])
def download_pdf():
    if not is_logged_in():
        return redirect(url_for('login'))
    # Recreate seating plan from last upload (or store in session for production)
    # For demo, just use last processed seating_plan
    # You may want to store seating_plan in session for real use
    # Here, we assume seating_plan is passed from the form or session
    # For now, reprocess with last uploaded files
    upload_folder = 'uploads'
    student_csv = None
    room_csv = None
    for file in os.listdir(upload_folder):
        if file.endswith('.csv') and 'student' in file:
            student_csv = os.path.join(upload_folder, file)
        if file.endswith('.csv') and 'room' in file:
            room_csv = os.path.join(upload_folder, file)
    if not student_csv or not room_csv:
        flash('CSV files not found for PDF export.')
        return redirect(url_for('index'))
    students_per_desk = 1
    include_detained = False
    from seating import generate_seating_plan
    seating_plan, error = generate_seating_plan(student_csv, room_csv, students_per_desk, include_detained)
    if error:
        flash(error)
        return redirect(url_for('index'))
    pdf_path = export_to_pdf(seating_plan)
    return send_file(pdf_path, as_attachment=True)
app = Flask(__name__)
app.secret_key = 'your_secret_key'

def is_logged_in():
    return session.get('logged_in', False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logged out successfully.')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if not is_logged_in():
        return redirect(url_for('login'))
    if request.method == 'POST':
        student_file = request.files.get('student_csv')
        room_file = request.files.get('room_csv')
        students_per_desk = int(request.form.get('students_per_desk', 1))
        include_detained = request.form.get('include_detained', 'off') == 'on'
        if not student_file or not room_file:
            flash('Please upload both CSV files.')
            return redirect(url_for('index'))
        # Save files to uploads folder
        upload_folder = 'uploads'
        import os
        os.makedirs(upload_folder, exist_ok=True)
        student_path = os.path.join(upload_folder, student_file.filename)
        room_path = os.path.join(upload_folder, room_file.filename)
        student_file.save(student_path)
        room_file.save(room_path)
        from seating import generate_seating_plan
        seating_plan, error = generate_seating_plan(student_path, room_path, students_per_desk, include_detained)
        if error:
            flash(error)
            return redirect(url_for('index'))
        return render_template('seating_plan.html', seating_plan=seating_plan)
    return render_template('index.html')

if __name__ == '__main__':
    # Change host to your desired IP, e.g., '0.0.0.0' for all interfaces or your LAN IP
    app.run(host='0.0.0.0', port=5000, debug=True)
