import os

import torch
# from sdp.settings import BASE_DIR
from .config import UNIQUE_TAGS
from .utils import predict_sentence, load_pickle

PAD_IDX = 0
UNK_IDX = 1

tag2idx = {tag: idx for idx, tag in enumerate(UNIQUE_TAGS)}
idx2tag = {idx: tag for tag, idx in tag2idx.items()}

def main(s):
    # os.path.join(BASE_DIR, 'program/data/twograms.txt')
    device = "cpu"

    # model = torch.load(os.path.join(BASE_DIR, 'ner/testing/model.pth'), map_location=lambda storage, loc: storage)
    model = torch.load("/Users/feqanrasulov/Desktop/sdp/recognizer/model.pth", map_location=lambda storage, loc: storage)
    model = model["model"]
    model.eval()
    print(model)
    model.crf.device = device
    model.device = device
    w2i = load_pickle("/Users/feqanrasulov/Desktop/sdp/recognizer/word2index.pkl")
    sentence = (
        s
    )
    sentence_tokens = sentence.split()
    score, tags = predict_sentence(model, sentence_tokens, w2i, idx2tag)

    for token, tag in zip(sentence_tokens, tags):
        print("{:<15}{:<5}".format(token, tag))

    return (sentence_tokens, tags)
