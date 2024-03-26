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
from class_list import classes_list


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
with probability as score of its presence in the conversation. The classes are {{classes_list}}
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
            smart_format=False,
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
Identify these queries from the text : \
    - In the text is anyone sharing phone number like whatsapp number or contact number, answer true if yes and false if not. \
       \
    - Probability between 0 and 1 to previous query. \
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


##########################tests##########################################

# string1 = " हां. आप ऐसा करो इस number पर आप WhatsApp करो तिहत्तर अठानवे सतासी अट्ठासी हज़ार.एक second रुको, एक second रुको. बताओ number तिहत्तर. अठानवे अठानवे, अठानवे 9 8 है? हां, 9 8. हां, तैंतीस 8787 double 896.Ok, इसमें WhatsApp करूं? हां हां, यह मेरा personal number. ठीक है ok, मैं अभी उसको save करके आपको message करती हूं."

# string2 = "मेरी date of birth 6 march 1993 hai, aur mai 5 saal ki hu, aur meera janam subah 10 baje hua tha,aap call karo mujhe diya maine 675111"

# eng = translate_hindi_to_english(string2)
# print(eng)
# identify_contact(eng)


####with phrases similar to training words


def identify_greeting(text):
    prompt = f"""
The text is delimited with triple backticks. \
The text is a conversation between two professionals \
Identify these queries from the text : \
    - In the text is anyone greeting the other person at the start properly , return value as true if yes and false if not. \
       \
    - Probability between 0 and 1 to previous query. \
Format your response as JSON Object with \
"contact_details" and "probability" as the keys.
if contact details reponse is N/A replace it with false
Review text: '''{text}'''
"""
    response = get_completion1(prompt)
    print(response)
    r1 = json.loads(response)
    return r1

text5 = "it is with pleasure i greet you, how are you? welcome to our app"

text6 = "you dont matter anymore"


def identify_silence(words,length_audio):
    start = 0
    end = length_audio
    silence_ranges = []
    print(float(words[0].start))
    silence_ranges.append([start,float(words[0].start)])
    for i in range(1,len(words)):
        if(float(words[i-1].end) != float(words[i].start)):
            silence_ranges.append([float(words[i-1].end),float(words[i].start)])
    if(float(words[len(words)-1].end)!= end):
        silence_ranges.append([float(words[len(words)-1].end),end])
    print(silence_ranges)
    return silence_ranges

identify_greeting(text5)
identify_greeting(text6)





##############################


from pydub import AudioSegment
import requests
import wave,wget

def download_audio(url):
    full_sounds = AudioSegment.empty()
    #audio = AudioSegment.from_file("")
    filename = wget.download(url)
    sound = AudioSegment.from_file(filename, format='m4a')
    file_handle = sound.export("1.wav", format='wav')
    #open("file.wav", 'wb').write(resp.content)

    #f = wave.open(audio_file, "r")



def trim_audio(intervals, input_file_path, output_file_path):
    # load the audio file
    audio = AudioSegment.from_file(input_file_path)
    combined_sounds = AudioSegment.empty()
    # iterate over the list of time intervals
    for i, (start_time, end_time) in enumerate(intervals):
        # extract the segment of the audio
        segment = audio[start_time*1000:end_time*1000]

        # construct the output file path
        #output_file_path_i = f"{output_file_path}_{i}.wav"
        combined_sounds += segment
        # export the segment to a file
    combined_sounds.export(output_file_path, format='wav')

# test it out
print("Trimming audio...")
#trim_audio([[0, 1], [1, 2]], "test_input.wav", "test_output")


import numpy as np
from scipy.io.wavfile import read

def calculate_average_db(wav_file):
  """Calculates the average dB level over a WAV file.

  Args:
    wav_file: The path to the WAV file.

  Returns:
    The average dB level.
  """

  # Read the WAV file.
  sample_rate, wav_data = read(wav_file)

  # Convert the WAV data to a float32 array.
  wav_data = np.abs(wav_data.astype(np.float32)) / 32768

  # Split the WAV data into chunks.
  chunks = np.array_split(wav_data, 100)

  # Calculate the average dB level for each chunk.
  db_levels = [20 * np.log10(np.mean(chunk ** 2)) for chunk in chunks]

  # Calculate the average dB level over the entire file.
  average_db_level = np.mean(db_levels)

  return average_db_level

# # Example usage:

