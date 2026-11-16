# NerdTrending Bot 🧠📈

NerdTrending is a fully automated, Python-based Twitter (X) bot that curates the daily "nerdiest" Google Trends and breaks them down into highly engaging, 5-part educational threads. Powered by Google's Gemini AI, the bot transforms everyday trends into universal tech, science, and history lore.

## Features

* **Real-Time Trend Extraction:** Leverages `trendspyg` to safely fetch real-time Google Trends via stable RSS feeds, avoiding hidden API 404 endpoints.
* **Two-Stage AI Pipeline:** 
  1. **The Editor:** Evaluates top trends and selects the one with the highest potential for a tech/science/historical angle.
  2. **The Writer:** Drafts a perfectly formatted, 5-part Twitter thread tailored for a global, nerdy audience.
* **Resilient Architecture:** Built with exponential backoff and timeout handling to smoothly bypass upstream API 503/504 errors and corporate proxy drops.
* **Zero-Touch Publishing:** Authenticates via OAuth 1.0a User Context to automatically thread and publish posts using `tweepy`.

## Prerequisites

* Python 3.8+
* [Google AI Studio](https://aistudio.google.com/) API Key
* [X (Twitter) Developer](https://developer.x.com/) Account (Free Tier with Read & Write permissions)

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
   TWITTER_API_KEY="your_consumer_key"
   TWITTER_API_SECRET="your_consumer_secret"
   TWITTER_ACCESS_TOKEN="your_access_token"
   TWITTER_ACCESS_SECRET="your_access_token_secret"
   GEMINI_API_KEY="your_gemini_api_key"
   ```
   *(Note: The `.env` file is included in `.gitignore` by default to prevent accidental credential leaks).*

## Usage

Run the bot manually from your terminal:
```bash
python bot.py
```

### Automation (Cron)
To run the bot automatically 5 times a day (e.g., 9 AM, 12 PM, 3 PM, 6 PM, 9 PM), add this to your system's crontab (`crontab -e`):
```bash
0 9,12,15,18,21 * * * cd /absolute/path/to/NerdTrending && /absolute/path/to/NerdTrending/.venv/bin/python bot.py >> cron.log 2>&1
```

## Containerized Deployment (Docker / Podman)

For terminal-first and self-hosted workflows, you can easily containerize this bot to run as a background daemon.

1. **Create a `Dockerfile`:**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY bot.py .
   CMD ["python", "bot.py"]
   ```
2. **Build and Run:**
   ```bash
   podman build -t nerd-trending-bot .
   podman run -d --env-file .env --name nerd-bot nerd-trending-bot
   ```

## Author
**Umang Upadhayay**
