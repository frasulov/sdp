from rest_framework import serializers

from recognizer.test import main
from .tokenizer import word_tokenizer
class NerInputSeriaziler(serializers.Serializer):
    text = serializers.CharField(required=True)


    def create(self, validated_data):
        all_tags = {
            "B-LOC": {
                "next": "I-LOC",
                "name": "location",
            },
            "B-PER": {
                "next": "I-PER",
                "name": "person",
            },
            "B-DATE": {
                "next": "I-DATE",
                "name": "date",
            },
            "B-ORG": {
                "next": "I-ORG",
                "name": "organization"
            },
        }
        tokened_sentence = word_tokenizer(validated_data["text"])
        tokened_sentence = " ".join(tokened_sentence)
        (sentence, tags) = main(tokened_sentence)
        result = ""
        i = 0
        while i < len(sentence):
            if tags[i] in all_tags:
                copy_tag = tags[i]
                text = sentence[i]
                k = i
                for j in range(i+1, len(sentence)):
                    if tags[j] == all_tags[tags[i]]["next"]:
                        if sentence[j] in "-" or sentence[j-1] in "-":
                            text += sentence[j]
                        else:
                            text += " " + sentence[j]
                        k = j
                    else:
                        break
                i = k
                meta_text = self.__generate_tag(all_tags[copy_tag]["name"], text)
                result += meta_text
            else:
                if sentence[i] not in ".()-":
                    result += " "
                result += sentence[i]
            i = i+1
        return {
            "text": result
        }

    def __generate_tag(self, tag,  text):
        return f'<mark data-tag=\'{tag}\' data-text=\'{text}\'></mark>'
