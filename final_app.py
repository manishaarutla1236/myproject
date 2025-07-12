import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Finance News Sentiment Analyzer", layout="wide")

# Title
st.title("📊 Finance News Sentiment Analyzer")
st.markdown("Analyze whether finance news headlines are 🔴 Negative, 🟡 Neutral, or 🟢 Positive.")

# Sidebar Info
st.sidebar.title("⚙️ Instructions")
st.sidebar.markdown("""
1. Upload a CSV file with a column named `headline`.  
2. The app will detect the sentiment using **TextBlob**.  
3. View table, charts, and download the results.
""")

# File uploader
uploaded_file = st.file_uploader("📁 Upload CSV file with 'headline' column", type=["csv"])

# Sentiment analysis function
def get_sentiment(text):
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# When a file is uploaded
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        if 'headline' not in df.columns:
            st.error("❌ CSV must contain a column named 'headline'")
        else:
            with st.spinner("Analyzing Sentiment..."):
                df["Polarity"] = df["headline"].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
                df["Sentiment"] = df["headline"].apply(get_sentiment)

            st.success("✅ Sentiment analysis completed!")

            # Display results
            st.subheader("📄 Analysis Table")
            st.dataframe(df)

            # Pie Chart
            st.subheader("🧁 Sentiment Distribution (Pie Chart)")
            sentiment_counts = df["Sentiment"].value_counts()
            fig1, ax1 = plt.subplots()
            ax1.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)

            # Bar Chart
            st.subheader("📊 Sentiment Count (Bar Chart)")
            st.bar_chart(sentiment_counts)

            # Download results
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Results as CSV", data=csv, file_name="analyzed_sentiment.csv", mime='text/csv')

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
else:
    st.info("👈 Upload a CSV file to begin.")
