import pandas as pd

df = pd.read_csv("ProcessedTweets.csv")
month = "March"
sentiment = [.2,.8]
subjectivity = [.2,.5]

filtered_df = df[df["Month"] == month]
filtered_df = filtered_df[filtered_df["Sentiment"] >= sentiment[0]]
filtered_df = filtered_df[filtered_df["Sentiment"] <= sentiment[1]]
filtered_df = filtered_df[filtered_df["Subjectivity"] >= subjectivity[0]]
filtered_df = filtered_df[filtered_df["Subjectivity"] <= subjectivity[1]]

print(type(df["Sentiment"].min().item()))