from database import create_connection

# Function to recommend projects based on freelancer's skills
def recommend_projects(freelancer_id):
    conn = create_connection()
    cursor = conn.cursor()

    # Fetch the freelancer's skills
    cursor.execute("SELECT skills FROM freelancers WHERE id=?", (freelancer_id,))
    freelancer = cursor.fetchone()
    
    if not freelancer:
        return []

    freelancer_skills = set(freelancer[0].split(','))

    # Fetch all projects and their required skills
    cursor.execute("SELECT id, title, skills FROM projects")
    projects = cursor.fetchall()

    # Score projects based on skill match
    recommendations = []
    for project in projects:
        project_id, title, project_skills = project
        project_skills_set = set(project_skills.split(','))

        # Calculate skill overlap
        skill_match = len(freelancer_skills & project_skills_set)

        if skill_match > 0:
            recommendations.append((project_id, title, skill_match))

    # Sort recommendations by best match
    recommendations.sort(key=lambda x: x[2], reverse=True)
    
    return [(rec[0], rec[1]) for rec in recommendations]

# Function to recommend freelancers for a project
def recommend_freelancers(project_id):
    conn = create_connection()
    cursor = conn.cursor()

    # Fetch the project's required skills
    cursor.execute("SELECT skills FROM projects WHERE id=?", (project_id,))
    project = cursor.fetchone()

    if not project:
        return []

    project_skills = set(project[0].split(','))

    # Fetch all freelancers and their skills
    cursor.execute("SELECT id, name, skills FROM freelancers")
    freelancers = cursor.fetchall()

    # Score freelancers based on skill match
    recommendations = []
    for freelancer in freelancers:
        freelancer_id, name, freelancer_skills = freelancer
        freelancer_skills_set = set(freelancer_skills.split(','))

        # Calculate skill overlap
        skill_match = len(freelancer_skills_set & project_skills)

        if skill_match > 0:
            recommendations.append((freelancer_id, name, skill_match))

    # Sort recommendations by best match
    recommendations.sort(key=lambda x: x[2], reverse=True)
    
    return [(rec[0], rec[1]) for rec in recommendations]
