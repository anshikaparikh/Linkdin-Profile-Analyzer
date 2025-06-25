import cohere

# 👇 Apni COHERE_API_KEY yaha daale
COHERE_API_KEY = "NjgIHhFLUEQ6JWwnEarM3vFTJp2waGWzR8KF5lwc"

def get_ai_feedback(data):
    """Cohere AI ke saath Suggestions."""
    prompt = (
        f"LinkedIn Profile:\n"
        f"Headline: {data.get('headline')}\n"
        f"About: {data.get('about')}\n"
        f"Experience Present: {data.get('experience')}\n"
        f"Skills Present: {data.get('skills')}\n\n"
        "Give 3 actionable, crisp, professional suggestions for making this LinkedIn profile better."
    )
    try:
        co = cohere.Client(COHERE_API_KEY)
        response = co.generate(
            model='command-r-plus',
            prompt=prompt,
            max_tokens=150,
            temperature=0.5
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"Error getting AI feedback from Cohere: {str(e)}"
