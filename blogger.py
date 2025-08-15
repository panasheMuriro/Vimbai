from utils.firebase import get_categories_for_today, db
from google import genai
from datetime import datetime
import os

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY", "")

def generate_blog(category, articles):
    
    prompt = f"""
    You are a Gen Z content creator writing a fun, engaging blog post for the category '{category}'.
    Use casual Gen Z slang, add emojis, keep it short & snappy.
    End with 3-5 trending hashtags.

    Articles:
    {articles}

    Format: Markdown
    """

    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
    )
    
    return response.text



def create_and_save_blogs():
    categories_data = get_categories_for_today()
    if not categories_data:
        return

    today_str = datetime.now().strftime("%Y-%m-%d")
    blogs_doc = {}

    for category, articles in categories_data.items():
        print("starting blog for ", category)
        blog_md = generate_blog(category, articles)
        blogs_doc[category] = blog_md

    # Save to Firestore: blogs/{today_str}
    db.collection("blogs").document(today_str).set(blogs_doc)
    print(f"✅ Blogs saved to Firestore at blogs/{today_str}")

if __name__ == "__main__":
    create_and_save_blogs()
