import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Set Streamlit page config
st.set_page_config(page_title="ReviewRadar", page_icon="🛍️", layout="centered")

# Title and banner
st.title("🛍️ ReviewRadar: Sentiment Analysis of Product Reviews on Social Media")
st.markdown("""
This app analyzes the **sentiment** of social media **product reviews** — either individually or in bulk via CSV upload.
Ideal for **brands, e-commerce platforms, or marketing teams** to understand customer perception.
""")

# Sidebar info
st.sidebar.title("Instructions")
st.sidebar.info("Upload any prouct review from social media or load a csv file for sentimental analysis ")

# Tabs: Single Review vs CSV Upload
tab1, tab2 = st.tabs(["🔍 Analyze Review", "📂 Upload Review Dataset"])

# ---- TAB 1: Analyze Review ----
with tab1:
    st.subheader("🔍 Analyze a Single Product Review")
    input_text = st.text_area("Paste a social media product review:")
    if st.button("Analyze Review"):
        if input_text:
            analysis = TextBlob(input_text)
            polarity = analysis.sentiment.polarity
            subjectivity = analysis.sentiment.subjectivity

            # Interpret polarity
            if polarity > 0:
                sentiment = "🙂 Positive"
                st.success(f"Sentiment: {sentiment} ({polarity:.2f})")
            elif polarity < 0:
                sentiment = "☹️ Negative"
                st.error(f"Sentiment: {sentiment} ({polarity:.2f})")
            else:
                sentiment = "😐 Neutral"
                st.info(f"Sentiment: {sentiment} ({polarity:.2f})")

            st.caption(f"Subjectivity: {subjectivity:.2f} (0 = objective, 1 = subjective)")
        else:
            st.warning("Please enter a review to analyze.")

# ---- TAB 2: Upload CSV ----
with tab2:
    st.subheader("📂 Bulk Review Analysis via CSV Upload")
    st.markdown("CSV must contain a column named **'review'** containing product reviews.")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if 'Reviews' not in df.columns:
            st.error("CSV must contain a 'Reviews' column.")
        else:
            st.write("✅ Data Preview:", df.head())

            # Analyze all reviews
            df['polarity'] = df['Reviews'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
            df['sentiment'] = df['polarity'].apply(
                lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral')
            )

            # Sentiment distribution
            st.subheader("📊 Sentiment Distribution")
            sentiment_counts = df['sentiment'].value_counts()
            st.bar_chart(sentiment_counts)

            # Word Cloud
            st.subheader("☁️ Most Common Words in Reviews")
            all_text = ' '.join(df['Reviews'].dropna().astype(str))
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)

            # Line chart of average polarity over time (if timestamp exists)
            if 'timestamp' in df.columns:
                st.subheader("📈 Sentiment Trend Over Time")
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                time_df = df.groupby(df['timestamp'].dt.date)['polarity'].mean()
                st.line_chart(time_df)

            # Pie chart for sentiment proportion
            st.subheader("🧁 Sentiment Proportion (Pie Chart)")
            fig_pie, ax_pie = plt.subplots()
            ax_pie.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90)
            ax_pie.axis('equal')
            st.pyplot(fig_pie)


            # Download analyzed data
            st.download_button(
                label="📥 Download Analyzed Reviews as CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name="analyzed_reviews.csv",
                mime='text/csv'
            )

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | Hackathon Project by Manisha Arutla")
