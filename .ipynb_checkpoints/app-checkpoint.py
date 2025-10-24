import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

st.set_page_config(page_title="Pokémon 2025 Dashboard", page_icon="🐉", layout="wide")

st.title("🐉 Pokémon 2025 Data Dashboard")
st.markdown("""
Explore Pokémon stats interactively.  
Data extracted from *PokeAPI*, analyzed using Pandas, and visualized here with Streamlit.
---
""")

# Load data
with open("data/pokemons.json", "r", encoding="utf-8") as f:
    pokemons = json.load(f)
df = pd.DataFrame(pokemons)

# Normalize columns
if "type_1" in df.columns:
    df["main_type"] = df["type_1"]
elif "type" in df.columns:
    df["main_type"] = df["type"]
elif "types" in df.columns:
    df["main_type"] = df["types"].apply(lambda x: x[0] if isinstance(x, list) and len(x)>0 else "Unknown")
else:
    df["main_type"] = "Unknown"

for col in ["hp","attack","defense","speed"]:
    if col not in df.columns:
        df[col] = 0

df["power_score"] = df["hp"] + df["attack"] + df["defense"]

# Sidebar filters
st.sidebar.header("🔍 Filters")
selected_type = st.sidebar.selectbox("Select Pokémon Type", ["All"] + sorted(df["main_type"].unique()))
min_power = st.sidebar.slider("Minimum Power Score", int(df["power_score"].min()), int(df["power_score"].max()), int(df["power_score"].min()))

filtered_df = df.copy()
if selected_type != "All":
    filtered_df = filtered_df[filtered_df["main_type"] == selected_type]
filtered_df = filtered_df[filtered_df["power_score"] >= min_power]

# Show data table
st.subheader("📋 Pokémon Data Table")
st.dataframe(filtered_df[["name","main_type","hp","attack","defense","speed","power_score"]])

# Strongest Pokémon
st.subheader("💪 Strongest Pokémon")
strongest = filtered_df.loc[filtered_df["power_score"].idxmax()]
st.markdown(f"""
*{strongest['name'].capitalize()}* ({strongest['main_type']} type)  
- HP: {strongest['hp']}  
- Attack: {strongest['attack']}  
- Defense: {strongest['defense']}  
- Power Score: *{strongest['power_score']}*
""")

# Visualizations
st.subheader("📊 Visualizations")

col1, col2 = st.columns(2)

with col1:
    avg_power = filtered_df.groupby("main_type")["power_score"].mean().sort_values(ascending=False)
    if not avg_power.empty:
        fig, ax = plt.subplots(figsize=(6,4))
        sns.barplot(x=avg_power.values, y=avg_power.index, palette="plasma", ax=ax)
        ax.set_title("Average Power by Type")
        st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(6,4))
    sns.scatterplot(data=filtered_df, x="speed", y="power_score", hue="main_type", alpha=0.8)
    ax.set_title("Speed vs Power")
    st.pyplot(fig)

st.markdown("---")
st.caption("Developed by Melike Çırakman • Data Engineer • 2025")