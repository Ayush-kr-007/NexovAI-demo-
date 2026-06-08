import streamlit as st
import sqlite3
from pymongo import MongoClient
import pandas as pd
import os

st.set_page_config(
    page_title="NexovAI Dashboard",
    page_icon="📞",
    layout="wide"
)

# Database
client = MongoClient(os.getenv("MONGO_URI"))

db = client["nexovai"]

leads = list(
    db["leads"].find({}, {"_id": 0})
)

df = pd.DataFrame(leads)

st.title("📞 NexovAI Lead Dashboard")

# ----------------------------
# SIDEBAR
# ----------------------------

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Call Lead"]
)

# ----------------------------
# DASHBOARD PAGE
# ----------------------------

if page == "Dashboard":

    total_leads = len(df)

    warm_leads = len(
        df[df["lead_type"] == "WARM"]
    ) if "lead_type" in df.columns else 0

    cold_leads = len(
        df[df["lead_type"] == "COLD"]
    ) if "lead_type" in df.columns else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Leads", total_leads)
    col2.metric("Warm Leads", warm_leads)
    col3.metric("Cold Leads", cold_leads)

    st.divider()

    if len(df) > 0:

        lead_id = st.selectbox(
            "Select Lead",
            df["id"]
        )

        selected = df[df["id"] == lead_id].iloc[0]

        st.subheader("Lead Details")

        if "industry" in selected.index:
            st.write(f"**Industry:** {selected['industry']}")

        if "daily_calls" in selected.index:
            st.write(f"**Daily Calls:** {selected['daily_calls']}")

        if "call_handling" in selected.index:
            st.write(f"**Call Handling:** {selected['call_handling']}")

        if "interest" in selected.index:
            st.write(f"**Interest:** {selected['interest']}")

        if "budget" in selected.index:
            st.write(f"**Budget:** {selected['budget']}")

        if "timeline" in selected.index:
            st.write(f"**Timeline:** {selected['timeline']}")

        if "score" in selected.index:
            st.write(f"**Score:** {selected['score']}")

        if "lead_type" in selected.index:
            st.write(f"**Lead Type:** {selected['lead_type']}")

    st.divider()

    st.subheader("Call History")

    st.dataframe(
        df.sort_values(
            "id",
            ascending=False
        ),
        use_container_width=True
    )

    st.divider()

    if "lead_type" in df.columns:

        st.subheader("Lead Distribution")

        lead_counts = (
            df["lead_type"]
            .value_counts()
        )

        st.bar_chart(lead_counts)

    if "industry" in df.columns:

        st.subheader("Industry Distribution")

        industry_counts = (
            df["industry"]
            .value_counts()
        )

        st.bar_chart(industry_counts)

# ----------------------------
# CALL PAGE
# ----------------------------

if page == "Call Lead":

    st.title("📞 AI Sales Caller")

    number = st.text_input(
        "Prospect Phone Number"
    )

    if st.button("Start Call"):

        if number.strip():

            st.success(
                f"Opening AI caller for {number}"
            )

            st.link_button(
                "Launch AI Caller",
                "http://localhost:7860/client/"
            )

            st.info(
                "Complete the conversation and return to the dashboard."
            )

        else:

            st.warning(
                "Please enter a phone number."
            )