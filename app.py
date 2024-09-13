import pickle
import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from classifier_model import translate
from classifier_model import location_fetch
from news_fetch import all_news_fetch

# Fetching news from social media
usernames = ["priyanshu_pilaniwala"]
twitter_url = "https://x.com/IndiaToday"
count = 5
csv_filename = "fetched.csv"

all_news_fetch.fetch(twitter_url,csv_filename)
all_news_fetch.scrape_instagram_data(usernames, count, csv_filename)

ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

def transform_text(text):
    text = text.lower()
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)  
    words = text.split()
    filtered_words = [ps.stem(word) for word in words if word not in stop_words]
    return " ".join(filtered_words)

# Load the pre-trained vectorizer and model
cv = pickle.load(open('C://Users//samsung//Desktop//hackheritage models//newsclassifier//classifier_model//vectorizer.pkl', 'rb'))
model = pickle.load(open('C://Users//samsung//Desktop//hackheritage models//newsclassifier//classifier_model//model.pkl', 'rb'))
loaded_pipeline = pickle.load(open('C://Users//samsung//Desktop//hackheritage models//newsclassifier//classifier_model//disaster_classifier.pkl', 'rb'))

def classify_with_threshold(text, threshold=0.6):
    # Translate to English
    translated_text = translate.translate_to_english(text)
    
    # Preprocess
    transformed_sms = transform_text(translated_text)
    
    # Vectorize
    vector_input = cv.transform([transformed_sms])
    
    # Get prediction probabilities
    probas = model.predict_proba(vector_input)
    
    # Apply the threshold
    is_disaster = 1 if probas[0][1] >= threshold else 0
    
    # Optionally use the loaded pipeline for additional classification if necessary
    disaster_class = loaded_pipeline.predict([translated_text])[0] if is_disaster == 1 else None
    
    # Example location fetch (assuming a function exists)
    location = location_fetch.loc_fetch2(text) if is_disaster == 1 else None
    
    return {
        'Is_Disaster': 'Yes' if is_disaster == 1 else 'No',
        'Disaster_Class': disaster_class,
        'Location': location
    }

# Load the CSV file
df = pd.read_csv('fetched.csv')

# Initialize new columns
df['Is_Disaster'] = ''
df['Disaster_Class'] = ''
df['Location'] = ''

# Process each row in the 'news' column
for index, row in df.iterrows():
    input_text = row['news']
    
    # Classify with a threshold
    result = classify_with_threshold(input_text, threshold=0.3)
    
    # Update DataFrame
    df.at[index, 'Is_Disaster'] = result['Is_Disaster']
    df.at[index, 'Disaster_Class'] = result['Disaster_Class']
    df.at[index, 'Location'] = result['Location']

# Save the updated DataFrame back to a CSV file
df.to_csv('classified.csv', index=False)
