from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import re
from chat_fe import get_openai_response

from keywords import get_top_keywords
import math

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

    print(keywords)

    if len(keywords) > 1:
        prompt = "what are 10 commonly discussed solutions to combat the environmental problem of " + keywords[0] + " and " + keywords[1]
    else:
        prompt = "what are 10 commonly discussed solutions to combat the environmental problem of " + keywords[0]

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

    # Apply logarithmic transformation
    inv_log = math.log(inv + 1)  # Adding 1 to avoid log(0)
    
    # Scale to the target range (1 to 10)
    scaled_inv = (inv_log - math.log(1 + 1)) / (math.log(10 + 1) - math.log(1 + 1)) * 9 + 1

    # Apply additional scaling
    scaled_inv_more = scaled_inv * 1.75  # Adjust the scaling factor as needed

    # Ensure the final score doesn't exceed 10
    final_score = min(scaled_inv_more, 10)

    index = similarity_scores.index(max_similarity)

    print("The solution with the highest similarity is:", matches[index])

    print("score:", final_score)

    return final_score


print(get_novelty_score("The world's electronics industry continually churns out new devices, which generates a significant amount of electronic waste (e-waste). Many valuable components in these electronics end up in landfills, and their recovery and reuse are minimal due to a lack of efficient recycling solutions, causing severe environmental and economic loss.  ", 
                  "I propose a service named ""Eco-ElectroCycle"", a system where businesses provide their end-of-life electronics for recycling and recovery of valuable materials. In this system, electronic devices such as computers, mobile phones, and other digital appliances are collected, segregated, and then sent to specialized recycling units.  These recycling units precisely extract valuable and rare materials such as gold, silver, copper, palladium, and a range of rare earth elements, which are then refined and made available for electronics manufacturers to reuse. Simultaneously, any hazardous materials are also securely disposed of, preventing any environmental damage.  Eco-ElectroCycle would help in creating a circular economy in the electronics sector, tightly closing the loop between production, use, and disposal. The novelty of the solution lies in its extensive, integrated approach to e-waste management, not just recycling, but also recovery and reuse of valuable materials. The environmental impact is massive, as it dramatically reduces the need for mining new resources, thus reducing carbon emissions and environmental degradation.  The financial benefits are twofold; businesses could monetize their e-waste, and electronics manufacturers could get a secure supply of essential materials at lower costs than newly mined resources. The feasibility lies in the proven technologies for e-waste recycling and material recovery, and the scalability can be achieved through setting up these recycling units in major cities initially and then expanding the services elsewhere."
                  ))