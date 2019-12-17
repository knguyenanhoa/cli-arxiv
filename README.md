# cli-arxiv
CLI tool for exploring arXiv (inspired by karpathy's brilliant ArXiv Sanity Preserver)

Please create data/pdf/, data/txt/ and data/summary/ directories to hold files downloaded from arXiv. The code doesn't do this for you at the moment. I am also aware that this is a rather stupid way to implement a datastore but I couldn't be bothered with DBs so there.

Uses tfidf with cosine similarity to recommend articles to you. Frequency sum ranking from the tfidf matrix is also implemented and can be switched to by editing the main_ml.py file. Please do add other algorithms as you see fit.

If you'd like to use this code for any reason, please clone or fork it because I will be pushing to this repo from time to time. Cheers!
