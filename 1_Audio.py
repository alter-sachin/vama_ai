#####
import os
import threading
import logging, verboselogs


from chains import *
#import streamlit as st
#from streamlit.runtime.scriptrunner import add_script_run_ctx
#from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx


from io import StringIO
from uuid import uuid4 

import math




def run_on_csv(uploaded_file,thread_number,n_threads):
    sensitivity = 0.1
    specific = 0.2
    silence_threshold = 10  #### seconds of silence allowed
    audio_csv_file = str(uploaded_file)
    # line_text = st.empty()
    ts = str(timestring())
    outfile_audio = "audio_output_"+ts+"_.csv"
    outfile_errors = "audio_output_"+ts+"_error.csv"
    
    
    id1 = read_variable_from_csv(audio_csv_file,"id")
    astrologer_id = read_variable_from_csv(audio_csv_file,"astrologer_id")
    user_id = read_variable_from_csv(audio_csv_file,"user_id")
    type1 = read_variable_from_csv(audio_csv_file,"type")
    created_at = read_variable_from_csv(audio_csv_file,"created_at")
    url = read_variable_from_csv(audio_csv_file,"file_url")
    order_item_id = read_variable_from_csv(audio_csv_file,"order_item_id")
    star_rating = read_variable_from_csv(audio_csv_file,"Rating")
    #Date = read_variable_from_csv(audio_csv_file,"Date")
    l = []
    # #for i in range(0,len(url)):
    #total_urls = 10
    total_urls = len(url)
    step = thread_number
    
    chunk = math.floor(total_urls/step)
    for i in range((step-1)*chunk,step*chunk):
        try:
            print("Processing line number %i" % i +" out of total lines %i" %total_urls)
            #frame_text.text("Percentage Completed %i" % percentage + "%")
            url_base = url[i]
            id1x=id1[i]
            astrologer_idx = astrologer_id[i]
            user_idx = user_id[i]
            type1x = type1[i]
            created_atx = created_at[i]
            order_item_idx = order_item_id[i]
            star_ratingx = star_rating[i]
            print(url_base)
            AUDIO_URL = {"url":url_base}
            response_object = call_api(AUDIO_URL)

            #print(response_object)
            number = i
            if(response_object):
                print("line number is ",number)
                sexual,hate,harrasment,self_harm,sexual_minor,threatening,violence,violence_graphic,self_harm_intent,self_harm_instructions,silence,background_noise,greeting_response,greeting_prob,if_any = (False,)*15
                #write each response to new csv
                transcript = response_object.results.channels[0].alternatives[0].transcript
                confidence = response_object.results.channels[0].alternatives[0].confidence
                print("here",transcript,confidence)

                ##### silence range and thresold 
                words = response_object.results.channels[0].alternatives[0].words
                length_audio = response_object.metadata.duration
                if(len(words)>0):
                    silence_ranges = identify_silence(words,length_audio)
                # download_audio(url_base)
                # trim_audio(silence_ranges,"1.wav","2.wav")
                # #calculate_average_db("test_output.wav")
                # finaldb = calculate_average_db('2.wav')
                # print("final",finaldb)
                # initialdb = calculate_average_db("1.wav")
                # print("initial",initialdb)
                # divide = initialdb/finaldb
                # if(divide>.80):
                #     background_noise = True
                #     if_any = True
                #if silence_ranges:
                    for silence_range in silence_ranges:
                        if((float(silence_range[1])-float(silence_range[0]))>silence_threshold):
                            silence = True
                            if_any = True
                list_transcript = list(chunkstring(transcript, 2000))
                ####checking for greetings at start of transcript only
                greeting_response = identify_greeting(list_transcript[0])

                print("greeting reponse is:",greeting_response)
                contact_details = (greeting_response["greeting_details"])
                greeting_prob = (greeting_response["probability"])
                if(greeting_prob>0.4 and greeting_prob<0.6):
                    greeting_details = "intermediate"
                    if_any = "intermediate"
                elif(greeting_prob>0.6):
                    greeting_details = True
                    if_any = True

                #print(list_transcript)
                for transcript in list_transcript:
                    eng_from_hindi = translate_hindi_to_english(transcript)
                    print(transcript,eng_from_hindi)
                    response = identify_classes(eng_from_hindi)
                    #intermediate area; a topic that is not clearly one thing or the other.

                    print(response["results"][0]["category_scores"])
                    # for scores in response["results"]:
                    #     print(scores)
                    #     print(type(scores))
                    sexual_score = (response["results"][0]["category_scores"]["sexual"])
                    if(sexual_score>sensitivity and sexual_score<specific):
                        sexual = "intermediate"
                        if_any = "intermediate"
                    elif(sexual_score>specific): 
                        sexual= True
                        if_any = True
                    hate_score = (response["results"][0]["category_scores"]["hate"])
                    if(hate_score>sensitivity and hate_score<specific):
                        hate = "intermediate"
                        if_any = "intermediate" 
                    elif(hate_score>specific): 
                        hate= True
                        if_any = True
                    harrasment_score = (response["results"][0]["category_scores"]["harassment"])
                    if(harrasment_score>sensitivity and harrasment_score<specific):
                        harrasment = "intermediate"
                        if_any = "intermediate" 
                    elif(harrasment_score>specific): 
                        harrasment= True
                        if_any = True    
                    self_harm_score = (response["results"][0]["category_scores"]["self-harm"])
                    if(self_harm_score>sensitivity and self_harm_score<specific):
                        self_harm = "intermediate"
                        if_any = "intermediate"
                    elif(harrasment_score>specific): 
                        self_harm= True
                        if_any = True
                    sexual_minor_score = (response["results"][0]["category_scores"]["sexual/minors"])
                    if(sexual_minor_score>sensitivity and self_harm_score<specific):
                        sexual_minor= "intermediate"
                        if_any = "intermediate"
                    elif(sexual_minor_score>specific): 
                        sexual_minor= True
                        if_any = True
                    threatening_score = (response["results"][0]["category_scores"]["hate/threatening"])
                    if(threatening_score>sensitivity and threatening_score<specific):
                        threatening = "intermediate"
                        if_any = "intermediate"
                    elif(threatening_score>specific): 
                        threatening= True
                        if_any = True
                    violence_graphic_score = (response["results"][0]["category_scores"]["violence/graphic"])
                    if(violence_graphic_score>sensitivity and violence_graphic_score<specific):
                        violence_graphic = "intermediate" 
                        if_any = "intermediate"
                    elif(violence_graphic_score>specific): 
                        violence_graphic= True
                        if_any = True
                    self_harm_intent_score = (response["results"][0]["category_scores"]["self-harm/intent"])
                    if(self_harm_intent_score>sensitivity and self_harm_intent_score<specific):
                        self_harm_intent= "intermediate" 
                        if_any = "intermediate"
                    elif(self_harm_intent_score>specific): 
                        self_harm_intent= True
                        if_any = True
                    self_harm_instructions_score = (response["results"][0]["category_scores"]["self-harm/instructions"])
                    if(self_harm_instructions_score>sensitivity and self_harm_instructions_score>specific):
                        self_harm_instructions = "intermediate"
                        if_any = "intermediate" 
                    elif(self_harm_instructions_score>specific): 
                        self_harm_instructions= True
                        if_any = True
                    violence_score = (response["results"][0]["category_scores"]["violence"])
                    if(violence_score>sensitivity and violence_score<specific):
                        violence = "intermediate"
                        if_any = "intermediate"
                    elif(violence_score>specific): 
                        violence= True
                        if_any = True
                    contact_response = identify_contact(eng_from_hindi)
                    contact_details = (contact_response["contact_details"])
                    probability = (contact_response["probability"])
                    if(probability>0.4 and probability<0.6):
                        contact_details = "intermediate"
                        if_any = "intermediate"
                    df = pd.DataFrame([[astrologer_idx,id1x,type1x,user_idx,created_atx,order_item_idx,star_ratingx,number,url_base,transcript,confidence,eng_from_hindi,sexual,sexual_score,hate,hate_score,harrasment,harrasment_score,self_harm,self_harm_score,sexual_minor,sexual_minor_score,threatening,threatening_score,violence_graphic,violence_graphic_score,self_harm_intent,self_harm_intent_score,self_harm_instructions,self_harm_instructions_score,violence,violence_score,contact_details,probability,silence,background_noise,greeting_response,greeting_prob,if_any]],
                        columns=['astrologer_id','id1','type1','user_id','created_at','order_item_id','star_rating','number','url_base','transcript','confidence','eng_from_hindi','sexual','sexual_score','hate','hate_score','harrasment','harrasment_score','self_harm','self_harm_score','sexual_minor','sexual_minor_score','threatening','threatening_score','violence_graphic','violence_graphic_score','self_harm_intent','self_harm_intent_score','self_harm_instructions','self_harm_instructions_score','violence','violence_score','contact_details','probability','silence','background_noise','greeting_response','greeting_prob','if_any'])
                    print(df)
                    
                    hdr = False  if os.path.isfile(outfile_audio) else True
                    df.to_csv(outfile_audio, mode='a', header=hdr)
                    #df.to_csv('file_name.csv',mode='a+')
                    print(transcript)
                    sexual,hate,harrasment,self_harm,sexual_minor,threatening,violence,violence_graphic,self_harm_intent,self_harm_instructions,silence,background_noise,greeting_response,greeting_prob,if_any = (False,)*15
                    #sexual,hate,harrasment,self_harm,sexual_minor,threatening,violence,violence_graphic,self_harm_intent,self_harm_instructions,silence,if_any = (False,)*12
        except Exception as e:
            print(e)
            l = 39 *["None"]
            transcript = "None"
            confidence = "None"
            words = "None"
            hdr = False  if os.path.isfile(outfile_errors) else True
            df = pd.DataFrame([l],
                columns=['astrologer_id','id1','type1','user_id','created_at','order_item_id','star_rating','number','url_base','transcript','confidence','eng_from_hindi','sexual','sexual_score','hate','hate_score','harrasment','harrasment_score','self_harm','self_harm_score','sexual_minor','sexual_minor_score','threatening','threatening_score','violence_graphic','violence_graphic_score','self_harm_intent','self_harm_intent_score','self_harm_instructions','self_harm_instructions_score','violence','violence_score','contact_details','probability','silence','background_noise','greeting_response','greeting_prob','if_any'])
            print(df)
            df.to_csv(outfile_errors,mode='a+')
            continue
    with open(outfile_audio, "rb") as template_file:
        template_byte = template_file.read()
        #frame_text.text("Download Now")
        #progress_bar.progress(100)
        # st.download_button(label="Download Final Result",
        #                     data=template_byte,
        #                     file_name=outfile_audio,
        #                     mime='text/csv')
    #st.dataframe(df)


    # parsed = json.loads(call_api(read_url_from_csv("recordings.csv")))
    # df1=pd.DataFrame(parsed[""])
    # df1.to_csv('csvfile.csv', encoding='utf-8', index=False)



#run_on_csv()



# # Page title
# st.set_page_config(page_title='🦜🔗 Vama AI Audio CSV')
# st.title('🦜🔗 Classify Audio Calls Data')

# # File upload
# uploaded_file = st.file_uploader('Upload the audio URL csv', type='csv')
# #= st.download_button('Download CSV for audio', text_contents, 'f3_mar3_111.csv', 'text/csv',disabled=True)


# download_instructions = st.empty()
# download_instructions.text("🦜🔗 Download button enables when 100% done. Do not refresh or close tab.\n All processing will be lost.")
# #with open('f3_mar3_111.csv') as f:
# #st.title('🦜🔗 Download button enables when 100% done')
# #download_final = st.download_button('Download Final CSV')  # Defaults to 'text/plain'

# #uploaded_file2 = st.file_uploader('Upload the text csv', type='csv')

# #data = read_csv(temp_filepath)

# if uploaded_file is not None:
#     content = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
#     temp_filepath = f"/tmp/{uuid4()}"
#     with open(temp_filepath, "w") as f:
#         f.write(content)
#     #t1 = threading.Thread(target=run_on_csv, args=(temp_filepath))
#     #t1.start()



n_threads = 20

thread_list =[]
for thr in range(n_threads):
    thread = threading.Thread(target=run_on_csv, args=("1_agora.csv",thr,n_threads),)
    thread_list.append(thread)
    thread_list[thr].start()
    #run_on_csv(temp_filepath,n_threads)



#if uploaded_file2 is not None:
#    second_thread()
