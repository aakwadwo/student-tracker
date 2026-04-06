from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle

# Training data — descriptions and their categories
training_data = [
    # AI
    ("machine learning model for predictions", "AI"),
    ("neural network for image recognition", "AI"),
    ("AI chatbot for customer support", "AI"),
    ("deep learning system for healthcare", "AI"),
    ("natural language processing pipeline", "AI"),
    ("computer vision object detection", "AI"),
    ("AI system for fraud detection", "AI"),
    ("recommendation engine using ML", "AI"),
    ("sentiment analysis tool", "AI"),
    ("AI model for stock prediction", "AI"),

    # Web
    ("ecommerce website with payment integration", "Web"),
    ("portfolio website with React", "Web"),
    ("REST API for user authentication", "Web"),
    ("blog platform with CMS", "Web"),
    ("social media app with real time chat", "Web"),
    ("online booking system for appointments", "Web"),
    ("dashboard for managing users", "Web"),
    ("web scraper for collecting data", "Web"),
    ("fullstack app with database", "Web"),
    ("landing page with contact form", "Web"),

    # Data Science
    ("data analysis of sales trends", "Data Science"),
    ("visualization dashboard for business metrics", "Data Science"),
    ("statistical analysis of survey results", "Data Science"),
    ("exploratory data analysis on dataset", "Data Science"),
    ("data pipeline for cleaning and processing", "Data Science"),
    ("predictive analytics for business forecasting", "Data Science"),
    ("clustering analysis of customer segments", "Data Science"),
    ("time series analysis of financial data", "Data Science"),
    ("report generation from database queries", "Data Science"),
    ("data mining for patterns in logs", "Data Science"),

    # Mobile
    ("android app for tracking fitness", "Mobile"),
    ("iOS app for food delivery", "Mobile"),
    ("cross platform mobile app with flutter", "Mobile"),
    ("mobile game with leaderboard", "Mobile"),
    ("react native app for social networking", "Mobile"),
    ("mobile app for scanning QR codes", "Mobile"),
    ("push notification system for mobile", "Mobile"),
    ("offline mobile app for note taking", "Mobile"),
    ("mobile wallet payment app", "Mobile"),
    ("location tracking app for delivery", "Mobile"),
]

descriptions = [item[0] for item in training_data]
labels       = [item[1] for item in training_data]

# Build pipeline: TF-IDF vectorizer + Naive Bayes classifier
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", MultinomialNB())
])

model.fit(descriptions, labels)

# Save model to disk
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved as model.pkl")

# Quick test
test_cases = [
    "AI system for healthcare",
    "website for online shopping",
    "analysis of student performance data",
    "mobile app for learning"
]

for test in test_cases:
    prediction = model.predict([test])[0]
    print(f"  '{test}' → {prediction}")