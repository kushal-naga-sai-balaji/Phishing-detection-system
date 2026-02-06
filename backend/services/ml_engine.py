import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

MODEL_PATH = "model.pkl"

# Small embedded dataset for demonstration/bootstrapping
# In a real system, this would be loaded from a large CSV
TRAIN_DATA = [
    # Phishing / Bad
    ("http://secure-login-update.com", "phishing"),
    ("http://verify-account-security.net", "phishing"),
    ("http://apple-id-reset.urgent.com", "phishing"),
    ("http://paypal-verification-needed.com", "phishing"),
    ("free-prize-winner.com/claim-now", "phishing"),
    ("urgent: your account will be suspended", "phishing"),
    ("verify your banking details immediately", "phishing"),
    ("click here to claim your lottery winning", "phishing"),
    ("login to update your password", "phishing"),
    ("your netflix subscription is on hold", "phishing"),
    
    # Safe / Good
    ("https://google.com", "safe"),
    ("https://github.com", "safe"),
    ("https://stackoverflow.com", "safe"),
    ("https://python.org", "safe"),
    ("https://amazon.com", "safe"),
    ("meeting agenda for next week", "safe"),
    ("reminder: doctor appointment tomorrow", "safe"),
    ("check out this cool article", "safe"),
    ("project status update", "safe"),
    ("can we reschedule our call?", "safe")
]

model_pipeline = None

def train_model():
    """Trains a simple Naive Bayes model on the embedded dataset."""
    global model_pipeline
    print("Training ML model on embedded dataset...")
    
    X = [item[0] for item in TRAIN_DATA]
    y = [item[1] for item in TRAIN_DATA]
    
    # Create a pipeline that converts text to features and then trains a classifier
    model_pipeline = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model_pipeline.fit(X, y)
    
    # Save the model
    joblib.dump(model_pipeline, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

def load_model():
    """Loads the model from disk, or trains it if missing."""
    global model_pipeline
    if os.path.exists(MODEL_PATH):
        try:
            model_pipeline = joblib.load(MODEL_PATH)
            print("ML Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            train_model()
    else:
        train_model()

def predict_text(text: str) -> dict:
    """Predicts if text is phishing or safe."""
    global model_pipeline
    if model_pipeline is None:
        load_model()
        
    prediction = model_pipeline.predict([text])[0]
    probabilities = model_pipeline.predict_proba([text])[0]
    
    # probabilities is [prob_class_0, prob_class_1]
    # We need to know which class is which. 
    # classes_ attribute of the classifier step stores labels.
    classes = model_pipeline.named_steps['multinomialnb'].classes_
    
    # Find probability of the predicted class
    prob_score = 0.0
    for cls, prob in zip(classes, probabilities):
        if cls == prediction:
            prob_score = prob
            
    return {
        "label": prediction,
        "confidence": float(prob_score)
    }

if __name__ == "__main__":
    # Test training when run directly
    train_model()
    print("Test Prediction for 'google.com':", predict_text("google.com"))
    print("Test Prediction for 'verify-bank-now.com':", predict_text("verify-bank-now.com"))
