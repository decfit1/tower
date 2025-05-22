
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title and user input
st.title("Reinsurance Tower: Net vs Ceded Capacity")

# Input for Gross Deployed Line
gross_line = st.number_input("Input Gross Deployed Line (in millions)", min_value=0.0, max_value=75.0, value=60.0, step=0.5)

# Define the R/I structure
layers = [
    {"Layer": "1: First", "Start": 0, "Size": 2.5, "Retention": 1.00},
    {"Layer": "2: Second", "Start": 2.5, "Size": 7.5, "Retention": 1.00},
    {"Layer": "3: Third", "Start": 10, "Size": 7.5, "Retention": 0.50},
    {"Layer": "4: Fourth", "Start": 17.5, "Size": 15, "Retention": 0.15},
    {"Layer": "5: Fifth", "Start": 32.5, "Size": 12.5, "Retention": 0.00},
    {"Layer": "6: Sixth", "Start": 45, "Size": 30, "Retention": 1.00},
]

df = pd.DataFrame(layers)
df["End"] = df["Start"] + df["Size"]

# Calculate exposures
def calculate_exposure(row, gross_line):
    if gross_line <= row["Start"]:
        return 0
    elif gross_line >= row["End"]:
        return row["Size"]
    else:
        return gross_line - row["Start"]

df["Gross Exposed"] = df.apply(lambda row: calculate_exposure(row, gross_line), axis=1)
df["Net Retained"] = df["Gross Exposed"] * df["Retention"]
df["Ceded"] = df["Gross Exposed"] - df["Net Retained"]

# Reverse for tower order
df = df[::-1].reset_index(drop=True)

# Tower View Plot
fig, ax = plt.subplots(figsize=(4, 8))
y_pos = range(len(df))
ax.barh(y_pos, df["Ceded"], color='orange', label="Ceded")
ax.barh(y_pos, df["Net Retained"], left=df["Ceded"], color='steelblue', label="Retained")
ax.set_yticks(y_pos)
ax.set_yticklabels(df["Layer"])
ax.invert_yaxis()
ax.set_xlabel("USD (millions)")
ax.set_title("Tower View by Layer")
ax.legend()
st.pyplot(fig)

# Optional: Show table
st.subheader("Layer Breakdown")
st.dataframe(df[["Layer", "Start", "End", "Gross Exposed", "Net Retained", "Ceded"]].round(2))
