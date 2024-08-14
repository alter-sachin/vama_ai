#####
import os
import threading
import logging, verboselogs


from chains import *


from io import StringIO
from uuid import uuid4 
import ast
import math




def run_on_chat_csv(uploaded_file,thread_number,n_threads):
  
    sensitivity = 0.1
    specific = 0.2
    #silence_threshold = 3  #### seconds of silence allowed
    chat_csv_file = str(uploaded_file)
    ts = str(timestring())
    outfile_chat = "chat_result_"+chat_csv_file+".csv"
    outfile_errors = "chat_error_"+chat_csv_file+".csv"


    #call_api(AUDIO_URL) #"id","astrologer_id","user_id","type","created_at"
    from_id = read_variable_from_csv(chat_csv_file,"from_id",'|')
    id1 = read_variable_from_csv(chat_csv_file,"id",'|')
    to_id = read_variable_from_csv(chat_csv_file,"to_id",sep='|')
    content = read_variable_from_csv(chat_csv_file,"content",sep='|')
    created_at = read_variable_from_csv(chat_csv_file,"updated_at",sep='|')
    updated_at = read_variable_from_csv(chat_csv_file,"updated_at",sep='|')
    
    l = []

    sexual,hate,harrasment,self_harm,sexual_minor,threatening,violence,violence_graphic,self_harm_intent,self_harm_instructions,silence,if_any = (False,)*12

    total_urls = 10
    total_urls = len(from_id)
    print(total_urls)
    step = thread_number

    chunk = math.floor(total_urls/n_threads)
    for i in range((step)*chunk,(step+1)*chunk):
        try:
            i = i +1
            # progress_bar.progress(percentage)
            print("Processing line number %i" % i +" out of total lines %i" %total_urls)
            from_idx = from_id[i]
            from_idx_prev = from_id[i-1]
            id1x=id1[i]
            to_idx = to_id[i]
            contentx = content[i]
            created_atx = created_at[i]
            created_atx_previous = created_at[i-1]
            updated_atx = updated_at[i]
            
            #order_item_idx = order_item_id[i]
            #star_ratingx = star_rating[i]
            print("type is",type(contentx))
            #contentx = "'"+contentx+"'"
            #content_dict = ast.literal_eval(contentx)
            content_dict = json.loads(contentx)
            print("type is",type(content_dict))
            #AUDIO_URL = {"url":url_base}
            #response_object = call_api(AUDIO_URL)
            text = content_dict["text"]
            print("text is",text)
            #print(response_object)
            number = i
            #if(response_object):
            print("line number is ",number)
            sexual,hate,harrasment,self_harm,sexual_minor,threatening,violence,violence_graphic,self_harm_intent,self_harm_instructions,silence,if_any = (False,)*12
            

            
            if(to_idx==from_idx_prev):
                t = difference_in_time(created_at[i],created_at[i-1])
                if(t>10000):  #### greater than 10 seconds for astrolger to respond
                    silence = True
                    if_any = True

            #print(list_transcript)
            #for transcript in list_transcript:
            eng_from_hindi = translate_hindi_to_english(text)
            print(eng_from_hindi)
            response = identify_classes(eng_from_hindi)
            #intermediate area; a topic that is not clearly one thing or the other.
            ####checking for greetings at start of transcript only
            ############### needs to be done differently for chat only data


            greeting_response = identify_greeting(eng_from_hindi)

            print(greeting_response)



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
            df = pd.DataFrame([[from_idx,id1x,to_idx,contentx,created_atx,updated_atx,number,eng_from_hindi,sexual,sexual_score,hate,hate_score,harrasment,harrasment_score,self_harm,self_harm_score,sexual_minor,sexual_minor_score,threatening,threatening_score,violence_graphic,violence_graphic_score,self_harm_intent,self_harm_intent_score,self_harm_instructions,self_harm_instructions_score,violence,violence_score,contact_details,probability,silence,if_any]],
                columns=['from_id','id','to_id','content','created_at','updated_at','number','eng_from_hindi','sexual','sexual_score','hate','hate_score','harrasment','harrasment_score','self_harm','self_harm_score','sexual_minor','sexual_minor_score','threatening','threatening_score','violence_graphic','violence_graphic_score','self_harm_intent','self_harm_intent_score','self_harm_instructions','self_harm_instructions_score','violence','violence_score','contact_details','probability','silence','if_any'])
            print(df)
            
            hdr = False  if os.path.isfile(outfile_chat) else True
            df.to_csv(outfile_chat, mode='a', header=hdr,sep='|')
            #df.to_csv('file_name.csv',mode='a+')
            #print(transcript)
            sexual,hate,harrasment,self_harm,sexual_minor,threatening,violence,violence_graphic,self_harm_intent,self_harm_instructions,silence,if_any = (False,)*12
            # else:
            #     l = 36 *["None"]
            #     transcript = "None"
            #     confidence = "None"
            #     words = "None"
            #     hdr = False  if os.path.isfile(outfile_errors) else True
            #     df = pd.DataFrame([l],
            #         #columns=['from_id','id','to_id','content','created_at','updated_at','number','eng_from_hindi','sexual','sexual_score','hate','hate_score','harrasment','harrasment_score','self_harm','self_harm_score','sexual_minor','sexual_minor_score','threatening','threatening_score','violence_graphic','violence_graphic_score','self_harm_intent','self_harm_intent_score','self_harm_instructions','self_harm_instructions_score','violence','violence_score','contact_details','probability','silence','if_any'])#columns=['astrologer_id','id1','type1','user_id','created_at','order_item_id','star_rating','number','url_base','transcript','confidence','eng_from_hindi','sexual','sexual_score','hate','hate_score','harrasment','harrasment_score','self_harm','self_harm_score','sexual_minor','sexual_minor_score','threatening','threatening_score','violence_graphic','violence_graphic_score','self_harm_intent','self_harm_intent_score','self_harm_instructions','self_harm_instructions_score','violence','violence_score','contact_details','probability','silence','if_any'])
            #     	columns=['from_id','id','to_id','content','created_at','updated_at','number','eng_from_hindi','sexual','sexual_score','hate','hate_score','harrasment','harrasment_score','self_harm','self_harm_score','sexual_minor','sexual_minor_score','threatening','threatening_score','violence_graphic','violence_graphic_score','self_harm_intent','self_harm_intent_score','self_harm_instructions','self_harm_instructions_score','violence','violence_score','contact_details','probability','silence','if_any'])
            #     print(df)
            #     df.to_csv(outfile_errors,mode='a+')
        except Exception as e:
            print(e)
            l = 36*["None"]
            df = pd.DataFrame([[from_idx,id1x,to_idx,contentx,created_atx,updated_atx,number,eng_from_hindi,sexual,sexual_score,hate,hate_score,harrasment,harrasment_score,self_harm,self_harm_score,sexual_minor,sexual_minor_score,threatening,threatening_score,violence_graphic,violence_graphic_score,self_harm_intent,self_harm_intent_score,self_harm_instructions,self_harm_instructions_score,violence,violence_score,contact_details,probability,silence,if_any]],
                columns=['from_id','id','to_id','content','created_at','updated_at','number','eng_from_hindi','sexual','sexual_score','hate','hate_score','harrasment','harrasment_score','self_harm','self_harm_score','sexual_minor','sexual_minor_score','threatening','threatening_score','violence_graphic','violence_graphic_score','self_harm_intent','self_harm_intent_score','self_harm_instructions','self_harm_instructions_score','violence','violence_score','contact_details','probability','silence','if_any'])
            df.to_csv(outfile_errors,mode='a+',sep='|')

            continue
    #with open(outfile_chat, "rb") as template_file:
    #    template_byte = template_file.read()
    #     frame_text.text("Download Now")
    #     progress_bar.progress(100)
    # st.download_button(label="Download Final Result",
    #                     data=template_byte,
    #                     file_name="chat_result.csv",
    #                     mime='text/csv')
    #st.dataframe(df)


    # parsed = json.loads(call_api(read_url_from_csv("recordings.csv")))
    # df1=pd.DataFrame(parsed[""])
    # df1.to_csv('csvfile.csv', encoding='utf-8', index=False)



#run_on_csv()



# # Page title
# st.set_page_config(page_title='🦜🔗 Vama AI Chat Data CSV')
# st.title('🦜🔗 Classify Chat Data')

# # File upload
# uploaded_file = st.file_uploader('Upload the Chat Text Data csv', type='csv')
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
#     run_on_chat_csv(temp_filepath)


#if uploaded_file2 is not None:
#    second_thread()

def chat_thread(csv_name=str):
    n_threads = 10

    thread_list =[]
    for thr in range(n_threads):
        thread = threading.Thread(target=run_on_chat_csv, args=(csv_name,thr,n_threads),)
        thread_list.append(thread)
        thread_list[thr].start()
        #run_on_csv(temp_filepath,n_threads)



