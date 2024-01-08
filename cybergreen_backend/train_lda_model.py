from lda_helper import preprocess_text
from gensim import corpora, models
import pandas as pd

CONF_THRESHOLD = 0.4
topic_labels = {
  0: "Fashion and Clothing Industry",
  1: "Electronic Waste and Recycling",
  2: "Paper and Energy Conservation",
  3: "Plastic Packaging and Business",
  4: "Packaging and Energy Efficiency",
  5: "Electronic Waste Recycling Platform"
}
num_topics = 6

def train_and_interpret_lda_model(data, num_topics):
    # Create a dictionary and corpus for topic modeling
    dictionary = corpora.Dictionary(data)
    corpus = [dictionary.doc2bow(text) for text in data]

    # Train the LDA (Latent Dirichlet Allocation) model
    # Lower alpha -> Documents are composed of fewer dominant topics
    # Lower eta -> Topics are composed of fewer dominant words
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=20, alpha=0.1, eta=0.1)

    # Save topics and associated words by writing string to file
    # These topics will be interpreted later
    lda_topics_dist = ""

    for topic_id, topic_words in lda_model.print_topics():
        lda_topics_dist += f"Topic {topic_id + 1}: {topic_words}\n"
    
    with open('lda_topics_dist.txt', 'w') as f:
        f.write(lda_topics_dist)

    # Return topics distribution
    return lda_model, lda_topics_dist

def run_lda_training(dataset):
    # Load dataset
    df = pd.read_csv(dataset, encoding='latin-1')

    # Quick character length spam filter
    def spam_length_filter(word):
        if not isinstance(word, str): return False
        return len(word) > 50

    df['valid'] = df['solution'].apply(spam_length_filter)
    df = df[df['valid']]

    text_data = df['problem'] + ' ' + df['solution']

    # Apply the preprocessing function to each document in the dataset
    tokenized_text = text_data.apply(preprocess_text)

    # Set parameters
    data = tokenized_text
    num_topics = 6

    # Train and interpret LDA model
    lda_model, lda_topics_dist = train_and_interpret_lda_model(data, num_topics)

    dictionary = corpora.Dictionary(data)
    corpus = [dictionary.doc2bow(text) for text in data]

    # Assign topics and probabilities to each document in the dataset
    topic_data = [max(lda_model[doc], key=lambda x: x[1]) for doc in lda_model[corpus]]
    df['topic'] = [topic_labels[topic[0]] if topic[1] >= CONF_THRESHOLD else "Other" for topic in topic_data]
    df['topic_probability'] = [topic[1] for topic in topic_data]

    # Save the updated DataFrame to a new CSV file
    updated_csv_path = 'updated_dataset.csv'
    df.to_csv(updated_csv_path, index=False, encoding='utf-8')

    return lda_topics_dist, updated_csv_path

# Example usage
topics_dist, updated_csv_path = run_lda_training("dataset.csv")
print("LDA Topics Distribution:\n", topics_dist)
print("Updated CSV saved at:", updated_csv_path)