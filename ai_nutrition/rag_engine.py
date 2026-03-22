"""
rag_engine.py

This is the RAG part of the project. The flow is:
1. Take the user's preferences (goal, calories, diet type)
2. Run semantic searches against Endee for each meal slot
3. Build a prompt using those retrieved meals as context
4. Send to Gemini and get back a personalised meal plan

The key idea is that Gemini only recommends meals that actually
exist in the Endee database — it doesn't make things up.
"""

import os
import google.generativeai as genai
from vector_store import semantic_search

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


def get_gemini():
    if not GEMINI_API_KEY:
        raise EnvironmentError(
            "GEMINI_API_KEY is not set. Add it to your .env file."
        )
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel("gemini-1.5-flash")


def build_search_query(goal: str, diet_type: str, calories: int) -> str:
    """Turn user preferences into a natural language search query for Endee."""
    if calories < 400:
        calorie_label = "low calorie"
    elif calories < 700:
        calorie_label = "moderate calorie"
    else:
        calorie_label = "high calorie"

    return f"{calorie_label} {diet_type} meal for {goal} around {calories} calories high protein"


def generate_meal_plan(
    goal: str,
    daily_calories: int,
    diet_type: str,
    allergies: str = "none",
) -> dict:
    """
    Main function — retrieves meals from Endee and generates a meal plan with Gemini.

    Returns a dict with the retrieved meals, the generated plan text, and the input params.
    """

    # search Endee separately for each meal slot
    # I'm splitting the daily calorie budget roughly across slots
    searches = {
        "breakfast": f"breakfast {diet_type} {goal} {daily_calories // 4} calories",
        "lunch":     f"lunch {diet_type} {goal} {daily_calories // 3} calories",
        "dinner":    f"dinner {diet_type} {goal} {daily_calories // 3} calories",
        "snack":     f"snack {diet_type} {goal} low calorie light",
    }

    retrieved = {}
    for slot, query in searches.items():
        retrieved[slot] = semantic_search(query, top_k=3)

    # flatten retrieved meals into a readable context block for the prompt
    context_lines = []
    for slot, meals in retrieved.items():
        context_lines.append(f"\n{slot.upper()} OPTIONS (retrieved from Endee):")
        for m in meals:
            context_lines.append(
                f"  - {m['name']} | {m['calories']} kcal | {m['protein']}g protein | "
                f"{m['type']} | {m['description']}"
            )
    context = "\n".join(context_lines)

    prompt = f"""You are a nutrition assistant helping someone plan their meals for the day.

USER DETAILS:
- Goal: {goal}
- Daily calorie target: {daily_calories} kcal
- Diet: {diet_type}
- Foods to avoid: {allergies}

MEALS AVAILABLE (retrieved from the Endee vector database):
{context}

Using only the meals listed above, create a one-day meal plan that fits the user's goal and calorie target.

Format your response like this:

🌅 BREAKFAST:
[meal name] — [calories] kcal, [protein]g protein
Why: [one sentence]

☀️ LUNCH:
[meal name] — [calories] kcal, [protein]g protein
Why: [one sentence]

🌙 DINNER:
[meal name] — [calories] kcal, [protein]g protein
Why: [one sentence]

🍎 SNACK:
[meal name] — [calories] kcal, [protein]g protein
Why: [one sentence]

📊 TOTALS:
Calories: X kcal | Protein: Xg | Carbs: Xg | Fat: Xg

💡 NOTE:
[2-3 sentences explaining why this plan fits the user's goal]
"""

    model = get_gemini()
    response = model.generate_content(prompt)

    return {
        "retrieved_meals": retrieved,
        "meal_plan":       response.text,
        "goal":            goal,
        "daily_calories":  daily_calories,
        "diet_type":       diet_type,
    }


if __name__ == "__main__":
    result = generate_meal_plan(
        goal="fat loss",
        daily_calories=1500,
        diet_type="vegetarian",
        allergies="none",
    )
    print(result["meal_plan"])
