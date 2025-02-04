# Explorations
 A place to put experiments, explorations of papers, and tutorials for public use via an MIT license. 

## Contents
Below is a list of all the tutorials and their current status. If you have feedback on any of them please open an issue and I'll review it as soon as I can.

| Tutorial  | Status |
| ------------- | ------------- |
| [Pass^K implementation](Tutorials\passK\pass^K.ipynb)  | ✅  |
| [Beyond Accuracy](Tutorials\testing\beyond_accuracy.ipynb)  | 🚧  |

## Calling models for the experiments and tutorials
To minimize the amount of additonal effort, and make the work in this repo more accessible, I'm providing a short bit of guidance on how to quickly set up an environment to call LLMs. There are two ways I will share: 1) calling an API via [Hugging Face Hub](https://huggingface.co/docs/huggingface_hub/en/index) and 2) via local installation of [Ollama](https://ollama.com/). There are in depth tutorials available by navigating to the links so what I include below is a bare minimum to get anyone started.

### Environment Setup
1. Set up a virtual environment using pipenv, conda, or Poetry.
2. Install the `requirements.txt` in this repo
3. Activate your virtual environment
4. Optional - setup a `.env` file to hold your environmental variables (e.g., API Keys)

### Using Ollama
* Install Ollama from the [website](https://ollama.com/) or [github repo](https://github.com/ollama/ollama) to your machine
* Download and run the model you want to use (example below) after you find one at https://ollama.com/library
```command
ollama run llama3.2
```
* If you installed the requirements.txt file from this repo then you already installed the [ollama python package](https://github.com/ollama/ollama-python?tab=readme-ov-file#usage) (recommended)
```python
from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)

```

### Using Hugging Face Hub
Using the Hugging Face Hub allows you to move the compute for inference off your machine (necessary for most larger models or older machines). This does require you to sign up for a free account.
* If you installed the requirements.txt file then you already installed the [Hugging Face Hub](https://github.com/huggingface/huggingface_hub) library to process your inference requests
* Copy your Hugging Face API Key from your profile and add it to the `.env` file.
* You can try the example code below to verify it works.

```python
from huggingface_hub import InferenceClient
import os

client = InferenceClient(
    "cardiffnlp/twitter-roberta-base-sentiment-latest",
    token= os.environ.get("Hugging_Face_API"),
)

client.text_classification("Today is a great day")
```