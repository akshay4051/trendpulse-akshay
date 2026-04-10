"""

# TrendPulse - Task 1
# Fetch trending stories from HackerNews API and categorize them

# Author: Akshay

"""

# -------------------- library import --------------------

import requests  # api call / data lene ke liye
import json      # json file banana / handle karna
import time      # delay dene ke liye (fast call avoid)
import os        # folder / file handle karne ke liye
from datetime import datetime  # date time ke liye


# -------------------- api url --------------------

TOP_STORIES = "https://hacker-news.firebaseio.com/v0/topstories.json"  # top story id list
ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"  # ek story ka data


# -------------------- header --------------------

headers = {"User-Agent": "TrendPulse/1.0"}  # request safe banane ke liye


# -------------------- category --------------------

CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

MAX_PER_CATEGORY = 25  # har category me max 25 data


# -------------------- category function --------------------

def assign_category(title):
    title_lower = title.lower()  # lowercase me convert

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:  # match mila to
                return category

    return None  # nahi mila to none


# -------------------- main function --------------------

def main():
    try:
        response = requests.get(TOP_STORIES, headers=headers)  # top stories fetch
        story_ids = response.json()[:500]  # sirf 500 id lo
    except Exception as e:
        print("Failed to fetch top stories:", e)
        return

    collected_data = []  # final data store
    category_count = {cat: 0 for cat in CATEGORIES}  # count track
    seen_ids = set()  # duplicate avoid

    print("Collecting stories and categorizing...")


    # -------------------- loop --------------------

    for story_id in story_ids:

        # agar sab category full ho gayi to stop
        if all(count >= MAX_PER_CATEGORY for count in category_count.values()):
            break

        try:
            res = requests.get(ITEM.format(story_id), headers=headers)  # ek story fetch
            story = res.json()

            if not story or "title" not in story:  # title nahi to skip
                continue

            assigned = assign_category(story["title"])  # category assign

            if assigned and category_count[assigned] < MAX_PER_CATEGORY:

                if story_id not in seen_ids:  # duplicate check

                    data = {
                        "post_id": story.get("id"),
                        "title": story.get("title"),
                        "category": assigned,
                        "score": story.get("score", 0),
                        "num_comments": story.get("descendants", 0),
                        "author": story.get("by"),
                        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                    collected_data.append(data)  # data add
                    category_count[assigned] += 1  # count increase
                    seen_ids.add(story_id)  # seen me add

        except Exception as e:
            print(f"Failed to fetch story {story_id}: {e}")

        time.sleep(0.2)  # delay (api safe)


    # -------------------- folder create --------------------

    if not os.path.exists("data"):
        os.makedirs("data")  # folder bana


    # -------------------- save file --------------------

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_data, f, indent=4)

    print(f"\nCollected {len(collected_data)} stories. Saved to {filename}")


# -------------------- run --------------------

if __name__ == "__main__":
    main()
