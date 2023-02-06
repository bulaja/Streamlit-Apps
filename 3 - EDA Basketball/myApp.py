import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title("NBA Player Stats Explorer")

st.markdown(
    """
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit, seaborn
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
"""
)

st.sidebar.header("User Input Features")
selected_year = st.sidebar.selectbox("Year", list(reversed(range(1950, 2022))))

# Web scraping of NBA player stats
@st.cache
def load_data(year):
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
    # "https://www.basketball-reference.com/leagues/NBA_2021_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == "Age"].index)  # Deletes repeating headers in content

    # Set the type of each column to str to address issues like below.
    # streamlit.errors.StreamlitAPIException: (
    # "Expected bytes, got a 'int' object", 'Conversion failed for column FG% with type object')

    raw = raw.astype(str)
    raw = raw.fillna(0)

    player_stats = raw.drop(["Rk"], axis=1)
    return player_stats


player_stats = load_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(player_stats.Tm.unique())
selected_team = st.sidebar.multiselect("Team", sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = ["C", "PF", "SF", "PG", "SG"]
selected_pos = st.sidebar.multiselect("Position", unique_pos, unique_pos)

# Filtering data
df_selected_team = player_stats[
    (player_stats.Tm.isin(selected_team)) & (player_stats.Pos.isin(selected_pos))
]

st.header("Display Player Stats of Selected Team(s)")
st.write(
    "Data Dimension: "
    + str(df_selected_team.shape[0])
    + " rows and "
    + str(df_selected_team.shape[1])
    + " columns."
)

# Format columns
string_cols = ['Player', 'Pos', 'Tm']
df_selected_team[string_cols] = df_selected_team[string_cols].astype(str)

int_cols = ['Age', 'G', 'GS'] 
df_selected_team[int_cols] = df_selected_team[int_cols].astype(int)

float_cols = df_selected_team.columns[~df_selected_team.columns.isin(string_cols + int_cols)]
df_selected_team[float_cols] = df_selected_team[float_cols].astype(float)

st.dataframe(df_selected_team.style.format(subset = float_cols, formatter = '{:.2f}'))

# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def file_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

# TODO: Fix download format for % stats
st.markdown(file_download(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.button("Intercorrelation Heatmap"):
    st.header("Intercorrelation Matrix Heatmap")
    df_selected_team.to_csv("output.csv", index=False)
    df = pd.read_csv("output.csv")

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(f)