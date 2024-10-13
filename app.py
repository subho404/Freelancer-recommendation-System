from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from database import get_freelancers, add_freelancer, get_recommended_freelancers, add_project, projects_collection

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user-role', methods=['POST'])
def user_role():
    role = request.form['role']
    if role == 'freelancer':
        return render_template('add_freelancer.html')
    else:
        return render_template('add_project.html')

@app.route('/add-freelancer', methods=['POST'])
def add_freelancer_route():
    name = request.form['name']
    email = request.form['email']
    skills = request.form['skills']
    profile_picture = request.files['profile_picture']
    
    if profile_picture:
        filename = secure_filename(profile_picture.filename)
        profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        profile_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    else:
        profile_url = None

    add_freelancer(name, email, skills, profile_url)
    return redirect('/')

@app.route('/add-project', methods=['POST'])
def add_project_route():
    title = request.form['title']
    skills = request.form['skills']
    project_id = add_project(title, skills)  # Get the project_id when adding
    recommended_freelancers = get_recommended_freelancers(project_id)
    return render_template('recommendations.html', freelancers=recommended_freelancers)

@app.route('/recommend_freelancers', methods=['POST'])
def recommend_freelancers():
    project_id = request.form['project_id']
    recommended_freelancers = get_recommended_freelancers(project_id)
    return render_template('recommendations.html', freelancers=recommended_freelancers)

if __name__ == '__main__':
    app.run(debug=True)
