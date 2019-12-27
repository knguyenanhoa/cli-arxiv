from .learners import tfidf

def predict(feed_items, STATE=None):
    if STATE == None: raise Exception('you must provide STATE')

    learner = tfidf.Tfidf('./data/summary/')

    test_data = [(feed, feed.summary()) for feed in feed_items]
    best_matches = learner.predict(test_data, metric="cos_similarity")

    return best_matches, STATE
