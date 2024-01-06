from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import re

def get_bert_embeddings(sentences, model, tokenizer):
    # Tokenize input sentences
    tokenized_input = tokenizer(sentences, return_tensors='pt', padding=True, truncation=True)

    # Get BERT embeddings
    with torch.no_grad():
        model_output = model(**tokenized_input)

    # Extract embeddings for [CLS] tokens
    cls_embeddings = model_output.last_hidden_state[:, 0, :]

    return cls_embeddings.numpy()

def calculate_cosine_similarity(embedding1, embedding2):
    # Reshape to (1, embedding_size) for sklearn's cosine_similarity function
    embedding1 = embedding1.reshape(1, -1)
    embedding2 = embedding2.reshape(1, -1)

    # Calculate cosine similarity
    similarity = cosine_similarity(embedding1, embedding2)

    return similarity[0, 0]

def get_matches(text):
    pattern = re.compile(r': (.+)')
    matches = re.findall(pattern, text)
    return matches

def get_similarity_scores(target, matches):
    model_name = 'bert-base-uncased'
    model = BertModel.from_pretrained(model_name)
    tokenizer = BertTokenizer.from_pretrained(model_name)
    embeddings = []

    for sent in matches:
        embedding = get_bert_embeddings(sent, model, tokenizer)
        embeddings.append(embedding)

    target_embedding = get_bert_embeddings(target, model, tokenizer)

    scores = []

    for embedding in embeddings:
        score = calculate_cosine_similarity(target_embedding, embedding)
        scores.append(score)
        print(f"Cosine Similarity Score: {score}")

    return scores
