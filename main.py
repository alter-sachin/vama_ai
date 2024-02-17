import os
from dotenv import load_dotenv
import logging, verboselogs

from deepgram import DeepgramClient, DeepgramClientOptions, PrerecordedOptions

import pandas as pd
import json
from googletrans import Translator


load_dotenv()

# AUDIO_URL = {
#     "url": "https://storage.googleapis.com/vama-prod-assets/agora/snapshots/2de269686847de228b60b99f28e86132_privateConsult-871384-Ach._Vandana_Ji-jagdish_0.mp4"
# }

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
    df = pd.read_csv(csv_file)
    variable = str(variable)
    url = df[variable]#file_url,transcript
    return url
    # for i in range(0,1):
    #     url = (df["file_url"][i])
    #     AUDIO_URL = {"url" : url }
    #     return AUDIO_URL



def transalate_to_english(text):
    translator = Translator()
    out = translator.translate(text)
    print(out)


if __name__ == "__main__":
    AUDIO_URL = {
    "url": "https://s3-ap-southeast-1.amazonaws.com/exotelrecordings/aviga1/bae15c97eb96a712a492bae55fc6181e.mp3"
}
    #call_api(AUDIO_URL)
    # url = read_url_from_csv("recordings.csv")
    # for i in range(28,len(url)):
    # # for i in range(0,len(df)):
    #     url_base = url[i]
    #     AUDIO_URL = {"url":url_base}
    #     response_object = call_api(AUDIO_URL)
    #     number = i
    #     if(response_object):
    #         #write each response to new csv
    #         transcript = response_object.results.channels[0].alternatives[0].transcript
    #         confidence = response_object.results.channels[0].alternatives[0].confidence
    #         words = response_object.results.channels[0].alternatives[0].words
    #         df = pd.DataFrame([[number,url_base,transcript,confidence,words]],columns=['number','url','transcript','confidence','words'])
    #         print(df)
    #         hdr = False  if os.path.isfile('f1.csv') else True
    #         df.to_csv('f1.csv', mode='a', header=hdr)
    #         #df.to_csv('file_name.csv',mode='a+')
    #         print(transcript)
    #     else:
    #         transcript = "None"
    #         confidence = "None"
    #         words = "None"
    #         hdr = False  if os.path.isfile('f1.csv') else True
    #         df = pd.DataFrame([[number,url_base,transcript,confidence,words]],columns=['number','url','transcript','confidence','words'])
    #         print(df)
    #         df.to_csv('f1.csv',mode='a+')



    # parsed = json.loads(call_api(read_url_from_csv("recordings.csv")))
    # df1=pd.DataFrame(parsed[""])
    # df1.to_csv('csvfile.csv', encoding='utf-8', index=False)