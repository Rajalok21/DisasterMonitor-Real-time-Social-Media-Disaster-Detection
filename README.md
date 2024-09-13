# Social Media Disaster News Classifier

# A brief description of what this project does and who it's for


This project scrapes news headlines from Twitter and Instagram using Selenium web scraping, classifies whether the headline relates to a disaster, determines the type of disaster, and extracts the disaster's location if mentioned. The model works for headlines in both English and regional languages, utilizing the Google Translator API for translation. The model achieves an accuracy of 83.889% using a soft voting ensemble of Multinomial Naive Bayes, Logistic Regression, and K-Nearest Neighbors (KNN).

# Features
1. Web Scraping: Automatically fetches headlines from Twitter and Instagram handles.

2. Disaster Classification: Classifies whether a headline is related to a disaster or not.

3. Disaster Type Classification: Determines the type of disaster (e.g., earthquake, flood, fire).

4.Location Extraction: Extracts the location of the disaster if available in the headline.

5.Regional Language Support: Handles headlines in regional 
languages using Google Translator API for translation.

6.Soft Voting Model: Uses an ensemble of Multinomial Naive Bayes, Logistic Regression, and K-Nearest Neighbors to classify headlines.

# Technologies Used
## Web Scraping:
1. Selenium
2. Instaloader
## Machine Learning:
1. NumPy
2. Pandas
3. Scikit-learn
4. NLTK
5. Spacy
## Translation:
1. Google Translator API
## Model Ensemble:
Soft voting ensemble of:

1. Multinomial Naive Bayes
2. Logistic Regression
3. K-Nearest Neighbors (KNN)


# how to run this?

1. Fork this repository
2. install all dependencies and modules from requirements.txt
3. unzip zip compressed files
4. run the app.py file.
5. it will create two txt file


a. featched.txt (contain webscraped news)

b. classified.txt (contain the final classified news)

