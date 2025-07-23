import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('merged_user_track_data.csv')

# Get a random sample of 5000 rows
df_sample = df.sample(n=5000, random_state=42)  # Change n to 1000 or 10000 if you want

# Save to a new CSV
df_sample.to_csv('sample_merged_user_track_data.csv', index=False)
df.columns = df.columns.str.strip()

st.title("Deezer-style Music Analytics Dashboard")
st.markdown("Interactive dashboard analyzing user engagement, top genres/artists, and business KPIs.")

#KPI Table
user_play_dist = df.groupby('user_id')['playcount'].sum().sort_values(ascending=False)
total_plays = user_play_dist.sum()
kpi = {
    'Total Users': df['user_id'].nunique(),
    'Total Tracks': df['track_id'].nunique(),
    'Total Plays': df['playcount'].sum(),
    'Top Genre': df.groupby('genre')['playcount'].sum().idxmax(),
    'Power Users (80/20)': (user_play_dist.cumsum() / total_plays <= 0.8).sum()
}


st.subheader("Business KPIs")
st.write(pd.Series(kpi))

#Top Genres
st.subheader("Top 10 Genres by Playcount")
top_genres = df.groupby('genre')['playcount'].sum().sort_values(ascending=False).head(10)
fig, ax = plt.subplots()
top_genres.plot(kind='bar', color='teal', ax=ax)
plt.xlabel('Genre')
plt.ylabel('Total Plays')
st.pyplot(fig)

#Top Artists
st.subheader("Top 10 Artists by Total Plays")
top_artists = df.groupby('artist')['playcount'].sum().sort_values(ascending=False).head(10)
fig2, ax2 = plt.subplots()
top_artists.plot(kind='barh', color='navy', ax=ax2)
plt.xlabel('Total Plays')
st.pyplot(fig2)

st.markdown("**Summary & Recommendation:**")
st.write("""
- Rock dominates plays, but Electronic/Pop have high engagement—target with personalized playlists.
- 20% of users drive 80% of all plays; engage casual listeners with weekly mixes.
- Product team can use these insights for user retention and feature launches.
""")