# Fintech Choice Drivers NLP: Why Users Leave Traditional Banks 
<img width="980" height="741" alt="image" src="https://github.com/user-attachments/assets/2d318009-feec-4551-a7be-ec485ca7aef7" />
<img width="973" height="497" alt="image" src="https://github.com/user-attachments/assets/eba11423-58e7-4cb5-a536-49fff742bf00" />

An end-to-end Natural Language Processing (NLP) pipeline and competitive intelligence dashboard designed to solve a major blind spot in retail banking: understanding exactly why customers are migrating to digital fintechs.

This project autonomously harvests thousands of app reviews, uses AI to mathematically discover the hidden themes within the text, and visualizes the battleground between Traditional Banks and Digital Lenders.

## The Problem

Traditional banks know their Net Promoter Score (NPS) is dropping, but they often don't know why. Exit surveys are biased, and manually reading 10,000+ app store reviews across multiple competitors is impossible. Executives are left guessing whether they are losing customers due to fees, app stability, customer service, or loan approval speeds.

## Background

The financial landscape is rapidly shifting. Digital fintech apps (like Cash App, PayPal, Tala, or Branch) offer seamless digital onboarding, while legacy banks often struggle with technical debt. Customers leave highly opinionated, unstructured text feedback online. This unstructured text is a goldmine of competitive intelligence—if it can be processed at scale.

## Objective

* To build a fully automated system that:

* Harvests raw, unstructured voice-of-customer data from public app stores.

* Cleans and processes the text using modern NLP techniques.

* Automatically categorizes complaints and praises into distinct, actionable themes without human bias.

* Provides an executive dashboard to compare Traditional Bank performance against Digital Fintechs.

## How We Solve It (System Architecture)

This project is broken down into three core python engines:

1. **review_scraper.py (The Data Harvester)**

* Uses google-play-scraper to legally extract thousands of real customer reviews from global banking and fintech apps.

* Anonymizes and tags the data generically to maintain brand neutrality for portfolio display.

2. **nlp_topic_modeler.py (The AI Engine)**

* **Text Cleaning:** Uses NLTK to remove stop words, punctuation, and domain-specific filler words.

* **Vectorization:** Applies TF-IDF (Term Frequency-Inverse Document Frequency) to convert text into mathematical importance scores.

* **Topic Modeling:** Uses NMF (Non-Negative Matrix Factorization) to mathematically group reviews into 6 distinct competitive themes (e.g., "App Crashes", "Customer Service", "Hidden Fees").

3. **nlp_insights_dashboard.py (The Command Center)**

A high-performance Streamlit application.

Visualizes the NLP output using Plotly, showing exactly which themes dominate the complaints for banks vs. fintechs.

Includes a Qualitative Data Explorer to allow executives to read the raw, categorized reviews.

## Tech Stack

Language: Python 3.x

Data Extraction: google-play-scraper

NLP & Machine Learning: scikit-learn (TF-IDF, NMF), nltk (Natural Language Toolkit)

Data Processing: pandas, numpy, re (RegEx)

Visualization & UI: streamlit, plotly
