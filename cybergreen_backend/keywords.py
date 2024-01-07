import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation as string_punctuation
from heapq import nlargest

from rake_nltk import Rake
import nltk
nltk.download('punkt')

def get_top_keywords(text):

    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    tokens = [token.text for token in doc]
    print(tokens)
    custom_punctuation = string_punctuation + '\n'
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in custom_punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    print(word_frequencies)

    max_frequency = max(word_frequencies.values())
    max_frequency
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency
    print(word_frequencies)
    sentence_tokens = [sent for sent in doc.sents]
    print(sentence_tokens)

    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    print(sentence_scores)

    select_length = 1
    print(select_length)
    summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)
    print(summary)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    print(summary)

    # Print sentence scores
    print("Sentence Scores:", sentence_scores)

    # Print selected sentences for the summary
    print("Selected Sentences:", summary)

    # Define additional stopwords
    new_stop_words = ['approximately', 'circular', 'economy', 'problem', 'solution', 'model', 'business', 'would', 'could', 'also', 'environmental', 'sustainability']

    # Extend stopwords
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.extend(new_stop_words)

    # Initialize Rake with explicit stopwords
    r = Rake(stopwords=stopwords)

    # Extraction given the text
    r.extract_keywords_from_text(summary)

    # Get the top-ranked phrases with scores
    top_keywords = r.get_ranked_phrases_with_scores()[:2]

    # Print the top-ranked phrases with scores
    for score, keyword in top_keywords:
        print(f"Score: {score}, Keyword: {keyword}")

    # Extract just the keywords
    keywords_only = [keyword for score, keyword in top_keywords]

    # Print the array with just the keywords
    print("Keywords Only:", keywords_only)

    return keywords_only