# Vama app AI

This repository contains working scripts for analysis of Vama apps audio calls and chat messages, in order to understand AUDIT customer Behavior:
1. sexual, harmful content
   
3. Private information released so that astrologer and customer can go off platform


## Data collection:

Majority content is audio , plus chat texts. 

Audio content is Hindi, english majorly which will be the focus of this project. Forward compatilbilty for other indic languages

## Modularity:

Build each piece modular pieces, so that even if Speech to text API changes, data in text format can be used by next parts of the pipeline


# 1. Speech to text  : input audio files in different formats. wav,mp3, mp4 check what is the default audio format.
we use the deepgram API, please check issues for the current username passwords being used.

For the LLM analysis we use chatgpt API, again check issues for which username password is being used. with API keys.


# 2. Text : NLP analysis
LLM based prompts in the chains,py file 

# 3. Translation : Hindi to English ?
Use OpenAI API for translation
prompt engineer here to use words that are MOST SIMILAR to "bad" content.


## 4. LLM querying
Given a text output which of the following class does it belong to ? 
This is a distributed sum based output 


## 5. API endpoint to serve batch based.
S3 BUCKET is provided by vama team, where every midnight DB calls to their main DB creates files.
check issues again for what the username password for accessing the s3 bucket is,and what convention is used.


# CHECK ISSUES FOR DETAILS OF DEPLOYMENT OF EACH PIECE.

