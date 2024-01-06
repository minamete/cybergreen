from gensim import corpora, models

def train_and_save_lda_model(data, num_topics, model_path):
   # Create a dictionary and corpus for topic modeling
    dictionary = corpora.Dictionary(data)
    corpus = [dictionary.doc2bow(text) for text in data]

    # Train the LDA (Latent Dirichlet Allocation) model
    # Lower alpha -> Documents are composed of fewer dominant topics
    # Lower eta -> Topics are composed of fewer dominant words
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=20, alpha=0.1, eta=0.1)

    # Save the trained model
    lda_model.save(model_path)

def load_lda_model(model_path):
    # Load the LDA model from the saved file
    lda_model = models.LdaModel.load(model_path)
    return lda_model