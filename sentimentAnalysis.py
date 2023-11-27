from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json

def sentimentFinder(result):
    words = result
    analyzer = SentimentIntensityAnalyzer()
    
    sentiments = {}
    
    with open("sentiments.py", "w") as f:
        f.write("sentiments = ")
    
    for word in words:
        vs = analyzer.polarity_scores(word)
        score = vs['compound']
        sentiments[word] = score
    
    with open("sentiments.py", "a") as f:
        f.write(json.dumps(sentiments))
        


