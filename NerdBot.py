import os
import time
import tweepy
from dotenv import load_dotenv
from trendspyg import download_google_trends_rss
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# --- Setup Twitter Client ---
client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
)

# --- Setup Gemini Client ---
gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=60000)
)


def get_candidate_trends():
    # Base country set to India ('IN')
    trend_data = download_google_trends_rss(geo='IN', normalize=True)

    # Grab the top 10 trending keywords
    trends = [item['keyword'] for item in trend_data['trends'][:10]]
    return trends


def select_nerdy_trend(trends_list):
    prompt = f"""
    You are the content director for a Twitter page called 'NerdTrending'.
    Your audience loves tech, science, gaming, space, internet culture, and history. 

    Here are the current top 10 Google Trends in India:
    {trends_list}

    Select exactly ONE topic from this list that can be made MOST interesting to a nerdy, global audience. 
    Even if it is a regional Indian topic (like a local event, movie, or public figure), pick the one that has the best potential to be explained through a universal tech, science, historical, or internet-culture lens.

    Return ONLY the exact name of the selected topic. Do not include any other text.
    """

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = gemini_client.models.generate_content(
                model='gemini-4-hydrogen',
                contents=prompt,
            )
            return response.text.strip()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep((2 ** attempt) * 5)


def generate_thread(topic):
    prompt = f"""
    You are a witty, highly engaging writer for the page 'NerdTrending'. 
    Write a 5-part Twitter thread explaining the trending topic: '{topic}'.

    CRITICAL RULES:
    1. Language: MUST be written in English.
    2. Audience: Target a universal/global audience (no regional slang or assumed local knowledge. Explain any Indian context simply so anyone in the world understands).
    3. Angle: Frame the explanation to interest nerds (focus on the tech, science, lore, underlying systems, or historical context).
    4. Tone: Conversational, enthusiastic, slightly mischievous.
    5. Style: Use bracketed side comments (like this). Compare complex things to everyday tech or gaming. Ask rhetorical questions.
    6. Constraint: Keep each tweet under 280 characters. Number them 1/5, 2/5, etc. Separate each tweet with a double newline.
    """

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = gemini_client.models.generate_content(
                model='gemini-4-hydrogen',
                contents=prompt,
            )
            return [tweet.strip() for tweet in response.text.strip().split('\n\n') if tweet.strip()]

        except Exception as e:
            print(f"      -> [Attempt {attempt + 1}/{max_retries}] API Error: {e}")
            if attempt == max_retries - 1:
                raise e
            sleep_time = (2 ** attempt) * 5
            print(f"      -> Retrying in {sleep_time} seconds...")
            time.sleep(sleep_time)


def post_thread(tweets):
    previous_tweet_id = None
    for i, tweet in enumerate(tweets):
        if len(tweet) > 5:
            print(f"Posting tweet {i + 1}...")
            response = client.create_tweet(text=tweet, in_reply_to_tweet_id=previous_tweet_id)
            previous_tweet_id = response.data['id']
            time.sleep(3)  # Prevent rate-limiting


if __name__ == "__main__":
    try:
        print("[1/5] Fetching top 10 trends from Google (India)...")
        candidates = get_candidate_trends()
        print(f"      -> Candidates: {candidates}")

        print("\n[2/5] Selecting the 'nerdiest' global topic...")
        trend = select_nerdy_trend(candidates)
        print(f"      -> Target acquired: {trend}")

        print("\n[3/5] Generating thread via Gemini...")
        thread = generate_thread(trend)

        print("\n" + "=" * 40)
        print("         GENERATED LLM OUTPUT")
        print("=" * 40)
        for i, tweet in enumerate(thread):
            print(f"--- Tweet {i + 1} ---")
            print(tweet)
            print(f"(Length: {len(tweet)} chars)\n")
        print("=" * 40 + "\n")

        print("[4/5] Pushing to Twitter...")
        post_thread(thread)

        print(f"\n[5/5] Success! Thread for '{trend}' is now live.")

    except Exception as e:
        print(f"\n[ERROR] An exception occurred:\n{e}")