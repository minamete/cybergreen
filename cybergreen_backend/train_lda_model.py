from lda_helper import preprocess_text
from gensim import corpora, models

import pandas as pd

def train_and_interpret_lda_model(data, num_topics):
   # Create a dictionary and corpus for topic modeling
    dictionary = corpora.Dictionary(data)
    corpus = [dictionary.doc2bow(text) for text in data]

    # Train the LDA (Latent Dirichlet Allocation) model
    # Lower alpha -> Documents are composed of fewer dominant topics
    # Lower eta -> Topics are composed of fewer dominant words
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=20, alpha=0.1, eta=0.1)

    # Initialize an empty string to store the output
    lda_output_string = ""

    # Save topics and associated words in order to interpret!
    for topic_id, topic_words in lda_model.print_topics():
        lda_output_string += f"Topic {topic_id + 1}: {topic_words}\n"

    return lda_output_string

def run_lda_training(dataset):
    # Load dataset
    df = pd.read_csv(dataset)

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

    return train_and_interpret_lda_model(data, num_topics)