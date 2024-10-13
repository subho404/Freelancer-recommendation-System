from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['freelancer_db']
freelancers_collection = db['freelancers']
projects_collection = db['projects']

def add_freelancer(name, email, skills, profile_url):
    freelancer = {
        "name": name,
        "email": email,
        "skills": skills.split(','),
        "profile_url": profile_url
    }
    freelancers_collection.insert_one(freelancer)

def get_freelancers():
    return list(freelancers_collection.find({}))

def add_project(title, skills):
    project_id = f"project-{projects_collection.count_documents({}) + 1}"
    project = {
        "_id": project_id,
        "title": title,
        "skills": skills.split(',')
    }
    projects_collection.insert_one(project)
    return project_id  # Return the project_id after adding

def get_recommended_freelancers(project_id):
    project = projects_collection.find_one({"_id": project_id})
    if project:
        required_skills = project.get('skills', [])
        return list(freelancers_collection.find({"skills": {"$in": required_skills}}))
    return []
