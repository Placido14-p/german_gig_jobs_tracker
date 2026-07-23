import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

st.set_page_config(page_title="Berlin Gig Jobs Dashboard", layout="wide")

@st.cache_data(ttl=3600)
def load_data():
    conn = psycopg2.connect(dbname="german_gig_jobs")
    query = """
        SELECT j.titel, j.firma, j.vollzeit, j.verguetungsangabe,
               j.festgehalt, j.gehaltsspanne_von, j.gehaltsspanne_bis,
               j.veroeffentlicht_am, j.quereinstieg_geeignet,
               c.category_name, l.plz, l.ort
        FROM jobs j
        LEFT JOIN categories c ON j.category_id = c.category_id
        LEFT JOIN locations l ON j.location_id = l.location_id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = load_data()

st.title("Berlin Entry-Level & Gig Jobs Dashboard")
st.markdown("Tracking delivery, warehouse, cleaning, and driving job postings via the Bundesagentur fur Arbeit API")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Jobs", len(df))
col2.metric("Unique Employers", df["firma"].nunique())
col3.metric("Categories", df["category_name"].nunique())
col4.metric("Career-Changer Friendly", int(df["quereinstieg_geeignet"].sum()))

st.subheader("Jobs by Category")
category_counts = df["category_name"].value_counts().head(10).reset_index()
category_counts.columns = ["category_name", "count"]
fig1 = px.bar(category_counts, x="count", y="category_name", orientation="h")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Jobs by Postal Code")
location_counts = df[df["plz"] != ""]["plz"].value_counts().head(10).reset_index()
location_counts.columns = ["plz", "count"]
fig2 = px.bar(location_counts, x="plz", y="count")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Average Hourly Pay by Category")
hourly = df[df["verguetungsangabe"] == "STUNDENLOHN"]
pay_by_cat = hourly.groupby("category_name")["festgehalt"].mean().dropna().sort_values(ascending=False).head(10).reset_index()
fig3 = px.bar(pay_by_cat, x="category_name", y="festgehalt", labels={"festgehalt": "Avg Hourly Pay (EUR)"})
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Posting Trend Over Time")
df["month"] = pd.to_datetime(df["veroeffentlicht_am"]).dt.to_period("M").astype(str)
trend = df.groupby("month").size().reset_index(name="count")
fig4 = px.line(trend, x="month", y="count")
st.plotly_chart(fig4, use_container_width=True)
