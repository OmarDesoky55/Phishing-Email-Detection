import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Import the Dataset
df= pd.read_csv("Phishing_Email.csv")
df.head()

# Check NAN values
df.isna().sum()

#Drop tha Na values
df = df.dropna()
print(df.isna().sum())

#dataset shape
df.shape

# Count the occurrences of each E-mail type.
email_type_counts = df['Email Type'].value_counts()
print(email_type_counts)

# Create the bar chart
# Create a list of unique email types
unique_email_types = email_type_counts.index.tolist()

# Define a custom color map
color_map = {
    'Phishing Email': 'red',
    'Safe Email': 'green',}

# Map the colors to each email type
colors = [color_map.get(email_type, 'gray') for email_type in unique_email_types]

# Create the bar chart with custom colors
plt.figure(figsize=(8, 6))
plt.bar(unique_email_types, email_type_counts, color=colors)
plt.xlabel('Email Type')
plt.ylabel('Count')
plt.title('Distribution of Email Types with Custom Colors')
plt.xticks(rotation=45)

# Show the chart
plt.tight_layout()
plt.show()

# We will use undersapling technique
Safe_Email = df[df["Email Type"]== "Safe Email"]
Phishing_Email = df[df["Email Type"]== "Phishing Email"]
Safe_Email = Safe_Email.sample(Phishing_Email.shape[0])

# lets check the sahpe again
Safe_Email.shape,Phishing_Email.shape

# lest create a new Data with the balanced E-mail types
Data= pd.concat([Safe_Email, Phishing_Email], ignore_index = True)
Data.head()

# split the data into a metrix of features X and Dependent Variable y
X = Data["Email Text"].values
y = Data["Email Type"].values

# lets splitting Our Data
from sklearn.model_selection import train_test_split
X_train,x_test,y_train,y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)

# Importing Libraries for the model ,Tfidf and Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

# define the Classifier
classifier = Pipeline([("tfidf",TfidfVectorizer() ),("classifier",RandomForestClassifier(n_estimators=10))])# add another hyperparamters as U want

# Trian Our model
classifier.fit(X_train,y_train)

# Prediction
y_pred = classifier.predict(x_test)

# Importing classification_report,accuracy_score,confusion_matrix
from sklearn.metrics import classification_report,accuracy_score,confusion_matrix

#accuracy_score
accuracy_score(y_test,y_pred)

#confusion_matrix
confusion_matrix(y_test,y_pred)

#classification_report
classification_report(y_test,y_pred)

# This function is for Checking the type of Email (Safe or Phishing)!
def predict_email_type(email_text):
    prediction = classifier.predict([email_text])[0]
    probabilities = classifier.predict_proba([email_text])[0]
    phishing_prob = probabilities[0] * 100  # Probability of 'Phishing Email'
    safe_prob = probabilities[1] * 100      # Probability of 'Safe Email'

    if prediction == 'Phishing Email':
        print(f"The email is classified as: {prediction} with {phishing_prob:.2f}% confidence.")
    else:
        print(f"The email is classified as: {prediction} with {safe_prob:.2f}% confidence.")
    return prediction

# Example usage of the function
email_text = input("Enter Email Text to Check if it's Safe or Not ---->   ")
result = predict_email_type(email_text)











