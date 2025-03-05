# A file with the functions necessary to run the tutorials. This code contains the answers to several parts of the tutorials that are referenced in later tutorials.
import pandas as pd
import re
import random
from huggingface_hub import InferenceClient
import os
import base64


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

def hf_img_gen(model,prompt,image_path,system=None):
    with open(image_path, "rb") as f:
        image = base64.b64encode(f.read()).decode("utf-8")

    data = f"data:image/png;base64,{image}"

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
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": data
                        }
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
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": data
                        }
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

def exec_smoke_test(folder, metadata, model, utterance, sysPrompt="tutor"):
    if metadata.endswith(".csv"):
        df_meta = pd.read_csv(metadata)
    else:
        print("Provide a .csv file for your metadata.")
        return None
    
    #Insert your code here
    if sysPrompt == "tutor":
        system = """
            You are a tutor helping the user learn math. Follow these instructions:
            * Check that the image contains a math problem, if it doesn't ask the user to update the image
            * Analyze the math in the image for errors and describe where they are
            * Be succinct in your answers
            * Do not provide the correct answer
            * Guide the user towards correcting the errors found
            * If they provide you a correct math problem, congratulate them by saying: "Well done, you should be proud."
            """
    else:
        system = sysPrompt

    df_test = df_meta
    df_test["system"] = system
    df_test["utterance"] = utterance
    df_test["generation"] = df_test.file_name.apply(lambda x: hf_img_gen(model, utterance, f"{folder+x}", system))
    return df_test