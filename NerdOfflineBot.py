import os
import time
from datetime import datetime
from dotenv import load_dotenv
from trendspyg import download_google_trends_rss
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# --- Setup Gemini Client ---
gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=60000)
)


def get_candidate_trends():
    # Fetch from both US (global proxy) and India
    try:
        trend_data_us = download_google_trends_rss(geo='US', normalize=True)
        trend_data_in = download_google_trends_rss(geo='IN', normalize=True)

        trends_us = [item['keyword'] for item in trend_data_us['trends'][:10]]
        trends_in = [item['keyword'] for item in trend_data_in['trends'][:10]]

        # Combine and remove any duplicates
        combined_trends = list(set(trends_us + trends_in))
        return combined_trends
    except Exception as e:
        print(f"[!] Error fetching trends: {e}")
        return []


def select_nerdy_trend(trends_list):
    prompt = f"""
    You are the content director for a Twitter page called 'NerdTrending'.
    Your target audience is global, but the perspective should resonate with an Indian tech/science enthusiast (think global tech, space, gaming, and internet culture).

    Here is a combined list of current top Google Trends from the US and India:
    {trends_list}

    Select exactly ONE topic from this list that is globally recognizable, but highly relatable to an Indian nerd. 
    Avoid hyper-local politics or regional sports unless they have massive global tech or meme crossover appeal.

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
    2. Audience & Persona: Target a global audience, written from the relatable, sharp perspective of an Indian tech enthusiast.
    3. Angle: Frame the explanation to interest nerds (focus on the tech, science, lore, underlying systems, or historical context).
    4. Tone: Conversational, enthusiastic, slightly mischievous.
    5. Style: Use bracketed side comments (like this). Compare complex things to everyday tech, pop culture, or gaming. Ask rhetorical questions.
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


def save_thread_to_file(tweets, topic):
    output_dir = "generated_tweets"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    today_str = datetime.now().strftime("%Y-%m-%d")

    counter = 1
    while True:
        filename = f"{today_str}_{counter}.txt"
        filepath = os.path.join(output_dir, filename)
        if not os.path.exists(filepath):
            break
        counter += 1

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(f"Topic: {topic}\n")
        file.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("=" * 40 + "\n\n")

        for i, tweet in enumerate(tweets):
            file.write(f"--- Tweet {i + 1} ---\n")
            file.write(tweet + "\n\n")

    print(f"      -> Saved successfully to: {filepath}")


if __name__ == "__main__":
    try:
        print("[1/5] Fetching combined global & local trends...")
        candidates = get_candidate_trends()
        print(f"      -> Candidates: {candidates}")

        print("\n[2/5] Selecting the perfect crossover topic...")
        trend = select_nerdy_trend(candidates)
        print(f"      -> Target acquired: {trend}")

        print("\n[3/5] Generating thread via Gemini...")
        thread = generate_thread(trend)

        print("\n[4/5] Saving to local text file...")
        save_thread_to_file(thread, trend)

        print(f"\n[5/5] Success! Offline thread for '{trend}' is ready for review.")

    except Exception as e:
        print(f"\n[ERROR] An exception occurred:\n{e}")