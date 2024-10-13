from flask import Flask, render_template, request, redirect
from database import get_freelancers, add_freelancer, get_recommended_freelancers, add_project, projects_collection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user-role', methods=['POST'])
def user_role():
    role = request.form['role']
    if role == 'freelancer':
        return render_template('add_freelancer.html')  # Redirect to freelancer registration page
    else:
        return render_template('add_project.html')  # Redirect to project addition page

@app.route('/add-freelancer', methods=['POST'])
def add_freelancer_route():
    name = request.form['name']
    skills = request.form['skills']
    add_freelancer(name, skills)
    return redirect('/')

@app.route('/add-project', methods=['POST'])
def add_project_route():
    title = request.form['title']
    skills = request.form['skills']
    
    # Generate a unique project ID (incremental ID)
    project_id = f"project-{projects_collection.count_documents({}) + 1}"
    
    # Add the project to the database
    add_project(project_id, title, skills)
    
    # Automatically recommend freelancers for this project
    recommended_freelancers = get_recommended_freelancers(project_id)

    # Render the recommendations page with the new freelancers
    return render_template('recommendations.html', freelancers=recommended_freelancers)

@app.route('/recommend_freelancers', methods=['POST'])
def recommend_freelancers():
    project_id = request.form['project_id']
    recommended_freelancers = get_recommended_freelancers(project_id)
    return render_template('recommendations.html', freelancers=recommended_freelancers)

if __name__ == '__main__':
    app.run(debug=True)
