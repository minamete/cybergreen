from gensim.models.ldamodel import LdaModel

import string
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.metrics.distance import jaccard_distance
from nltk.util import ngrams
from nltk.corpus import words

# Download packages if necessary
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('words')

def preprocess_text(text):
    custom_stopwords = ['circular', 'economy', 'problem', 'solution', 'model', 'business', 'would', 'could', 'also', 'waste', 'environmental', 'sustainability']

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

# ---------------------------------------------------------------------
# DON'T USE

# Requires a trained LDA model to input
def classify_new_input(lda_model, new_input, topic_labels, conf_threshold=0.5):
    tokenized_input = preprocess_text(new_input) 
   
    # Create a bag-of-words representation
    input_bow = lda_model.id2word.doc2bow(tokenized_input)

    # Use the loaded model to get the topic distribution for the input
    topic_distribution = lda_model[input_bow]

    # Extract the dominant topic and its probability
    dominant_topic = max(topic_distribution, key=lambda x: x[1])
    topic_id, topic_prob = dominant_topic

    # Classify based on the confidence threshold
    if topic_prob >= conf_threshold:
        topic_label = topic_labels[topic_id]
    else:
        topic_label = "Other"

    return {
        "topic_label": topic_label,
        "topic_probability": topic_prob,
        "topic_id": topic_id,
    }
