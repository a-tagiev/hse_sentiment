import pickle
import re
from string import punctuation

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.linear_model import LogisticRegression

from misc.config import Paths


class Model:
    def __init__(self):
        with Paths.model.open("rb") as model_file:
            self.model: LogisticRegression = pickle.loads(model_file.read())

        with Paths.tfidf_vectorizer.open("rb") as vectorizer_file:
            self.tfidf_vectorizer = pickle.loads(vectorizer_file.read())

        self.useless = stopwords.words("russian") + list(punctuation) + [
            '<RT />', 'co', 't', 't co', 'RT', 'â', 'ã', '<Â />', '<Ã />', '<â â />', '<â />', '<t />',
            's', '<s />', 'n', '<n />', '<t/>', 's', '<s/>'
        ]
        self.regex_1 = re.compile(r"[^\w\s]")
        self.regex_2 = re.compile(r"(^|\W)\d+")
        self.lemmatizer = WordNetLemmatizer()

    def preprocess_text(self, text: str):
        text = text.lower()
        text = " ".join(
            filter(
                lambda word: not (word.startswith("@") or word.startswith("http") or word.startswith("rt")),
                text.split()
            )
        )

        tokens = word_tokenize(text.lower())

        lemmatized_tokens = tuple(map(
            self.lemmatizer.lemmatize,
            filter(lambda word: word not in self.useless, tokens)
        ))

        lemmatized_text = " ".join(lemmatized_tokens)
        lemmatized_text = self.regex_1.sub(" ", lemmatized_text)
        lemmatized_text = self.regex_2.sub(" ", lemmatized_text)

        text_vector = self.tfidf_vectorizer.transform([lemmatized_text])

        return text_vector

    def predict(self, text: str) -> int:
        return self.model.predict(self.preprocess_text(text))[0]


model = Model()
