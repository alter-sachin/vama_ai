import os

import logging, verboselogs


from chains import *



if __name__ == "__main__":
    AUDIO_URL = {
    "url": "https://s3-ap-southeast-1.amazonaws.com/exotelrecordings/aviga1/bae15c97eb96a712a492bae55fc6181e.mp3"

}
    sensitivity = 0.1
    specific = 0.2
    audio_csv_file = "r1.csv"
    outfile_audio = "f3_mar3_2.csv"
    outfile_errors = "f4_mar3_2.csv"
    #t = read_variable_from_csv("recordings_hinglish_transcript.csv","transcript")
    #print(t[0])
    #t1 = "hello हां पूजा जी राधे राधे राधे राधे अरे मैं बोल रही थी आपसे hello तो आप offline थे आज हां आज पहला दिन था ना नवरात्रि का तो part भी था पूरा दिन ok मैं यह पुछ रही थी आपने वह बताया था ना कुछ करने के लिए नवरात्रों में हां हां तो क्या करना था मुझे बताओ आज का दिन तो निकल गया यही कहां निकला है अरे एक दिन तो निकल गया नहीं भाई अभी नवरात्रि का पहला ही दिन तो है आज रात में ही तो करना हां आप ऐसा करो इस number पर आप whatsapp करो तिहत्तर अठानवे सतासी अट्ठासी हज़ार एक second रुको एक second रुको बताओ number तिहत्तर अठानवे अठानवे अठानवे nine eight है हां nine eight हां तैंतीस eight seven eight seven double eight nine six ok इसमें whatsapp करूं हां हां यह मेरा personal number ठीक है ok मैं अभी उसको save करके आपको message करती हूं ठीक है message कर दो मैं लिख देता हूं ठीक है यहां से call cut कर दूं हां हां कर दो"
    #t1 = "नमस्ते, आप कैसे हैं? क्या तुम आज उस बच्चे की गांड चोद रहे हो?"
    #t1 = "मैं गांड देख रहा हूँ लड़की की, क्या मस्त माल है, इसको चोदू क्या"
    #t1 = "किसी लड़की को बिना उसकी मर्जी के गंदी नीयत से छूना, गंदे मैसेज भेजना, जबरदस्ती किस करना, गंदी बातें करना, लड़की को देखकर भद्दी टिप्पणी करना"
    #t1 = "mat gaand sexy dekh pa raha hun ladki ki, kya mast maal hai"
    #t2 = translate_hindi_to_english(t1)
    #print(t2)

    #response = identify_classes(t2)
    
    #astrologer_id,id,type,user_id,created_at,Date,file_url,order_item_id,Star Rating

    #call_api(AUDIO_URL) #"id","astrologer_id","user_id","type","created_at"
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
    for i in range(1,len(url)):
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
            sexual,hate,harrasment,self_harm,sexual_minor,threatening,violence,violence_graphic,self_harm_intent,self_harm_instructions = (False,)*10
            #write each response to new csv
            transcript = response_object.results.channels[0].alternatives[0].transcript
            confidence = response_object.results.channels[0].alternatives[0].confidence
            print(transcript,confidence)
            #words = response_object.results.channels[0].alternatives[0].words
            list_transcript = list(chunkstring(transcript, 2000))
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
                elif(sexual_score>specific): 
                    sexual= True
                hate_score = (response["results"][0]["category_scores"]["hate"])
                if(hate_score>sensitivity and hate_score<specific):
                    hate = "intermediate" 
                elif(hate_score>specific): 
                    hate= True
                harrasment_score = (response["results"][0]["category_scores"]["harassment"])
                if(harrasment_score>sensitivity and harrasment_score<specific):
                    harrasment = "intermediate" 
                elif(harrasment_score>specific): 
                    harrasment= True       
                self_harm_score = (response["results"][0]["category_scores"]["self-harm"])
                if(self_harm_score>sensitivity and self_harm_score<specific):
                    self_harm = "intermediate"
                elif(harrasment_score>specific): 
                    self_harm= True
                sexual_minor_score = (response["results"][0]["category_scores"]["sexual/minors"])
                if(sexual_minor_score>sensitivity and self_harm_score<specific):
                    sexual_minor= "intermediate"
                elif(sexual_minor_score>specific): 
                    sexual_minor= True
                threatening_score = (response["results"][0]["category_scores"]["hate/threatening"])
                if(threatening_score>sensitivity and threatening_score<specific):
                    threatening = "intermediate"
                elif(threatening_score>specific): 
                    threatening= True
                violence_graphic_score = (response["results"][0]["category_scores"]["violence/graphic"])
                if(violence_graphic_score>sensitivity and violence_graphic_score<specific):
                    violence_graphic = "intermediate" 
                elif(violence_graphic_score>specific): 
                    violence_graphic= True
                self_harm_intent_score = (response["results"][0]["category_scores"]["self-harm/intent"])
                if(self_harm_intent_score>sensitivity and self_harm_intent_score<specific):
                    self_harm_intent= "intermediate" 
                elif(self_harm_intent_score>specific): 
                    self_harm_intent= True

                self_harm_instructions_score = (response["results"][0]["category_scores"]["self-harm/instructions"])
                if(self_harm_instructions_score>sensitivity and self_harm_instructions_score>specific):
                    self_harm_instructions = "intermediate" 
                elif(self_harm_instructions_score>specific): 
                    self_harm_instructions= True
                violence_score = (response["results"][0]["category_scores"]["violence"])
                if(violence_score>sensitivity and violence_score<specific):
                    violence = "intermediate"
                elif(violence_score>specific): 
                    violence= True
                contact_response = identify_contact(eng_from_hindi)
                contact_details = (contact_response["contact_details"])
                probability = (contact_response["probability"])
                if(probability>0.4 and probability<0.6):
                    contact_details = "intermediate"
                df = pd.DataFrame([[astrologer_idx,id1x,type1x,user_idx,created_atx,order_item_idx,star_ratingx,number,url_base,transcript,confidence,eng_from_hindi,sexual,sexual_score,hate,hate_score,harrasment,harrasment_score,self_harm,self_harm_score,sexual_minor,sexual_minor_score,threatening,threatening_score,violence_graphic,violence_graphic_score,self_harm_intent,self_harm_intent_score,self_harm_instructions,self_harm_instructions_score,violence,violence_score,contact_details,probability]],
                    columns=['astrologer_id','id1','type1','user_id','created_at','order_item_id','star_rating','number','url_base','transcript','confidence','eng_from_hindi','sexual','sexual_score','hate','hate_score','harrasment','harrasment_score','self_harm','self_harm_score','sexual_minor','sexual_minor_score','threatening','threatening_score','violence_graphic','violence_graphic_score','self_harm_intent','self_harm_intent_score','self_harm_instructions','self_harm_instructions_score','violence','violence_score','contact_details','probability'])
                print(df)
                hdr = False  if os.path.isfile(outfile_audio) else True
                df.to_csv(outfile_audio, mode='a', header=hdr)
                #df.to_csv('file_name.csv',mode='a+')
                print(transcript)
                sexual,hate,harrasment,self_harm,sexual_minor,threatening,violence,violence_graphic,self_harm_intent,self_harm_instructions = (False,)*10
        else:
            l = 34 *["None"]
            transcript = "None"
            confidence = "None"
            words = "None"
            hdr = False  if os.path.isfile(outfile_errors) else True
            df = pd.DataFrame([l],
                columns=['astrologer_id','id1','type1','user_id','created_at','order_item_id','star_rating','number','url_base','transcript','confidence','eng_from_hindi','sexual','sexual_score','hate','hate_score','harrasment','harrasment_score','self_harm','self_harm_score','sexual_minor','sexual_minor_score','threatening','threatening_score','violence_graphic','violence_graphic_score','self_harm_intent','self_harm_intent_score','self_harm_instructions','self_harm_instructions_score','violence','violence_score','contact_details','probability'])
            print(df)
            df.to_csv(outfile_errors,mode='a+')



    # parsed = json.loads(call_api(read_url_from_csv("recordings.csv")))
    # df1=pd.DataFrame(parsed[""])
    # df1.to_csv('csvfile.csv', encoding='utf-8', index=False)