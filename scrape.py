import requests
from bs4 import BeautifulSoup

def scrape_linkedin(url):
    """
    Final scrape_linkedin method:
    1️⃣ Try karega public page se scrape.
    2️⃣ Agar fail hua (ya restriction laga), dummy data dega.
    """
    try:
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(resp.content, 'html.parser')
        headline = soup.find('h2')
        about = soup.find('div', {'class': 'pv-about__summary'}) or soup.find('section', {'class': 'pv-about-section'})
        experience = bool(soup.find('section', {'id': 'experience-section'}))
        skills = bool(soup.find('span', {'class': 'pv-skill-category-entity__name'}))

        headline_text = headline.get_text(strip=True) if headline else None
        about_text = about.get_text(strip=True) if about else None

        # ✅ Check kya data mila
        if not headline_text and not about_text:
            # Dummy fallback
            return {
                'headline': 'Software Engineer | AI Enthusiast',
                'about': 'Passionate about AI and ML. Seeking opportunities in AI/ML and data engineering roles.',
                'experience': True,
                'skills': True
            }

        return {
            'headline': headline_text,
            'about': about_text,
            'experience': experience,
            'skills': skills
        }

    except Exception as e:
        # ✅ Jab error aaye (ya scraping fail ho), dummy data
        print(f"Error scraping LinkedIn: {e}")
        return {
            'headline': 'Software Engineer | AI Enthusiast',
            'about': 'Passionate about AI and ML. Seeking opportunities in AI/ML and data engineering roles.',
            'experience': True,
            'skills': True
        }

