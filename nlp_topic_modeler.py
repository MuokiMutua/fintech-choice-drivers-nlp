import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

# Download standard English stop words (only runs the first time)
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('stopwords', quiet=True)

def clean_text(text):
    """
    Cleans raw review text for the machine learning model.
    Converts to lowercase, removes punctuation/numbers, and removes filler words.
    """
    if not isinstance(text, str):
        return ""
    
    # Lowercase and remove punctuation/numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    
    # Remove stop words (the, is, at, which, etc.)
    stop_words = set(stopwords.words('english'))
    # Add domain-specific stop words that don't help us find themes
    custom_stops = {'app', 'bank', 'banking', 'account', 'money', 'use', 'would', 'like', 'get'}
    stop_words = stop_words.union(custom_stops)
    
    words = text.split()
    cleaned_words = [w for w in words if w not in stop_words and len(w) > 2]
    
    return " ".join(cleaned_words)

def run_nlp_pipeline():
    print("Loading raw financial app reviews...")
    try:
        df = pd.read_csv("financial_app_reviews.csv")
    except FileNotFoundError:
        print("Error: Could not find financial_app_reviews.csv. Run the scraper first.")
        return

    # 1. Clean the Text
    print("Cleaning text and removing stop words (this takes a few seconds)...")
    df['Cleaned_Review'] = df['Review_Content'].apply(clean_text)
    
    # Remove empty reviews after cleaning
    df = df[df['Cleaned_Review'].str.strip() != '']

    # 2. Vectorize Text (Convert words into mathematical importance scores using TF-IDF)
    print("Vectorizing text (TF-IDF)...")
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=1000)
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['Cleaned_Review'])
    
    # 3. Topic Modeling (Using NMF - Non-Negative Matrix Factorization)
    # We ask the AI to find exactly 6 distinct themes/topics in the data
    num_topics = 6
    print(f"Running AI Topic Modeling to discover {num_topics} distinct themes...")
    nmf_model = NMF(n_components=num_topics, random_state=42, max_iter=500)
    nmf_matrix = nmf_model.fit_transform(tfidf_matrix)
    
    # 4. Extract Topic Keywords and assign generic names
    feature_names = tfidf_vectorizer.get_feature_names_out()
    topics_dict = {}
    
    print("\n--- DISCOVERED THEMES ---")
    for topic_idx, topic in enumerate(nmf_model.components_):
        # Get the top 7 words for this topic
        top_words_idx = topic.argsort()[:-8:-1]
        top_words = [feature_names[i] for i in top_words_idx]
        
        # We assign a general label based on the index to categorize them in the dashboard
        topic_label = f"Theme {topic_idx + 1}: " + ", ".join(top_words[:3])
        topics_dict[topic_idx] = topic_label
        
        print(f"Topic {topic_idx + 1}: {', '.join(top_words)}")
    
    # 5. Assign the Dominant Topic to each review
    print("\nAssigning themes to individual reviews...")
    df['Dominant_Topic_ID'] = nmf_matrix.argmax(axis=1)
    df['Topic_Name'] = df['Dominant_Topic_ID'].map(topics_dict)
    
    # 6. Save the Analyzed Data
    output_file = "analyzed_reviews.csv"
    df.to_csv(output_file, index=False)
    print(f"\n[✓] NLP pipeline complete. Analyzed data saved to {output_file}")

if __name__ == "__main__":
    run_nlp_pipeline()