import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime
import os

st.set_page_config(page_title="PokéPipeline 2025", layout="wide")
st.title(" PokéPipeline 2025 – Pokémon Data Explorer")
st.subheader("Summary")

st.markdown("""
This report provides an overview of the Pokémon dataset collected from the public PokeAPI.
A total of 30 Pokémon were analyzed, including information about their attack, defense, and speed
attributes as well as type distribution. 

The analysis shows that Pokémon with higher overall power tend to have balanced attack and defense
statistics rather than extreme values in a single attribute. Speed is more variable and depends strongly
on type classification. 

Among the sampled data, the strongest Pokémon recorded had a total power score of 350,
indicating a high level of offensive and defensive capability. Average attack power across all Pokémon
was approximately 70, while the average defense was around 65. 

This exploratory analysis aims to demonstrate how raw API data can be structured, transformed, and visualized
to highlight key performance metrics and relational patterns across entities.
""")
st.sidebar.header(" Settings")
pokemon_count = st.sidebar.slider("Number of Pokémon to fetch", 10, 100, 30)

@st.cache_data
def fetch_pokemon_data(n=30):
    pokemons = []
    for i in range(1, n+1):
        url = f"https://pokeapi.co/api/v2/pokemon/{i}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            pokemons.append({
                "id": i,
                "name": data["name"].capitalize(),
                "type_1": data["types"][0]["type"]["name"],
                "type_2": data["types"][1]["type"]["name"] if len(data["types"]) > 1 else None,
                "hp": data["stats"][0]["base_stat"],
                "attack": data["stats"][1]["base_stat"],
                "defense": data["stats"][2]["base_stat"],
                "speed": data["stats"][5]["base_stat"]
            })
    return pokemons

if st.button(" Run PokéPipeline"):
    with st.spinner("Fetching Pokémon data..."):
        pokemons = fetch_pokemon_data(pokemon_count)
        df = pd.DataFrame(pokemons)
        st.success(f"{len(df)} Pokémon fetched successfully!")

        os.makedirs("data", exist_ok=True)
        json_path = f"data/pokemons_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(pokemons, f, indent=4)

        df["total_power"] = df["hp"] + df["attack"] + df["defense"] + df["speed"]
        strongest = df.loc[df["total_power"].idxmax()]

        st.subheader(" Strongest Pokémon")
        st.write(f"{strongest['name']}** (Total Power: {strongest['total_power']})")

        st.subheader(" Pokémon Stats Overview")

        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots(figsize=(6,4))
            sns.barplot(data=df, x="name", y="attack", ax=ax, color="orange")
            plt.xticks(rotation=90)
            ax.set_title("Attack Power per Pokémon")
            st.pyplot(fig)

        with col2:
            fig2, ax2 = plt.subplots(figsize=(6,4))
            sns.countplot(data=df, x="type_1", ax=ax2, palette="Set3",
                          order=df["type_1"].value_counts().index)
            plt.xticks(rotation=45)
            ax2.set_title("Distribution by Type")
            st.pyplot(fig2)

        st.subheader(" Summary Table")
        st.dataframe(df)

        report_name = f"Pokemon_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        df.describe().to_html(report_name)
        st.success(f"📄 Report generated: {report_name}")
