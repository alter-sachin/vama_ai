Vama app AI

This repository contains working code for analysis of Vama apps audio calls,in order to understand behavior of customers:
1. sexual, harmful content
2. Private information released so that astrologer and customer can go off platform


Data collection:

Majority content is audio , plus chat based. 

Audio content is Hindi, english majorly which will be the focus of this project. Forward compatilbilty for other indic languages.

Modularity:
Build each piece modular pieces, so that even if Speech to text API changes, data in text format can be used by next parts of the pipeline


1. Speech to text  : input audio files in different formats. wav,mp3, mp4 check what is the default audio format.
Output: text data. how output data saved. Database choice ? VectorDB vs relational DB.
is similarity search needed ? yes. 

2. Text : NLP analysis
Bag of words. 
semantic search.
Regex

3. Translation : Hindi to English ?
Use API or OpenAI translation, can querying and translation be combined to reduce token costs.


4. LLM querying
Given a text output which of the following class does it belong to ? 


5. API endpoint to serve batch based.
