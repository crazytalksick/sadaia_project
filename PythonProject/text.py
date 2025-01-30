import google.generativeai as genai
import streamlit as st
from textblob import TextBlob

genai.configure(api_key="AIzaSyDNHUYg0Y3NcESwCzJnaZsmvThlBXUiEo4")
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("Enter your interest")
interest = st.text_input("Enter your topic of interest:", placeholder="Type something here...")

def cefr_check(text):
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

def cefr_generator(cefr, text):
    return model.generate_content(f"generate a short paragraph that's the exact same as provided next, but MUST be in {cefr} CEFR level: {text}")._result.candidates[0].content.parts[0].text

if st.button("Submit"):
    if interest:
        if model.generate_content(f"reply with only either Yes or No without any additional spaces or punctuations, is this considered something that expresses an interest ?: {interest}")._result.candidates[0].content.parts[0].text == "Yes\n":
            articles = {"A1": "", "A2": "", "B1": "", "B2": "", "C1": "", "C2": ""}
            article = model.generate_content(f"write a short add simple A1 article about anything related to {interest}")._result.candidates[0].content.parts[0].text
            cfr_of_article = cefr_check(article)["level"]
            articles[cfr_of_article] = article
            for i in articles:
                if articles[i] == "": articles[i] = cefr_generator(i, article)
                st.title(f"The article in {i}")
                st.write(articles[i])
        else:
            st.write("please enter a valid expression of interest.")
    else:
        st.error("Please enter a topic before submitting.")
