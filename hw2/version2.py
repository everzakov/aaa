from typing import List
import unittest


class CountVectorizerV2:

    def __init__(self, lowercase=True):
        self._features = dict()
        self.lowercase = lowercase

    def fit_transform(self, _corpus: List[str]) -> List[List[int]]:
        self._features = dict()
        count = 0
        matrix = []
        for i in range(len(_corpus)):
            matrix.append([0 for i in range(len(self._features.keys()))])
            strings = []
            if self.lowercase:
                strings = _corpus[i].lower().split()
            else:
                strings = _corpus[i].split()
            for string in strings:
                if string not in self._features.keys():
                    self._features[string] = count
                    count += 1
                    matrix[i].append(1)
                else:
                    matrix[i][self._features[string]] += 1
        for i in range(len(_corpus)):
            matrix[i] += [0 for i in range(len(self._features.keys()) - len(matrix[i]))]
        return matrix

    def get_feature_names(self) -> List[str]:
        features = ['' for _ in range(len(self._features.keys()))]
        for key, value in self._features.items():
            features[value] = key
        return features


class TestCountVectorizerV2(unittest.TestCase):

    def test_lowercase(self):
        corpus = [
            'Crock Pot Pasta Never boil pasta again',
            'Pasta Pomodoro Fresh ingredients Parmesan to taste'
        ]
        vectorizer = CountVectorizerV2()
        count_matrix = vectorizer.fit_transform(corpus)

        features = ['crock', 'pot', 'pasta', 'never', 'boil', 'again', 'pomodoro', 'fresh', 'ingredients', 'parmesan',
                    'to', 'taste']
        right_count_matrix = [[1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]]
        self.assertEqual(vectorizer.get_feature_names(), features)
        self.assertEqual(count_matrix, right_count_matrix)

    def test_uppercase(self):
        corpus = [
            'Crock Pot Pasta Never boil pasta again',
            'Pasta Pomodoro Fresh ingredients  Parmesan to taste'
        ]
        vectorizer = CountVectorizerV2(lowercase=False)
        count_matrix = vectorizer.fit_transform(corpus)

        features = ['Crock', 'Pot', 'Pasta', 'Never', 'boil', 'pasta', 'again', 'Pomodoro', 'Fresh', 'ingredients',
                    'Parmesan', 'to', 'taste']
        right_count_matrix = [[1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]]

        self.assertEqual(vectorizer.get_feature_names(), features)
        self.assertEqual(count_matrix, right_count_matrix)


corpus = [
    'Crock Pot Pasta Never boil pasta again',
    'Pasta Pomodoro Fresh ingredients Parmesan to taste'
]

vectorizer = CountVectorizerV2()
count_matrix = vectorizer.fit_transform(corpus)

print(vectorizer.get_feature_names())

print(count_matrix)


if __name__ == '__main__':
    unittest.main()
