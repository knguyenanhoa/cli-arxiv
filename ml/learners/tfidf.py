"""
ArXiv CLI Browser - a command line interface browser for the popular pre-print
academic paper website https://arxiv.org

Copyright (C) 2020  Klinkesorn Nguyen An Hoa

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

Author contactable at k<dot>nguyen<dot>an<dot>hoa<at>gmail<dot>com
"""

import os, sys, re, copy

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

from . import base_learner

class Tfidf(base_learner.BaseLearner):
    def __init__(self, repo_path, learner_params={}):
        learner = TfidfVectorizer(**learner_params)
        super(Tfidf, self).__init__(repo_path, learner)

    def data_load(self):
        for (dirpath, dirnames, filenames) in os.walk(self.repo_path):
            self.data = [
                open(
                    self.repo_path+fname, 'r'
                ).readlines() for fname in filenames if fname[0] != '.'
            ]
            break
        return self.data

    def data_clean(self, data):
        data = [
            [
                text.replace("\n", "") for text in content_list
            ] for content_list in data
        ]
        return [[text for text in content_list if text != ""] for content_list in data]

    def fit_from_db(self):
        data = self.data_load()
        data = self.data_clean(data)
        data = [' '.join(document) for document in data]

        try:
            X = self.instance.fit_transform(data).toarray()
        except:
            raise Exception('no summaries detected (check summary folder)')

        self.model = X
        return X

    def predict_sum_freq(self, test_data):
        self.fit_from_db()
        feed_scores = []
        for feed, text in test_data:
            test_tokens = self.instance.build_tokenizer()(text)
            test_tokens = [token for token in test_tokens if len(token) > 1]
            sum_freq_score = max([
                sum([
                    doc[
                        self.instance.vocabulary_.get(token)
                    ] for token in test_tokens if self.instance.vocabulary_.get(token) != None
                ]) for doc in self.model
            ])
            feed_scores += [(feed, sum_freq_score)]

        # top 5 for now
        best = sorted(feed_scores, key=lambda x: x[1], reverse=True)[:5]
        return [feed for feed, score in best]


    def fit(self, test_data):
        data = copy.copy(self.data_load())
        data += [text.split(".") for feed, text in test_data]
        data = self.data_clean(data)
        data = [' '.join(document) for document in data]

        try:
            X = self.instance.fit_transform(data).toarray()
        except:
            raise Exception('no summaries detected (check summary folder)')

        self.model = X
        return X

    def predict_cos_similarity(self, test_data):
        self.fit(test_data)
        train = self.model[:len(self.model)-len(test_data)]
        test = self.model[len(self.model)-len(test_data):]
        scores = np.matmul(train, test.transpose())

        model_data = [' '.join(document) for document in self.data]

        test_data_lengths = np.array([len(data) for data in test_data])
        model_data_lengths = np.array([len(data) for data in model_data])
        mat_lengths = np.matmul(
            test_data_lengths.reshape(test_data_lengths.shape[0],1),
            model_data_lengths.reshape(1, model_data_lengths.shape[0])
        )
        scores = scores * 1/mat_lengths.transpose()
        # ordering doesn't matter
        #gets best n results
        n = 5
        indices = np.unique(np.argpartition(scores, -n, axis=1)[:,-n:].flatten())
        best = np.array(test_data)[indices].tolist()
        return [feed for feed, text in best]

    def predict(self, test_data, metric='sum_freq'):
        if metric == 'sum_freq':
            return self.predict_sum_freq(test_data)
        if metric == 'cos_similarity':
            return self.predict_cos_similarity(test_data)
