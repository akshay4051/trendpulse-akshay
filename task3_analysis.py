"""

# TrendPulse - Task 3
# Analyze cleaned CSV using Pandas and NumPy

# Author: Akshay

"""

# -------------------- import --------------------

import pandas as pd  # data handle
import numpy as np   # stats ke liye
import os            # file / folder


# -------------------- load data --------------------

file_path = "data/trends_clean.csv"

try:
    df = pd.read_csv(file_path)  # csv load
    print(f"Loaded data: {df.shape}")
except Exception as e:
    print("Error loading file:", e)
    exit()


# -------------------- basic check --------------------

print("\nFirst 5 rows:")
print(df.head())  # top 5 data


# -------------------- pandas stats --------------------

avg_score = df["score"].mean()  # avg score
avg_comments = df["num_comments"].mean()  # avg comments

print(f"\nAverage score   : {avg_score:.2f}")
print(f"Average comments: {avg_comments:.2f}")


# -------------------- numpy stats --------------------

scores = df["score"].values  # numpy array

mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)

print("\n--- NumPy Stats ---")
print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")
print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")


# -------------------- category analysis --------------------

category_counts = df["category"].value_counts()  # count per category
top_category = category_counts.idxmax()  # max category
top_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")


# -------------------- most commented --------------------

max_comments_row = df.loc[df["num_comments"].idxmax()]

print(f'\nMost commented story: "{max_comments_row["title"]}" — {max_comments_row["num_comments"]} comments')


# -------------------- new columns --------------------

# engagement = comments / (score + 1)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# popular hai ya nahi (avg se compare)
df["is_popular"] = df["score"] > avg_score


# -------------------- save file --------------------

if not os.path.exists("data"):
    os.makedirs("data")

output_file = "data/trends_analysed.csv"

df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")

