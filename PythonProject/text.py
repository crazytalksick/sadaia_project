import google.generativeai as genai
import streamlit as st
from textblob import TextBlob
import requests

API_URL = "https://api-inference.huggingface.co/models/vennify/t5-base-grammar-correction"
HEADERS = {"Authorization": "Bearer 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"}

genai.configure(api_key="AIzaSyDNHUYg0Y3NcESwCzJnaZsmvThlBXUiEo4")
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("Enter your text")
text = st.text_area(label="", placeholder="Type something here...")

def grammar_corrector(text):
    payload = {"inputs": "grammar: " + text}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return "Error: Unable to process request."

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
    if text:
        articles = {"A1": "", "A2": "", "B1": "", "B2": "", "C1": "", "C2": ""}
        cfr_of_article = cefr_check(text)["level"]
        articles[cfr_of_article] = text
        st.write(f"Your CEFR level is: {cefr_check(text)["level"]}")
        st.write(f"The score of your text: {cefr_check(text)["score"]}")
        st.write(f"Your polarity: {round(cefr_check(text)["polarity"]*100, 2)}%")
        st.write(f"Your subjectivity: {round(cefr_check(text)["subjectivity"]*100, 2)}%")
        if grammar_corrector(text) and len(grammar_corrector(text)) <= 80 and grammar_corrector(text) != "Error: Unable to process request." and text.strip() != grammar_corrector(text).strip() :
            st.write(f"*Grammar Issues Found:* ✅\n*Corrected Text:* {grammar_corrector(text)}")
        else:
            st.write("✅ No grammar errors detected!")
        for i in articles:
            if articles[i] == "": articles[i] = cefr_generator(i, text)
            if i != cfr_of_article:
                st.title(f"The article in {i}")
                st.write(articles[i])
    else:
        st.error("Please enter a topic before submitting.")
