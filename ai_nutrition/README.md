# NutriAI — Meal Planner using Endee Vector DB + Gemini

I built this project to solve a problem I actually face — figuring out what to eat based on my fitness goal without spending 20 minutes Googling. The idea was simple: use vector search to find meals that *actually match* what I need, then use an LLM to put together a full day's plan.

The interesting part was using **Endee** as the vector database. Instead of doing a boring keyword search like `WHERE goal = 'fat loss'`, the app converts meal descriptions into embeddings and does semantic similarity search. So when you type "high protein low calorie veg", it finds meals that fit — even if those exact words aren't in the meal name.

\---

## What the project does

You enter your fitness goal, diet preference, daily calorie target, and any allergies. The app:

1. Converts your input into a search query
2. Searches the Endee vector DB for the best matching meals (separately for breakfast, lunch, dinner, snack)
3. Sends those retrieved meals as context to Gemini
4. Gets back a full personalised meal plan with reasoning

There's also a live semantic search panel where you can type anything and see which meals Endee returns with similarity scores — useful for understanding how vector search actually works.

\---

## How Endee fits in

Endee is the core of this project, not just a side component. Here's exactly how I used it:

* Created an index called `nutri\_meals` with 384 dimensions, cosine similarity, INT8 precision
* Each meal's description, goal, diet type, calories etc. gets converted into a 384-dim vector using `sentence-transformers`
* Those vectors get stored in Endee via `index.upsert()`
* At query time, the user's input gets embedded the same way, and `index.query(vector, top\_k=5)` returns the closest meals
* I run 4 separate queries (one per meal slot) and feed all results into the Gemini prompt

The reason vector search makes sense here is that a regular database can't understand that "light protein-rich dinner" and "Grilled Salmon Salad" are related unless you manually tag everything. Endee figures that out from the embeddings.

\---

## System design

```
User fills in the form (goal, calories, diet type, allergies)
        |
        v
Query gets built and embedded (sentence-transformers, 384-dim)
        |
        v
Endee vector DB — cosine similarity search
(nutri\_meals index, 15 meals stored as vectors)
        |
        v
Top-K meals retrieved for breakfast / lunch / dinner / snack
        |
        v
RAG prompt built with retrieved meals as context
        |
        v
Google Gemini 1.5 Flash generates the meal plan
        |
        v
Output shown in Streamlit UI
```

\---

## Project files

```
nutri-ai/
├── app.py              # Streamlit UI
├── vector\_store.py     # Everything Endee related — store, search, embed
├── rag\_engine.py       # Retrieval + Gemini call
├── requirements.txt
├── docker-compose.yml  # Runs Endee locally via Docker
├── .env.example        # Copy this to .env and add your API key
└── data/
    └── meals.json      # 15 meals with nutritional info
```

\---

## Tech used

|What|Tool|
|-|-|
|Vector database|Endee (forked from endee-io/endee)|
|Embeddings|sentence-transformers all-MiniLM-L6-v2|
|LLM|Google Gemini 1.5 Flash|
|UI|Streamlit|
|Language|Python 3.10+|
|Running Endee|Docker|

\---

## Setup

### Before you start

You need:

* Python 3.10+
* Docker Desktop installed and running
* A free Gemini API key — get one at https://aistudio.google.com/apikey (takes about 30 seconds, no credit card needed)

\---

### Step 1 — Star and fork Endee (required by the evaluation)

Go to https://github.com/endee-io/endee, star it, and fork it to your account. This project is built on top of that fork.

\---

### Step 2 — Clone and set up

```bash
git clone https://github.com/<your-username>/nutri-ai
cd nutri-ai
pip install -r requirements.txt
```

\---

### Step 3 — Start Endee

```bash
docker compose up -d
```

Wait about 10 seconds then open http://localhost:8081 — if you see the Endee dashboard it's working.

\---

### Step 4 — Add your API key

```bash
cp .env.example .env
```

Open `.env` and paste your Gemini key:

```
GEMINI\_API\_KEY=your\_key\_here
```

\---

### Step 5 — Load meals into Endee

```bash
python vector\_store.py
```

This embeds all 15 meals and stores them in Endee. First run takes a minute because it downloads the embedding model. You should see:

```
\[INFO] Index 'nutri\_meals' created
\[SUCCESS] 15 meals stored in Endee
```

\---

### Step 6 — Run the app

```bash
streamlit run app.py
```

Opens at http://localhost:8501

\---

## Using the app

* Pick your goal (fat loss, muscle gain, etc.)
* Choose vegetarian or non-vegetarian
* Set your calorie target
* Add any foods you want to avoid
* Hit Generate

You'll get a full day's meal plan — breakfast, lunch, dinner, snack — with calorie totals and a short explanation of why the plan fits your goal.

The semantic search box at the bottom lets you search the Endee index directly if you want to test it.

\---

## Meals dataset

15 meals in `data/meals.json` covering Indian and international options across different goals and diet types. Each meal has: name, calories, protein, carbs, fat, type (veg/non-veg), goal, meal time, and a description that gets embedded.

\---

## If something breaks

|Error|Fix|
|-|-|
|Can't connect to Endee|Make sure Docker is running and you did `docker compose up -d`|
|GEMINI\_API\_KEY error|Check your `.env` file has the key|
|Meals not showing|Run `python vector\_store.py` first|
|pip install fails|Try `pip install --upgrade pip` first|

\---

## License

Apache 2.0 — same as the Endee repository this is built on.

