from gensim import corpora, models

def train_and_save_lda_model(data, num_topics, lda_model_path):
   # Create a dictionary and corpus for topic modeling
    dictionary = corpora.Dictionary(data)
    corpus = [dictionary.doc2bow(text) for text in data]

    # Train the LDA (Latent Dirichlet Allocation) model
    # Lower alpha -> Documents are composed of fewer dominant topics
    # Lower eta -> Topics are composed of fewer dominant words
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=20, alpha=0.1, eta=0.1)

    # Print topics and associated words in order to interpret!
    for topic_id, topic_words in lda_model.print_topics():
        print(f"Topic {topic_id + 1}: {topic_words}")

    # Save the trained model
    lda_model.save(lda_model_path)

def load_lda_model(lda_model_path):
    # Load the LDA model from the saved file
    lda_model = models.LdaModel.load(lda_model_path)
    return lda_model