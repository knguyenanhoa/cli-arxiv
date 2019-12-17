class BaseLearner():
    def __init__(self, repo_path, learner):
        self.repo_path = repo_path
        self.instance = learner
        self.model = None

    def fit(self):
        raise Exception('abstract class')

    def fit_from_db(self):
        raise Exception('abstract class')

    def predict(self):
        raise Exception('abstract class')
