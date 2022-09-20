from typing import List


class CountVectorizer:

    def __init__(self, lowercase=True):
        self._features = dict()
        self.lowercase = lowercase

    def fit_transform(self, _corpus: List[str]) -> List[List[int]]:
        self._features = dict()
        count = 0
        for text in _corpus:
            strings = []
            if self.lowercase:
                strings = text.lower().split()
            else:
                strings = text.split()
            for string in strings:
                if string not in self._features.keys():
                    self._features[string] = count
                    count += 1
        matrix = []
        for i in range(len(_corpus)):
            strings = []
            if self.lowercase:
                strings = _corpus[i].lower().split()
            else:
                strings = _corpus[i].split()
            matrix += [[0 for i in range(len(self._features.keys()))]]
            for string in strings:
                matrix[i][self._features[string]] += 1
        return matrix

    def get_feature_names(self) -> List[str]:
        features = ['' for _ in range(len(self._features.keys()))]
        for key, value in self._features.items():
            features[value] = key
        return features


corpus = [
    'Crock Pot Pasta Never boil pasta again',
    'Pasta Pomodoro Fresh ingredients Parmesan to taste'
]

vectorizer = CountVectorizer()
count_matrix = vectorizer.fit_transform(corpus)

print(vectorizer.get_feature_names())

print(count_matrix)
