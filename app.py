from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from ml_model import recommend_freelancers
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# MongoDB Setup
client = MongoClient('mongodb://localhost:27017/')
db = client['freelancer_db']
freelancers_collection = db['freelancers']
projects_collection = db['projects']

@app.route('/')
def home():
    return redirect(url_for('user_role'))

@app.route('/user-role', methods=['GET', 'POST'])
def user_role():
    if request.method == 'POST':
        role = request.form['role']
        if role == 'freelancer':
            return redirect(url_for('add_freelancer_route'))
        else:
            return redirect(url_for('add_project_route'))
    return render_template('user_role.html')

@app.route('/add_freelancer', methods=['GET', 'POST'])
def add_freelancer_route():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        skills = request.form['skills'].split(',')
        experience_level = request.form['experience_level']
        profile_picture = request.files['profile_picture']

        freelancer = {
            'name': name,
            'email': email,
            'skills': [skill.strip() for skill in skills],
            'experience_level': experience_level,
            'profile_url': f"/static/uploads/{profile_picture.filename}"
        }

        
        profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_picture.filename))
        freelancers_collection.insert_one(freelancer)

        return redirect(url_for('home'))
    return render_template('add_freelancer.html')

@app.route('/add_project', methods=['GET', 'POST'])
def add_project_route():
    if request.method == 'POST':
        title = request.form['title']
        skills = request.form['skills'].split(',')

        project_id = f"project-{projects_collection.count_documents({}) + 1}"
        new_project = {
            'project_id': project_id,
            'title': title,
            'skills': [skill.strip() for skill in skills]
        }

        projects_collection.insert_one(new_project)

        
        freelancers = list(freelancers_collection.find({}))

       
        recommended_freelancers = recommend_freelancers(freelancers, new_project['skills'])

        if recommended_freelancers:
            top_freelancer = recommended_freelancers[0] 
            other_freelancers = recommended_freelancers[1:]  
        else:
            top_freelancer = None
            other_freelancers = []

        return render_template('recommendations.html', top_freelancer=top_freelancer, other_freelancers=other_freelancers, project_title=title)

    return render_template('add_project.html')


@app.route('/contact-freelancer', methods=['POST'])
def contact_freelancer_route():
    freelancer_email = request.form['freelancer_email']
    project_title = request.form['project_title']
    message = request.form['message']

    
    print(f"Contacting {freelancer_email} regarding project {project_title} with message: {message}")

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
