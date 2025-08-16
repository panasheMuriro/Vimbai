# Vimbai – Zimbabwean AI News Blogger

Vimbai is a full-stack news aggregation and blogging app focused on Zimbabwean local news. The app scrapes multiple news sources, summarizes articles, categorizes them with AI, and generates Gen Z-style blog posts with emojis and hashtags. The frontend is built with **React + Vite**, and the backend uses **Python, Firebase, and Gemini Flash Lite API**.

---

## Table of Contents

1. [Features](#features)
2. [Frontend](#frontend)
3. [Backend](#backend)
4. [Setup](#setup)
5. [Environment Variables](#environment-variables)
6. [Running Locally](#running-locally)
7. [GitHub Actions Automation](#github-actions-automation)
8. [Folder Structure](#folder-structure)
9. [License](#license)

---

## Features

<img width="1536" height="1024" alt="flow_diagram" src="https://github.com/user-attachments/assets/348777d6-9001-4291-925d-7fb1436b9e52" />


* Scrapes multiple Zimbabwean news sources:

  * Pindula, ZimEye, New Zimbabwe, News Day, News Dze Zimbabwe
* Summarizes articles to 2-3 sentences
* Categorizes articles into meaningful groups using **Gemini Flash Lite**
* Generates fun, Gen Z-style blogs with emojis and hashtags
* Saves blogs and categorized articles in **Firebase Firestore**
* Frontend displays blogs in cards with expandable content
* Responsive, mobile-first UI using TailwindCSS

---

## Frontend

**Tech stack:** React, TypeScript, Vite, TailwindCSS, Firebase Firestore

**Key components:**

* `BlogList.tsx` – Fetches blogs from Firestore and displays them in cards. Supports “See More/Show Less” toggling.
* `StickyHeader.tsx` – Sticky top navigation.
* `Avatar.tsx` – Loads profile picture from `/public` folder.
* `Bio.tsx` – Displays AI author info for Vimbai.

**Firebase setup:**

* Firestore is used to fetch `blogs_test` collection
* Vite environment variables are stored in `.env` file:

```env
VITE_FIREBASE_API_KEY=your_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id
```

**Start frontend locally:**

```bash
cd frontend
npm install
npm run dev
```

---

## Backend

**Tech stack:** Python 3.11, Firebase Admin SDK, Gemini API, Sumy (text summarization), requests, BeautifulSoup

**Key files:**

* `categorizer.py` – Scrapes news, summarizes, and categorizes articles via Gemini Flash Lite
* `blogger.py` – Generates Gen Z-style blog posts from categorized articles and saves to Firestore
* `utils/firebase.py` – Handles Firestore operations (`post_to_firestore`, `get_categories_for_today`)
* `scrappers/` – Individual scrapers for each news source
* `requirements.txt` – Python dependencies

**Install backend dependencies:**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Environment Variables for backend (use GitHub secrets or `.env` for local dev):**

```env
GEMINI_API_KEY=your_gemini_api_key
FIREBASE_SERVICE_ACCOUNT_JSON=contents_of_your_service_account.json
```

---

## Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/vimbai.git
cd vimbai
```

2. Install frontend dependencies:

```bash
cd frontend
npm install
```

3. Install backend dependencies:

```bash
cd ../
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. Add Firebase service account JSON to `utils/firebase-service-account.json` or as a secret in GitHub Actions.
5. Add Gemini API key as an environment variable or secret.

---

## Running Locally

**Backend:**

```bash
source .venv/bin/activate
python categorizer.py    # Categorize articles
python blogger.py        # Generate blogs
```

**Frontend:**

```bash
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## GitHub Actions Automation

* Workflow runs daily at 6 AM UTC to scrape, categorize, and generate blogs automatically.
* Workflow steps:

  1. Checkout repository
  2. Set up Python 3.11
  3. Install dependencies
  4. Write Firebase service account JSON from secret
  5. Run `categorizer.py`
  6. Run `blogger.py`

Example workflow snippet:

```yaml
name: Daily Article Categorization & Blogging
on:
  schedule:
    - cron: "0 6 * * *"
  workflow_dispatch:

jobs:
  run_pipeline:
    runs-on: ubuntu-latest
    env:
      GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
      FIREBASE_SERVICE_ACCOUNT_JSON: ${{ secrets.FIREBASE_SERVICE_ACCOUNT_JSON }}
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - run: pip install -r requirements.txt
      - run: echo "$FIREBASE_SERVICE_ACCOUNT_JSON" > ./utils/firebase-service-account.json
      - run: python categorizer.py
      - run: python blogger.py
```

---

## Folder Structure

```
├── backend
│   ├── categorizer.py
│   ├── blogger.py
│   ├── utils
│   │   ├── firebase.py
│   │   └── firebase-service-account.json
│   └── scrappers
│       ├── pindula.py
│       ├── zimeye.py
│       ├── new_zimbabwe.py
│       ├── news_day.py
│       └── news_dze_zimbabwe.py
├── frontend
│   ├── src
│   │   ├── components
│   │   │   ├── BlogList.tsx
│   │   │   ├── StickyHeader.tsx
│   │   │   └── Avatar.tsx
│   │   ├── App.tsx
│   │   └── firebase.ts
│   └── public
│       └── avatar.png
├── .github/workflows
│   └── daily_blog.yml
├── README.md
└── requirements.txt
```

---

## License

MIT License – free to use and modify.

