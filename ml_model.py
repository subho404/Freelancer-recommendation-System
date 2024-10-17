from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_skills(skills):
    return [skill.lower().strip() for skill in skills]

def has_required_skills(freelancer_skills, required_skills):
 
    return any(skill in freelancer_skills for skill in required_skills)

def recommend_freelancers(freelancers, required_skills):
    
    required_skills = preprocess_skills(required_skills)
    
   
    filtered_freelancers = [
        freelancer for freelancer in freelancers
        if has_required_skills(preprocess_skills(freelancer['skills']), required_skills)
    ]
    
   
    if not filtered_freelancers:
        return []
    
    
    freelancer_skills = [', '.join(preprocess_skills(freelancer['skills'])) for freelancer in filtered_freelancers]
    
    
    documents = freelancer_skills + [', '.join(required_skills)]
    
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
    
    
    ranked_freelancers = sorted(zip(cosine_similarities, filtered_freelancers), key=lambda x: x[0], reverse=True)
    
    #
    return [freelancer for _, freelancer in ranked_freelancers]
