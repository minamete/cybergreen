from train_lda_model import train_and_save_lda_model, load_lda_model

import pandas as pd

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.metrics.distance import jaccard_distance
from nltk.util import ngrams
from nltk.corpus import words

import string

# Download NLTK resources
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
# nltk.download('words')

# Load dataset
df = pd.read_csv("dataset.csv")

# Quick character length spam filter
def spam_length_filter(word):
  if not isinstance(word, str): return False
  return len(word) > 50

df['valid'] = df['solution'].apply(spam_length_filter)
df = df[df['valid']]

text_data = df['problem'] + ' ' + df['solution']

custom_stopwords = ['circular', 'economy', 'problem', 'solution', 'business', 'would', 'could', 'also', 'waste', 'environmental', 'sustainability']

def preprocess_text(text):
    # Check for NaN values
    if pd.isnull(text):
      return []

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stop words
    stop_words = set(stopwords.words('english') + custom_stopwords)
    tokens = [token for token in tokens if token not in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return tokens

# Apply the preprocessing function to each document in the dataset
tokenized_text = text_data.apply(preprocess_text)

# Display the tokenized text for the first document
print(tokenized_text.iloc[0])

# Set parameters
data = tokenized_text
num_topics = 6
model_path = "models/lda_model"

train_and_save_lda_model(data, num_topics, model_path)

loaded_lda_model = load_lda_model(model_path)

# Print topics and associated words
for topic_id, topic_words in loaded_lda_model.print_topics():
    print(f"Topic {topic_id + 1}: {topic_words}")