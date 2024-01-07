from lda_helper import preprocess_text
from train_lda_model import train_and_save_lda_model, load_lda_model

import pandas as pd

# Load dataset
df = pd.read_csv("dataset.csv")

# Quick character length spam filter
def spam_length_filter(word):
  if not isinstance(word, str): return False
  return len(word) > 50

df['valid'] = df['solution'].apply(spam_length_filter)
df = df[df['valid']]

text_data = df['problem'] + ' ' + df['solution']

# Apply the preprocessing function to each document in the dataset
tokenized_text = text_data.apply(preprocess_text)

# Display the tokenized text for the first document
print(tokenized_text.iloc[0])

# Set parameters
data = tokenized_text
num_topics = 6
lda_model_path = "models/lda_model"

train_and_save_lda_model(data, num_topics, lda_model_path)