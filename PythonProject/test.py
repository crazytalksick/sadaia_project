from textblob import TextBlob

txt = """
Bridges are ubiquitous structures, ranging from grand spans to modest crossings over waterways or roadways. Skilled engineers, experts in construction, design and build these vital links. Bridges facilitate movement, enabling pedestrian, vehicular, and even cyclist transit. Their importance for transportation is undeniable, as they are crucial for both people and vehicles. Constructing a bridge is a complex undertaking, demanding meticulous planning and the utilization of robust materials such as steel and concrete. The next time you encounter a bridge, reflect on the remarkable engineering prowess that brought it into being."""


def calculate_cefr_level(text):
    blob = TextBlob(text)

    sentence_count = len(blob.sentences)
    word_count = len(blob.words)
    avg_sentence_length = word_count / sentence_count if sentence_count else 0

    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    pos_tags = blob.tags
    noun_count = sum(1 for _, tag in pos_tags if tag in ['NN', 'NNS', 'NNP', 'NNPS'])
    verb_count = sum(1 for _, tag in pos_tags if tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'])
    adjective_count = sum(1 for _, tag in pos_tags if tag in ['JJ', 'JJR', 'JJS'])
    adverb_count = sum(1 for _, tag in pos_tags if tag in ['RB', 'RBR', 'RBS'])

    pos_complexity = noun_count + verb_count + adjective_count + adverb_count

    score = 0

    if avg_sentence_length < 8:
        score += 1
    elif avg_sentence_length < 12:
        score += 2
    elif avg_sentence_length < 15:
        score += 3
    elif avg_sentence_length < 20:
        score += 4
    elif avg_sentence_length < 25:
        score += 5
    else:
        score += 6

    if polarity < -0.3:
        score += 1
    elif polarity < -0.1:
        score += 2
    elif polarity < 0.1:
        score += 3
    elif polarity < 0.3:
        score += 4
    elif polarity < 0.5:
        score += 5
    else:
        score += 6

    if subjectivity < 0.2:
        score += 1
    elif subjectivity < 0.4:
        score += 2
    elif subjectivity < 0.6:
        score += 3
    elif subjectivity < 0.8:
        score += 4
    elif subjectivity < 0.9:
        score += 5
    else:
        score += 6

    if pos_complexity < 10:
        score += 1
    elif pos_complexity < 20:
        score += 2
    elif pos_complexity < 30:
        score += 3
    elif pos_complexity < 40:
        score += 4
    elif pos_complexity < 50:
        score += 5
    else:
        score += 6

    if score <= 4:
        cefr_level = "A1"
    elif score <= 8:
        cefr_level = "A2"
    elif score <= 12:
        cefr_level = "B1"
    elif score <= 16:
        cefr_level = "B2"
    elif score <= 20:
        cefr_level = "C1"
    else:
        cefr_level = "C2"

    return {
        'level': cefr_level,
        'score': score,
        'sentence_length': avg_sentence_length,
        'polarity': polarity,
        'subjectivity': subjectivity,
        'pos_complexity': pos_complexity,
    }
print(calculate_cefr_level(txt)["level"])