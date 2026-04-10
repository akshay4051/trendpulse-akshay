"""

# TrendPulse - Task 2
# Load JSON data, clean it and save as CSV

# Author: Akshay

"""

# -------------------- import --------------------

import pandas as pd  # data handle ke liye
import os            # file / folder ke liye


# -------------------- file load --------------------

file_path = "data/trends_20260410.json"  # input file

try:
    df = pd.read_json(file_path)  # json load
    print(f"Loaded {len(df)} stories from {file_path}")
except Exception as e:
    print("Error loading file:", e)
    exit()


# -------------------- cleaning --------------------

# duplicate remove (same post id)
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")


# null values remove
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")


# data type fix
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)


# low quality data remove (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")


# title clean (extra space remove)
df["title"] = df["title"].str.strip()


# -------------------- save file --------------------

if not os.path.exists("data"):
    os.makedirs("data")  # folder bana

output_file = "data/trends_clean.csv"

df.to_csv(output_file, index=False)  # csv save

print(f"\nSaved {len(df)} rows to {output_file}")


# -------------------- analysis --------------------

print("\nStories per category:")
print(df["category"].value_counts())  # category count

