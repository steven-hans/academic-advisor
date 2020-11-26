import spacy
from spacy.language import Language
from spacy.pipeline import TextCategorizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk import word_tokenize
from nltk.corpus import stopwords

stopwords = stopwords.words('indonesian')

factory = StemmerFactory()
stemmer = factory.create_stemmer()

nlp: Language = spacy.load('classifier')

tc: TextCategorizer = nlp.get_pipe('textcat')


def process_prompt(prompts):
    stemmed_prompts = [stemmer.stem(p) for p in prompts]
    tokenized_prompts = [word_tokenize(p) for p in stemmed_prompts]
    stopword_prompts = []

    for p in tokenized_prompts:
        filtered = [n for n in p if n not in stopwords]
        stopword_prompts.append(filtered)

    return stopword_prompts


def predict(text: str) -> str:
    text = " ".join(process_prompt([text])[0])
    doc = [nlp.tokenizer(text)]

    scores, _ = tc.predict(doc)
    #print(scores)

    predicted_labels = scores.argmax(axis=1)
    return [tc.labels[label] for label in predicted_labels][0]

