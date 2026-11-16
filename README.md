# NerdTrending Bot 🧠📈

NerdTrending is an automated, Python-based bot that curates the daily "nerdiest" Google Trends and breaks them down into highly engaging, 5-part educational threads. Powered by Google's Gemini AI, the bot transforms everyday trends into universal tech, science, and history lore, written from the relatable perspective of an Indian tech enthusiast.

## Features

* **Dual-Region Trend Extraction:** Leverages `trendspyg` to safely fetch real-time Google Trends from both the US (as a proxy for global tech/culture) and India.
* **Two-Stage AI Pipeline:**
  1. **The Editor:** Evaluates combined global/local trends and selects the one with the highest potential for a universal crossover tech/science angle.
  2. **The Writer:** Drafts a perfectly formatted, 5-part Twitter thread tailored for a global, nerdy audience.
* **Offline-First Workflow:** Generates and saves the threads locally as `.txt` files in a `generated_tweets/` folder to build a backlog and avoid immediate X (Twitter) API Pay-Per-Use costs. 
* **Twitter Ready:** Includes a secondary script (`bot.py`) that can authenticate via OAuth 1.0a to automatically thread and publish posts directly to X whenever you are ready to automate.

## Prerequisites

* Python 3.8+
* [Google AI Studio](https://aistudio.google.com/) API Key
* *(Optional for `bot.py`)* [X (Twitter) Developer](https://developer.x.com/) Account (Free Tier with prepaid credits for Write access)

## Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/NerdTrending.git
   cd NerdTrending
   ```

2. **Set up the virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install tweepy python-dotenv google-genai trendspyg
   ```

4. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your API keys:
   ```env
   # Required for Gemini
   GEMINI_API_KEY="your_gemini_api_key"
   
   # Only required if using the online bot.py script
   TWITTER_API_KEY="your_consumer_key"
   TWITTER_API_SECRET="your_consumer_secret"
   TWITTER_ACCESS_TOKEN="your_access_token"
   TWITTER_ACCESS_SECRET="your_access_token_secret"
   ```
   *(Note: The `.env` file should be included in your `.gitignore` to prevent credential leaks).*

## Usage

**To generate and save threads locally (Recommended):**
Run the offline bot manually from your terminal:
```bash
python offline_bot.py
```
This will create a dated file (e.g., `2026-11-16_1.txt`) inside the `generated_tweets/` directory.

**To automatically post to Twitter (Requires API Credits):**
```bash
python bot.py
```

### Automation (Cron)
To generate new threads automatically 5 times a day (e.g., 9 AM, 12 PM, 3 PM, 6 PM, 9 PM), add this to your system's crontab (`crontab -e`):
```bash
0 9,12,15,18,21 * * * cd /absolute/path/to/NerdTrending && /absolute/path/to/NerdTrending/.venv/bin/python offline_bot.py >> cron.log 2>&1
```

## Containerized Deployment (Docker / Podman)

1. **Create a `Dockerfile`:**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY offline_bot.py .
   CMD ["python", "offline_bot.py"]
   ```
2. **Build and Run:**
   ```bash
   podman build -t nerd-trending-bot .
   podman run -d --env-file .env --name nerd-bot nerd-trending-bot
   ```

## Author
**Umang Upadhayay**