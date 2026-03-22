"""
vector_store.py

This file handles everything related to Endee — creating the index,
embedding meals, storing them, and running semantic searches.

I'm using sentence-transformers to convert text into 384-dim vectors,
then storing those in Endee with the meal metadata attached.
"""

import json
import os
from typing import List, Dict, Any

from sentence_transformers import SentenceTransformer
from endee import Endee, Precision

# change ENDEE_HOST if you're running Endee on a different port
ENDEE_HOST  = os.getenv("ENDEE_HOST", "http://localhost:8081")
ENDEE_TOKEN = os.getenv("ENDEE_TOKEN", "")
INDEX_NAME  = "nutri_meals"
EMBED_MODEL = "all-MiniLM-L6-v2"
VECTOR_DIM  = 384
DATA_PATH   = os.path.join(os.path.dirname(__file__), "data", "meals.json")


def get_client() -> Endee:
    client = Endee(ENDEE_TOKEN) if ENDEE_TOKEN else Endee()
    client.set_base_url(f"{ENDEE_HOST}/api/v1")
    return client


# load the model once and reuse it
_model: SentenceTransformer | None = None

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        print(f"Loading embedding model: {EMBED_MODEL}")
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def embed_text(text: str) -> List[float]:
    """Turn a string into a 384-dim vector."""
    vector = get_model().encode(text, normalize_embeddings=True)
    return vector.tolist()


def meal_to_text(meal: Dict[str, Any]) -> str:
    """
    Build a rich text string from a meal's fields.
    The richer the text, the better the semantic search results.
    I'm including goal, diet type, and macros so the embeddings
    capture nutritional context, not just the meal name.
    """
    return (
        f"{meal['name']}. "
        f"{meal['description']} "
        f"Goal: {meal['goal']}. "
        f"Diet: {meal['type']}. "
        f"Meal time: {meal['meal_time']}. "
        f"Calories: {meal['calories']} kcal. "
        f"Protein: {meal['protein']}g. "
        f"Carbs: {meal['carbs']}g. "
        f"Fat: {meal['fat']}g."
    )


def ensure_index(client: Endee) -> None:
    """
    Create the Endee index if it doesn't exist yet.
    If it already exists, just skip — upsert will handle updates.
    """
    try:
        client.create_index(
            name=INDEX_NAME,
            dimension=VECTOR_DIM,
            space_type="cosine",
            precision=Precision.INT8,
        )
        print(f"Index '{INDEX_NAME}' created.")
    except Exception:
        print(f"Index '{INDEX_NAME}' already exists, skipping creation.")


def load_and_store_meals() -> None:
    """
    Read meals.json, embed each meal, and store in Endee.
    Safe to run multiple times — upsert won't create duplicates.
    """
    client = get_client()
    ensure_index(client)
    index = client.get_index(name=INDEX_NAME)

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        meals: List[Dict] = json.load(f)

    print(f"Embedding and storing {len(meals)} meals...")
    vectors = []
    for meal in meals:
        text = meal_to_text(meal)
        vector = embed_text(text)
        vectors.append({
            "id": meal["id"],
            "vector": vector,
            "meta": {
                "name":        meal["name"],
                "calories":    meal["calories"],
                "protein":     meal["protein"],
                "carbs":       meal["carbs"],
                "fat":         meal["fat"],
                "type":        meal["type"],
                "goal":        meal["goal"],
                "meal_time":   meal["meal_time"],
                "description": meal["description"],
            },
        })

    index.upsert(vectors)
    print(f"Done — {len(vectors)} meals stored in Endee.")


def semantic_search(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Embed the query and search Endee for the closest meals.
    Returns a list of meals with their similarity scores and metadata.
    """
    client = get_client()
    index = client.get_index(name=INDEX_NAME)
    query_vector = embed_text(query)

    results = index.query(vector=query_vector, top_k=top_k)

    meals_found = []
    for r in results:
        meta = r.get("meta", {}) if isinstance(r, dict) else {}
        similarity = r.get("similarity", 0) if isinstance(r, dict) else getattr(r, "similarity", 0)
        meals_found.append({
            "name":        meta.get("name", ""),
            "similarity":  round(float(similarity), 4),
            "calories":    meta.get("calories"),
            "protein":     meta.get("protein"),
            "carbs":       meta.get("carbs"),
            "fat":         meta.get("fat"),
            "type":        meta.get("type"),
            "goal":        meta.get("goal"),
            "meal_time":   meta.get("meal_time"),
            "description": meta.get("description"),
        })
    return meals_found


if __name__ == "__main__":
    load_and_store_meals()
    print("\nTesting semantic search...")
    results = semantic_search("high protein vegetarian meal for muscle gain", top_k=3)
    for i, meal in enumerate(results, 1):
        print(f"\n#{i} {meal['name']} (similarity: {meal['similarity']})")
        print(f"    {meal['calories']} kcal | Protein: {meal['protein']}g | {meal['type']}")
