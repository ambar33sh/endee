"""
app.py

Main Streamlit app for NutriAI.
The UI is split into two columns — left for inputs, right for results.
There's also a semantic search section to directly query Endee.
"""

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="NutriAI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #2ecc71;
        margin-bottom: 0;
    }
    .subtitle {
        color: #888;
        font-size: 1rem;
        margin-top: 0.2rem;
    }
    .meal-card {
        background: #fff;
        border: 1px solid #e0f0e8;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.4rem 0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
    .tag {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 600;
    }
    .veg    { background: #d4edda; color: #155724; }
    .nonveg { background: #fde8e8; color: #7b241c; }
    .stButton>button {
        background: #2ecc71;
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        width: 100%;
    }
    .stButton>button:hover {
        background: #27ae60;
    }
</style>
""", unsafe_allow_html=True)


st.markdown('<p class="main-title">🥗 NutriAI</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Personalised meal planning with Endee vector search + Gemini</p>',
    unsafe_allow_html=True,
)
st.divider()


with st.sidebar:
    st.subheader("How it works")
    st.markdown("""
**1. You fill in your preferences**

**2. Your input gets embedded** using sentence-transformers and sent to Endee as a vector query

**3. Endee returns the most similar meals** using cosine similarity (separately for each meal slot)

**4. Those meals get sent to Gemini** as context, and it generates your plan

The meal plan only includes meals that exist in the Endee database — no hallucinations.

---
Stack: Endee · Gemini 1.5 Flash · sentence-transformers · Streamlit
    """)


col_left, col_right = st.columns([1, 1.6], gap="large")

with col_left:
    st.subheader("Your details")

    goal = st.selectbox(
        "Fitness goal",
        ["fat loss", "muscle gain", "weight gain", "maintenance"],
    )

    diet_type = st.radio(
        "Diet",
        ["vegetarian", "non-vegetarian"],
        horizontal=True,
    )

    daily_calories = st.slider(
        "Daily calorie target",
        min_value=1200,
        max_value=3500,
        value=1800,
        step=100,
        help="Total calories you want to eat in a day",
    )

    allergies = st.text_input(
        "Anything to avoid?",
        placeholder="e.g. dairy, gluten, nuts — or leave blank",
        value="none",
    )

    st.markdown("")
    generate_btn = st.button("Generate meal plan")

    st.divider()
    st.subheader("Search Endee directly")
    st.caption("Type anything and see what the vector DB returns")
    search_query = st.text_input("", placeholder="e.g. light high protein veg dinner")
    search_btn = st.button("Search")


with col_right:

    if search_btn and search_query:
        from vector_store import semantic_search
        st.subheader("Search results from Endee")
        with st.spinner("Querying Endee..."):
            results = semantic_search(search_query, top_k=5)

        if results:
            for r in results:
                tag_cls  = "veg" if r["type"] == "vegetarian" else "nonveg"
                tag_text = "Veg" if r["type"] == "vegetarian" else "Non-Veg"
                st.markdown(f"""
<div class="meal-card">
  <strong>{r['name']}</strong>
  <span class="tag {tag_cls}">{tag_text}</span>
  <span style="float:right;color:#2ecc71;font-weight:700;">{int(r['similarity']*100)}% match</span>
  <br/><small style="color:#666;">{r['description']}</small>
  <br/><br/>
  🔥 <b>{r['calories']}</b> kcal &nbsp;|&nbsp; 💪 <b>{r['protein']}g</b> protein &nbsp;|&nbsp; 🎯 {r['goal']}
</div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No results — make sure Endee is running and meals are loaded.")

    if generate_btn:
        from rag_engine import generate_meal_plan
        st.subheader("Your meal plan")

        progress = st.progress(0)
        status = st.empty()

        try:
            status.info("Searching Endee for matching meals...")
            progress.progress(25)

            with st.spinner("Generating your plan..."):
                progress.progress(50)
                result = generate_meal_plan(
                    goal=goal,
                    daily_calories=daily_calories,
                    diet_type=diet_type,
                    allergies=allergies,
                )
                progress.progress(90)

            progress.progress(100)
            status.success("Done!")

            st.markdown(
                f"**Goal:** {result['goal'].title()} &nbsp;·&nbsp; "
                f"**Calories:** {result['daily_calories']} kcal &nbsp;·&nbsp; "
                f"**Diet:** {result['diet_type'].title()}"
            )
            st.markdown("---")
            st.markdown(result["meal_plan"])

            with st.expander("See what Endee returned (RAG context)"):
                for slot, meals in result["retrieved_meals"].items():
                    st.markdown(f"**{slot.upper()}**")
                    for m in meals:
                        st.markdown(
                            f"- {m['name']} — {m['calories']} kcal "
                            f"(similarity: `{m['similarity']}`)"
                        )

        except EnvironmentError as e:
            progress.empty()
            status.empty()
            st.error(str(e))
            st.info("Add your GEMINI_API_KEY to the .env file.")

        except Exception as e:
            progress.empty()
            status.empty()
            st.error(f"Something went wrong: {e}")
            st.info(
                "Quick checklist:\n"
                "1. Is Endee running? → `docker compose up -d`\n"
                "2. Did you load meals? → `python vector_store.py`\n"
                "3. Is your API key in `.env`?"
            )

    if not generate_btn and not (search_btn and search_query):
        st.markdown("""
**How to use this app:**

1. Fill in your goal, diet preference, and calorie target on the left
2. Click **Generate meal plan**
3. The app searches Endee for the best matching meals and asks Gemini to build your plan

You can also test the vector search directly using the search box — it shows you exactly what Endee returns and the similarity score for each result.

---

**Flow:**
```
Your input
    ↓
Embed with sentence-transformers (384-dim vector)
    ↓
Query Endee (cosine similarity search)
    ↓
Top meals for each slot → Gemini prompt
    ↓
Personalised meal plan
```
        """)
