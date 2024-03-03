import json
from typing import List, Optional
from dotenv import load_dotenv
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel

from deepgram import DeepgramClient, DeepgramClientOptions, PrerecordedOptions

import pandas as pd
import json

import requests



load_dotenv()

# AUDIO_URL = {
#     "url": "https://storage.googleapis.com/vama-prod-assets/agora/snapshots/2de269686847de228b60b99f28e86132_privateConsult-871384-Ach._Vandana_Ji-jagdish_0.mp4"
# }

from openai import OpenAI

client = OpenAI()
import os

# from dotenv import load_dotenv, find_dotenv
# _ = load_dotenv(find_dotenv()) # read local .env file

# openai.api_key  = os.getenv('OPENAI_API_KEY')



template = """A conversation of official nature between professional will be passed to you. Extract from it all scores that suggest if the classes mentioned
with probability as score of its presence in the conversation 
Do not extract the name of the classes itself. If no classes are mentioned that's fine - you don't need to extract any! Just return an empty list.
Do not make up or guess ANY extra information. Only extract what exactly is in the text."""

prompt = ChatPromptTemplate.from_messages([("system", template), ("human", "{input}")])


# Function output schema
class Paper(BaseModel):
    """Information about classes mentioned."""

    title: str
    author: Optional[str]


class Info(BaseModel):
    """Information to extract"""

    classes: List[Paper]


# Function definition
model = ChatOpenAI()
function = [convert_pydantic_to_openai_function(Info)]
chain = (
    prompt
    | model.bind(functions=function, function_call={"name": "Info"})
    | (
        lambda x: json.loads(x.additional_kwargs["function_call"]["arguments"])[
            "classes"
        ]
    )
)

# chain = prompt | model.bind(
#     functions=function, function_call={"name": "Info"}
# ) | JsonKeyOutputFunctionsParser(key_name="papers")


def get_completion(prompt, model="gpt-3.5-turbo", temperature=0): 
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=temperature)
    return response.choices[0].message.content

def get_completion1(prompt, model="gpt-3.5-turbo", temperature=0): 
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model,response_format={ "type": "json_object" },
    messages=messages,
    temperature=temperature)
    return response.choices[0].message.content



def call_api(AUDIO_URL):
    try:
        # STEP 1:
        # Create a Deepgram client using the API key from environment variables
        # (ie export DEEPGRAM_API_KEY="YOUR_API_KEY")
        deepgram = DeepgramClient()

        # STEP 2: Call the transcribe_url method on the prerecorded class
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            language= "hi"
        )
        url_response = deepgram.listen.prerecorded.v("1").transcribe_url(AUDIO_URL, options)
        #print(type(url_response))
        #print(url_response)
        return url_response
        # print(url_response.results.channels[0].alternatives[0].transcript)
        # print(url_response.results.channels[0].alternatives[0].confidence)
        # print(url_response.results.channels[0].alternatives[0].words)

    except Exception as e:
        print(f"Exception: {e}")
        return False

def read_variable_from_csv(csv_file,variable):
    pd.options.display.max_rows = 9
    df = pd.read_csv(csv_file,on_bad_lines=lambda x: x[:-1], engine='python')
    variable = str(variable)
    var_df = df[variable]#file_url,transcript
    return var_df
    # for i in range(0,1):
    #     url = (df["file_url"][i])
    #     AUDIO_URL = {"url" : url }
    #     return AUDIO_URL



def translate_hindi_to_english(text):
    prompt = f"""
Translate the following Hindi or Hinglish text to English: \ 
```{text}```
"""
    response = get_completion(prompt)
    #print(response)
    return response

def translate_hinglish_to_english(text):
    prompt = f"""
Translate the following Hinglish text to English: \ 
```{text}```
"""
    response = get_completion(prompt)
    #print(response)
    return response




def identify_classes(text):

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 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',
    }

    json_data = {
        'input': str(text),
    }

    response = requests.post('https://api.openai.com/v1/moderations', headers=headers, json=json_data)
    #print(response.content)
    return response.json()
    # Note: json_data will not be serialized by requests
    # exactly as it was in the original request.
    #data = '{\n    "input": "मुझे अपने आप को मारने का मन कर रहा है मैं क्या करूँ सर बताओ"\n  }'.encode()
    #response = requests.post('https://api.openai.com/v1/moderations', headers=headers, data=data)

def identify_contact(text):
    prompt = f"""
The text is delimited with triple backticks. \
The text is a conversation between two professionals \
Identify the following from the text : \
    - In the text is anyone sharing phone number like whatsapp number or contact number, answer true or false. \
      Focus on phone number sharing Only. \
      Information like name, date of birth, place and time of birth are fine to be shared. \ 
    - Probability between 0 and 1 of thee answer to above question. \
Format your response as JSON Object with \
"contact_details" and "probability" as the keys.

Review text: '''{text}'''
"""
    response = get_completion1(prompt)
    print(response)
    r1 = json.loads(response)
    return r1


def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))