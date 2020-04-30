# cli-arxiv
CLI tool for exploring arXiv (inspired by karpathy's brilliant ArXiv Sanity
Preserver)

The script will create data/pdf/, data/txt/ and data/summary/ directories to hold
files downloaded from arXiv. I am also aware that this is a rather stupid way
to implement a datastore but DBs seem a bit over the top. Text from PDFs are
auto-converted on downloaded and are used to suggest future articles to the
user. Downloading articles is idempotent.

It uses tfidf with cosine similarity to recommend articles to you. Frequency
sum ranking from the tfidf matrix is also implemented and can be switched to by
editing the ml/main\_ml.py file (set metric="sum\_freq"). Please do add other
algorithms as you see fit.

If you'd like to alter this code for any reason, please fork it because
I will be pushing to this repo from time to time. Cheers!

# INSTALL
- Clone the repo (it uses python 3).
- Install dependencies.
```
pip install -r requirements.txt
```
- Start the script.
```
python main.py
```

# ISSUES
- There may be a few seconds of network delay when browsing new articles for the first
  time as the script has to go fetch the article list from arXiv. The same
  holds for first-time article downloads. The script does cache article lists
  for a while before asking arXiv for an updated list.
- I should've used an available arXiv API wrapper.

# DISCLAIMER
- This script hits the arXiv web API to function so please do not alter it to
  spam the arXiv site (though I don't think one can meaningfully impact
  their servers with this). I take no responsibiltiy for its misuse.
