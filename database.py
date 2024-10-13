from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['freelancer_db']
freelancers_collection = db['freelancers']
projects_collection = db['projects']

# Function to add a freelancer
def add_freelancer(name, skills):
    freelancer = {
        "name": name,
        "skills": skills.split(',')
    }
    freelancers_collection.insert_one(freelancer)

# Function to get freelancers
def get_freelancers():
    return list(freelancers_collection.find({}))

# Function to add a project
def add_project(project_id, title, skills):
    project = {
        "_id": project_id,  # Use project_id as the unique identifier
        "title": title,
        "skills": skills.split(',')
    }
    projects_collection.insert_one(project)

# Function to get recommended freelancers based on project ID
def get_recommended_freelancers(project_id):
    project = projects_collection.find_one({"_id": project_id})
    if project:
        required_skills = project.get('skills', [])
        return list(freelancers_collection.find({"skills": {"$in": required_skills}}))
    return []
