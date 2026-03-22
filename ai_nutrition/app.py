"""
app.py - Diet Logix
Redesigned: tighter layout, no wasted space, more visual impact.
"""
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Diet Logix", page_icon="🥗", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Outfit:wght@300;400;500;600&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #ffffff !important;
    color: #111 !important;
    font-family: 'Outfit', sans-serif;
}
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding: 0 2.5rem 3rem !important; max-width: 1280px !important; }

/* ── NAVBAR ── */
.navbar {
    background: #fff;
    border-bottom: 1.5px solid #f0f0f0;
    padding: 0 2.5rem;
    margin: 0 -2.5rem 0;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
}
.nav-logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
    color: #111;
    letter-spacing: -0.03em;
}
.nav-logo span { color: #16a34a; }
.nav-pills { display: flex; gap: 0.5rem; }
.nav-pill {
    background: #f4f4f4;
    color: #666;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
}
.nav-pill.active { background: #dcfce7; color: #16a34a; }

/* ── HERO STRIP ── */
.hero-strip {
    background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 60%);
    border-bottom: 1.5px solid #f0f0f0;
    padding: 4rem 2.5rem 3.5rem;
    margin: 0 -2.5rem 2.5rem;
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    gap: 2rem;
    align-items: center;
}
.hero-eyebrow {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #16a34a;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 6px;
}
.hero-eyebrow::before {
    content: '';
    display: inline-block;
    width: 20px;
    height: 2px;
    background: #16a34a;
    border-radius: 2px;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 4rem;
    font-weight: 800;
    line-height: 1.08;
    color: #111;
    letter-spacing: -0.04em;
    margin-bottom: 1rem;
}
.hero-title em {
    font-style: italic;
    color: #16a34a;
    font-family: 'Outfit', sans-serif;
    font-weight: 300;
}
.hero-desc {
    font-size: 1.05rem;
    color: #888;
    line-height: 1.7;
    font-weight: 400;
    max-width: 420px;
}
.hero-stats {
    display: flex;
    gap: 2rem;
}
.stat-item { text-align: center; }
.stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    color: #111;
    line-height: 1;
}
.stat-num span { color: #16a34a; }
.stat-label {
    font-size: 0.72rem;
    color: #aaa;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 4px;
}

/* ── STEPS BAR ── */
.steps-bar {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    border: 1.5px solid #f0f0f0;
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 1.8rem;
    background: #fafafa;
}
.step-cell {
    padding: 1.6rem 1.4rem;
    border-right: 1.5px solid #f0f0f0;
    background: #fff;
    position: relative;
}
.step-cell:last-child { border-right: none; }
.step-cell::before {
    content: attr(data-num);
    position: absolute;
    top: 1rem;
    right: 1rem;
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #f4f4f4;
    line-height: 1;
}
.step-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #16a34a;
    margin-bottom: 0.4rem;
}
.step-name {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #111;
    margin-bottom: 0.4rem;
}
.step-info { font-size: 0.82rem; color: #aaa; line-height: 1.55; }

/* ── FORM PANEL ── */
.panel {
    background: #fff;
    border: 1.5px solid #f0f0f0;
    border-radius: 14px;
    padding: 1.8rem 1.8rem;
    margin-bottom: 1rem;
}
.panel-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #ccc;
    margin-bottom: 1.4rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #f5f5f5;
    display: flex;
    align-items: center;
    gap: 8px;
}
.panel-title::before {
    content: '';
    display: inline-block;
    width: 3px;
    height: 14px;
    background: #16a34a;
    border-radius: 2px;
}

/* ── Streamlit widget overrides ── */
.stSelectbox label, .stRadio label, .stSlider label, .stTextInput label {
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    color: #aaa !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}
[data-testid="stSelectbox"] > div > div {
    background: #fafafa !important;
    border: 1.5px solid #efefef !important;
    border-radius: 10px !important;
    color: #111 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.9rem !important;
}
[data-testid="stTextInput"] input {
    background: #fafafa !important;
    border: 1.5px solid #efefef !important;
    border-radius: 10px !important;
    color: #111 !important;
    font-family: 'Outfit', sans-serif !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #16a34a !important;
    box-shadow: 0 0 0 3px rgba(22,163,74,0.08) !important;
}
[data-testid="stRadio"] label {
    text-transform: none !important;
    letter-spacing: 0 !important;
    font-size: 0.92rem !important;
    color: #111 !important;
    font-weight: 500 !important;
}
[data-testid="stRadio"] div[role="radiogroup"] {
    background: #f7f7f7 !important;
    border: 1.5px solid #efefef !important;
    border-radius: 10px !important;
    padding: 0.5rem 0.8rem !important;
}
[data-testid="stRadio"] p {
    color: #111 !important;
    font-size: 0.92rem !important;
    font-weight: 500 !important;
}
[data-testid="stRadio"] span {
    color: #111 !important;
    font-size: 0.92rem !important;
    font-weight: 500 !important;
}
[data-testid="stSlider"] [role="slider"] { background: #16a34a !important; border-color: #16a34a !important; }
.stSlider [data-baseweb="slider"] [role="progressbar"] { background: #16a34a !important; }

/* ── MAIN BUTTON ── */
.stButton > button {
    background: #111 !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.06em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #16a34a !important;
    box-shadow: 0 6px 20px rgba(22,163,74,0.2) !important;
    transform: translateY(-1px) !important;
}

/* ── MEAL CARDS ── */
.meal-card {
    background: #fff;
    border: 1.5px solid #f0f0f0;
    border-radius: 12px;
    padding: 1.3rem 1.4rem;
    margin: 0.6rem 0;
    transition: all 0.18s;
}
.meal-card:hover { border-color: #d1fae5; box-shadow: 0 4px 14px rgba(22,163,74,0.07); }
.mc-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.3rem; }
.mc-name { font-family: 'Syne', sans-serif; font-size: 1.05rem; font-weight: 700; color: #111; }
.mc-score { background: #f0fdf4; color: #16a34a; font-size: 0.72rem; font-weight: 700; font-family: 'Syne', sans-serif; padding: 4px 12px; border-radius: 20px; border: 1px solid #bbf7d0; white-space: nowrap; }
.mc-desc { font-size: 0.83rem; color: #bbb; line-height: 1.5; margin-bottom: 0.8rem; }
.mc-meta { display: flex; align-items: center; gap: 0.8rem; font-size: 0.82rem; color: #bbb; flex-wrap: wrap; }
.mc-meta b { color: #555; }
.mc-tag { font-size: 0.65rem; font-weight: 600; padding: 2px 8px; border-radius: 6px; text-transform: uppercase; letter-spacing: 0.05em; }
.veg  { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
.nveg { background: #fff1f0; color: #e5472a; border: 1px solid #fecaca; }

/* ── PLAN OUTPUT ── */
.plan-box {
    background: #fff;
    border: 1.5px solid #f0f0f0;
    border-radius: 14px;
    overflow: hidden;
}
.plan-top {
    background: #111;
    padding: 1.5rem 1.8rem;
    display: flex;
    gap: 2.5rem;
    align-items: center;
}
.plan-top-logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 800;
    color: #fff;
    margin-right: auto;
}
.plan-top-logo span { color: #4ade80; }
.pt-item { font-size: 0.7rem; color: #555; text-transform: uppercase; letter-spacing: 0.1em; }
.pt-item b { display: block; color: #fff; font-size: 0.95rem; text-transform: none; letter-spacing: 0; margin-top: 2px; font-family: 'Outfit', sans-serif; font-weight: 500; }
.plan-body { padding: 1.8rem; font-size: 1rem; line-height: 1.9; color: #444; }

/* ── EMPTY STATE ── */
.empty {
    background: #fafafa;
    border: 1.5px dashed #e5e5e5;
    border-radius: 14px;
    padding: 5rem 2rem;
    text-align: center;
}
.empty-icon { font-size: 3.5rem; margin-bottom: 1rem; }
.empty-title { font-family: 'Syne', sans-serif; font-size: 1.2rem; font-weight: 700; color: #333; margin-bottom: 0.5rem; }
.empty-desc { font-size: 0.88rem; color: #bbb; line-height: 1.6; max-width: 280px; margin: 0 auto; }

hr { border-color: #f0f0f0 !important; }
[data-testid="stAlert"] { background: #fafafa !important; border: 1.5px solid #efefef !important; border-radius: 12px !important; }
[data-testid="stExpander"] { background: #fafafa !important; border: 1.5px solid #efefef !important; border-radius: 12px !important; }
[data-testid="stExpander"] summary { color: #aaa !important; font-size: 0.8rem !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #fff; }
::-webkit-scrollbar-thumb { background: #e5e5e5; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ── Navbar ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div class="nav-logo">Diet<span>Logix</span></div>
    <div class="nav-pills">
        <span class="nav-pill active">Endee Vector DB</span>
        <span class="nav-pill">RAG Pipeline</span>
        <span class="nav-pill">Semantic Search</span>
        <span class="nav-pill">Python · Streamlit</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Hero strip ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-strip">
    <div>
        <div class="hero-eyebrow">AI-Powered Nutrition Planning</div>
        <div class="hero-title">Smart meals for<br>your <em>exact goal.</em></div>
        <div class="hero-desc">Tell us what you're working towards. We use Endee's vector database to find the most relevant meals and build your personalised day plan with AI.</div>
    </div>
    <div class="hero-stats">
        <div class="stat-item">
            <div class="stat-num">15<span>+</span></div>
            <div class="stat-label">Meals in DB</div>
        </div>
        <div class="stat-item">
            <div class="stat-num">384<span>d</span></div>
            <div class="stat-label">Vector Dims</div>
        </div>
        <div class="stat-item">
            <div class="stat-num">4<span>x</span></div>
            <div class="stat-label">Endee Queries</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Steps bar ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="steps-bar">
    <div class="step-cell" data-num="1">
        <div class="step-label">Step 01</div>
        <div class="step-name">Set your goal</div>
        <div class="step-info">Choose fat loss, muscle gain, or maintenance. Set calories and diet type.</div>
    </div>
    <div class="step-cell" data-num="2">
        <div class="step-label">Step 02</div>
        <div class="step-name">Endee searches</div>
        <div class="step-info">Query becomes a 384-dim vector. Endee returns closest meals via cosine similarity.</div>
    </div>
    <div class="step-cell" data-num="3">
        <div class="step-label">Step 03</div>
        <div class="step-name">AI builds plan</div>
        <div class="step-info">Retrieved meals are sent as context. LLM generates your personalised day plan.</div>
    </div>
    <div class="step-cell" data-num="4">
        <div class="step-label">Step 04</div>
        <div class="step-name">You get results</div>
        <div class="step-info">Full meal plan with macros and reasoning — only real meals from Endee.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Main layout ───────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.6], gap="large")

with col_left:
    st.markdown('<div class="panel"><div class="panel-title">Your Preferences</div>', unsafe_allow_html=True)
    goal = st.selectbox("FITNESS GOAL", ["fat loss", "muscle gain", "weight gain", "maintenance"])
    diet_type = st.selectbox("DIET TYPE", ["vegetarian", "non-vegetarian"])
    daily_calories = st.slider("DAILY CALORIES", min_value=1200, max_value=3500, value=1800, step=100)
    allergies = st.text_input("AVOID", placeholder="dairy, gluten, nuts — or leave as none", value="none")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("Generate My Meal Plan →")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="panel-title">Search Endee Directly</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.78rem;color:#ccc;margin-bottom:0.8rem;line-height:1.5;">Type anything and see what the vector DB returns with similarity scores.</p>', unsafe_allow_html=True)
    search_query = st.text_input("SEARCH QUERY", placeholder="e.g. high protein veg dinner")
    search_btn = st.button("Search Vector DB")
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:

    # ── Search results ────────────────────────────────────────────────────────
    if search_btn and search_query:
        from vector_store import semantic_search
        with st.spinner("Querying Endee..."):
            results = semantic_search(search_query, top_k=5)
        if results:
            st.markdown(f'<p style="font-size:0.68rem;color:#bbb;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.6rem;">— {len(results)} results from Endee vector DB</p>', unsafe_allow_html=True)
            for r in results:
                tag_cls  = "veg" if r["type"] == "vegetarian" else "nveg"
                tag_text = "Veg" if r["type"] == "vegetarian" else "Non-Veg"
                st.markdown(f"""
<div class="meal-card">
  <div class="mc-top">
    <div class="mc-name">{r['name'] or 'Unknown'}</div>
    <div class="mc-score">{int((r['similarity'] or 0)*100)}% match</div>
  </div>
  <div class="mc-desc">{r['description'] or ''}</div>
  <div class="mc-meta">
    <span class="mc-tag {tag_cls}">{tag_text}</span>
    🔥 <b>{r['calories']}</b> kcal &nbsp;·&nbsp;
    💪 <b>{r['protein']}g</b> protein &nbsp;·&nbsp;
    🎯 {r['goal']}
  </div>
</div>""", unsafe_allow_html=True)
        else:
            st.warning("No results. Make sure Endee is running and meals are loaded.")

    # ── Meal plan output ──────────────────────────────────────────────────────
    if generate_btn:
        from rag_engine import generate_meal_plan
        progress = st.progress(0)
        status = st.empty()
        try:
            status.info("Step 1/3 — Searching Endee for matching meals...")
            progress.progress(20)
            with st.spinner("Building your plan..."):
                progress.progress(55)
                result = generate_meal_plan(
                    goal=goal,
                    daily_calories=daily_calories,
                    diet_type=diet_type,
                    allergies=allergies,
                )
                progress.progress(95)
            progress.progress(100)
            status.success("Your plan is ready!")

            st.markdown(f"""
<div class="plan-box">
  <div class="plan-top">
    <div class="plan-top-logo">Diet<span>Logix</span></div>
    <div class="pt-item">Goal<b>{result['goal'].title()}</b></div>
    <div class="pt-item">Target<b>{result['daily_calories']} kcal</b></div>
    <div class="pt-item">Diet<b>{result['diet_type'].title()}</b></div>
    <div class="pt-item">Avoid<b>{allergies}</b></div>
  </div>
  <div class="plan-body">{result['meal_plan'].replace(chr(10), '<br>')}</div>
</div>""", unsafe_allow_html=True)

            with st.expander("See what Endee retrieved (RAG context)"):
                for slot, meals in result["retrieved_meals"].items():
                    st.markdown(f"**{slot.upper()}**")
                    for m in meals:
                        st.markdown(f"- {m['name'] or 'Unknown'} — {m['calories']} kcal · similarity `{m['similarity']}`")

        except EnvironmentError as e:
            progress.empty(); status.empty()
            st.error(str(e))
            st.info("Add GEMINI_API_KEY to your .env file.")
        except Exception as e:
            progress.empty(); status.empty()
            st.error(f"Something went wrong: {e}")
            st.info("1. Endee running → docker compose up -d\n2. Meals loaded → python vector_store.py\n3. API key in .env")

    # ── Default ───────────────────────────────────────────────────────────────
    if not generate_btn and not (search_btn and search_query):
        st.markdown("""
<div class="empty">
    <div class="empty-icon">🥗</div>
    <div class="empty-title">Ready when you are</div>
    <div class="empty-desc">Set your preferences and click Generate — or search the Endee vector DB directly to see similarity scores.</div>
</div>""", unsafe_allow_html=True)
