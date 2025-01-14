from flask import Flask, render_template, request, redirect, url_for, flash 
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = '1412KID'

UPLOAD_FOLDER = 'Subscription/static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

users = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def user_subscription():
    return render_template('user_subscription.html')

@app.route('/submit', methods=['POST'])
def submit_payment():
    if 'payment_proof' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['payment_proof']
    bank = request.form.get('bank')
    date = request.form.get('date')
    time = request.form.get('time')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        try:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            users.append({
                'bank': bank,
                'date': date,
                'time': time,
                'proof': filename,
                'approved': False
            })
            return redirect(url_for('success_page'))
        except Exception as e:
            flash(f"Error saving file: {e}")
            return redirect(url_for('user_subscription'))
        
        return redirect(url_for('user_subscription'))
    else:
        flash('Invalid file type. Only PNG, JPG, JPEG allowed.')
        return redirect(url_for('user_subscription'))
    
@app.route('/success')
def success_page():
    return render_template('success.html')

@app.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html', users=users)

@app.route('/approve/<int:user_id>', methods=['POST'])
def approve_user(user_id):
    if 0 <= user_id < len(users):
        users[user_id]['approved'] = True
        flash(f"User {users[user_id]} approved successfully!")
    return redirect(url_for('admin_dashboard'))

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)