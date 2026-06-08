import streamlit as st
from pymongo import MongoClient
import pandas as pd
import os

st.set_page_config(
    page_title="NexovAI Dashboard",
    page_icon="📞",
    layout="wide"
)

# MongoDB
client = MongoClient(st.secrets["MONGO_URI"])
db = client["nexovai"]

leads = list(db["leads"].find())

df = pd.DataFrame(leads)

if "_id" in df.columns:
    df["_id"] = df["_id"].astype(str)

st.title("📞 NexovAI Lead Dashboard")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Call Lead"]
)

# ==========================
# DASHBOARD
# ==========================

if page == "Dashboard":

    total_leads = len(df)

    warm_leads = len(df[df["lead_type"] == "WARM"]) if "lead_type" in df.columns else 0
    cold_leads = len(df[df["lead_type"] == "COLD"]) if "lead_type" in df.columns else 0

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Leads", total_leads)
    c2.metric("Warm Leads", warm_leads)
    c3.metric("Cold Leads", cold_leads)

    st.divider()

    if len(df) > 0:

        selected_id = st.selectbox(
            "Select Lead",
            df["_id"]
        )

        selected = df[df["_id"] == selected_id].iloc[0]

        st.subheader("Lead Details")

        for field in [
            "call_handling",
            "daily_calls",
            "industry",
            "interest",
            "budget",
            "timeline",
            "score",
            "lead_type"
        ]:
            if field in selected.index:
                st.write(f"**{field.replace('_',' ').title()}:** {selected[field]}")

    st.divider()

    st.subheader("Call History")

    st.dataframe(
        df,
        use_container_width=True
    )

    if "lead_type" in df.columns:
        st.subheader("Lead Distribution")
        st.bar_chart(df["lead_type"].value_counts())

# ==========================
# CALL PAGE
# ==========================

if page == "Call Lead":

    st.title("📞 AI Sales Caller")

    number = st.text_input("Prospect Phone Number")

    if st.button("Start Call"):

        if number:

            st.success(
                f"Opening AI caller for {number}"
            )

            st.link_button(
                "Launch AI Caller",
                "http://localhost:7860/client/"
            )

        else:
            st.warning(
                "Please enter a phone number"
            )