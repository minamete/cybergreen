from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import re
from chat_fe import get_openai_response

from keywords import get_top_keywords

# scores 1 - 10
# novelty
# feasiblity 
# environmental impact
# restart backend

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
    keywords = get_top_keywords(text)

    prompt = "what are 10 commonly discussed solutions to combat the environmental problem of " + keywords[0] + " and " + keywords[1]

    response = [get_openai_response(prompt)]
    response_str = ' '.join(response)
    pattern = re.compile(r': (.+)')

    print("Response: ", response)

    matches = re.findall(pattern, response_str)
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

def get_novelty_score(problem, solution):
    matches = get_matches(problem)
    similarity_scores = get_similarity_scores(solution, matches)

    max_similarity = max(similarity_scores)
    inv = 10 - (max_similarity * 10)

    index = similarity_scores.index(max_similarity)

    print("The solution with the highest similarity is:", matches[index])

    print("score:", inv)

    return inv


print(get_novelty_score("On a global scale, massive amounts of food gets wasted at a shocking rate. This is particularly prominent in the restaurant and fast-food industry where surplus food and ingredients are often discarded. This rampant food waste not only has a significant environmental impact, but it also overlooks the potential value of these resources that could otherwise be tapped into.", 
                  "I envision a unique and exciting solution where restaurants and fast-food chains create partnerships with local composting enterprises. In this system, these businesses would collect their food waste and sell it to composting companies who would then convert this waste into nutrient-rich soil. This soil can be sold back to local agricultural producers or to the general public for home gardening use. Not only does this minimize the amount of food waste going into landfills, it creates a new revenue stream for both the restaurants and the composting companies. Moreover, this rotation completes a full-circle economy where resources are put to best use. It promotes healthy eating, community growth and a sense of unity as we all strive for a greener and healthier earth. This action might seem small, but the collective impact can be massive! Let's turn the tide on food waste and create a tastier and greener future together!"
                  ))