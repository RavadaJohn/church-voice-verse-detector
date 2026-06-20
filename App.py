
from flask import Flask, request, render_template, jsonify
import re
import json

app = Flask(__name__)

# Load Bible Data from JSON File

with open('bible_data.json', 'r') as file:

    bible_data = json.load(file)

print(bible_data)

# Home Page

@app.route('/')
def home():

    return render_template('index.html')

# Detect Bible Verses

@app.route('/detect', methods=['POST'])
def detect():

    data = request.get_json()

    text = data['text']

    # Speech Corrections

    text = text.replace("John 316", "John 3:16")
    text = text.replace("John 360", "John 3:16")
    text = text.replace("John v16", "John 3:16")

    text = text.replace("Romans 828", "Romans 8:28")
    text = text.replace("Romans 826", "Romans 8:26")

    text = text.replace("Psalm 231", "Psalm 23:1")

    text = text.replace("Genesis 11", "Genesis 1:1")

    text = text.replace("Matthew 514", "Matthew 5:14")

    text = text.replace("Philippians 413", "Philippians 4:13")

    # Regex Pattern

    pattern = r'[1-3]?\s?[A-Za-z]+\s\d+:\d+'

    # Detect Verses

    detected_verses = re.findall(pattern, text)

    # Remove Duplicates

    detected_verses = list(set(detected_verses))

    results = []

    # Fetch Verse Text

    for verse in detected_verses:

        verse = verse.strip()

        print("Detected:", verse)

        print("Verse Text:", bible_data.get(verse))

        verse_text = bible_data.get(
            verse,
            "Verse text not available"
        )

        results.append({
            "reference": verse,
            "text": verse_text
        })

    # Send Response

    return jsonify({
        "results": results
    })

# Run Server

app.run(debug=True)