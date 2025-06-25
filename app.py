from flask import Flask, render_template, request
import re
import random
from database import insert_profile, get_profiles
from scrape import scrape_linkedin
from ai import get_ai_feedback

app = Flask(__name__)

# ==========================
# 1️⃣ Analyze Profile Logic
# ==========================
def analyze_profile(data):
    """Dummy Score Logic - Bas example ke liye"""
    headline_score = 20 if data.get('headline') else 0
    about_score = 30 if data.get('about') and len(data['about']) > 100 else 10
    experience_score = 30 if data.get('experience') else 0
    skills_score = 20 if data.get('skills') else 0
    return headline_score + about_score + experience_score + skills_score


# ==========================
# 2️⃣ Route
# ==========================
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        profile_data = scrape_linkedin(url)

        if profile_data:
            score = analyze_profile(profile_data)
            suggestions = get_ai_feedback(profile_data)

            name = re.sub(r'http[s]?://(www\.)?linkedin\.com/in/', '', url).rstrip('/')
            insert_profile({
                'url': url,
                'name': name,
                'score': score,
                'headline': profile_data.get('headline'),
                'about': profile_data.get('about'),
            })

            profiles = get_profiles()
            return render_template('index.html',
                                   score=score,
                                   profile_data=profile_data,
                                   suggestions=suggestions,
                                   profiles=profiles)

    profiles = get_profiles()
    return render_template('index.html', profiles=profiles)


# ==========================
# 3️⃣ Dummy Profiles Injection
# ==========================
dummy_profiles = [
    {
        'url': 'https://www.linkedin.com/in/satish-sharma/',
        'name': 'Satish Sharma',
        'score': 85,
        'headline': 'Full Stack Developer | React | Node.js',
        'about': 'Developing SaaS products for startups.'
    },
    {
        'url': 'https://www.linkedin.com/in/radhika-verma/',
        'name': 'Radhika Verma',
        'score': 90,
        'headline': 'Data Scientist | AI & ML',
        'about': 'Passionate about building AI & ML pipelines for production.'
    },
    {
        'url': 'https://www.linkedin.com/in/arjun-mehta/',
        'name': 'Arjun Mehta',
        'score': 78,
        'headline': 'Digital Marketer | Growth Hacker',
        'about': 'Helping businesses scale online with growth marketing.'
    },
    {
        'url': 'https://www.linkedin.com/in/priya-singh/',
        'name': 'Priya Singh',
        'score': 88,
        'headline': 'UI/UX Designer | Figma | Adobe',
        'about': 'Designing seamless user interfaces and memorable digital experiences.'
    }
]

# Randomly pick 2 profiles and insert into database (if not already present!)
existing = [p[1] for p in get_profiles()]
to_add = random.sample(dummy_profiles, 2)

for dp in to_add:
    if dp['name'] not in existing:
        insert_profile(dp)


# ==========================
# 4️⃣ Run the App
# ==========================
if __name__ == '__main__':
    app.run(debug=True)

