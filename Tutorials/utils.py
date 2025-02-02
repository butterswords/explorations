# A file with the functions necessary to run the tutorials. This code contains the answers to several parts of the tutorials that are referenced in later tutorials.
import pandas as pd
import re
import random
from huggingface_hub import InferenceClient
import os


# set up your huggingface client
client = InferenceClient(token=os.environ.get('hf_api')) #replace with your enviornmental variable for the Hugging Face API key

# I'm certain there's a better, more production grade way to implement this but for now I am going to directly input it into the file.

def sourceWords():
    urls = {
        "country":"https://github.com/butterswords/xai-bias-word-lists/blob/main/Countries/combined-countries.csv",
    "profession":"https://github.com/butterswords/xai-bias-word-lists/blob/main/Professions/soc_2018_direct_match_title_file.csv",
    "mFirst":"https://github.com/butterswords/xai-bias-word-lists/blob/main/Names/1990-census-male-first.csv",
    "fFirst":"https://github.com/butterswords/xai-bias-word-lists/blob/main/Names/1990-census-female-first.csv",
    "genderId":"https://github.com/butterswords/xai-bias-word-lists/blob/main/SOGI/sogi.csv",
    "age":"https://github.com/butterswords/xai-bias-word-lists/blob/main/Age/age.csv"
    }

    wordLists = {}
    if not wordLists:
        for item in urls.items():
            category = item[0]
            rawURL = item[1] + "?raw=true"
            frame = pd.read_csv(rawURL)
            if category == "profession":
                wordLists[category] = frame[frame.columns[2]].values.tolist() #The relevant column in this csv is different than the rest for historical reasons
            else:
                wordLists[category] = frame[frame.columns[0]].values.tolist()
    return wordLists

# basic generator to call LLMs hosted on Hugging Face.
def hf_generator(model, prompt, system=None):
    """The function uses a user prompt and (Optional) system prompt to generate a ressponse from a model hosted on Hugging Face.
    Extracts the content out of the response for direct use."""
    if system:    
        messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": system
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    else:
                messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]

    completion = client.chat.completions.create(
        model=model, 
        messages=messages, 
        max_tokens=500
    )
    return completion.choices[0].message.content



def replaceWords(text,lists):
    """This function takes a string (text) and then uses random sampling to replace each placeholder with a random value in the list from a dictionary containing the lists.
    
    This function assumes that each placeholder will only appear once."""
    updated_text = text
    for item in lists.items():
        updated_text = re.sub(f"<<{item[0]}>>",f"{random.sample(item[1],1)[0]}",updated_text)
    return updated_text

def fillPatterns(patterns,words):
    """A simple function to iterate through a list of patterns and fill them using the replaceWords function and a given set """
    filled = []
    for x in patterns:
        filled.append(replaceWords(x,words))
    return filled