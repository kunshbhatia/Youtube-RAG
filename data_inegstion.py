from youtube_transcript_api import YouTubeTranscriptApi #Access to Youtube
from langchain_core.documents import Document  #Formating
from langchain_text_splitters import RecursiveCharacterTextSplitter #For Chunking
from langchain_huggingface import HuggingFaceEmbeddings #Embedding Model
from langchain_chroma import Chroma #Vector DB 
from googletrans import Translator #To Translate the text to english for LLM
import httpx #Remove Timeout
from utilities import get_video_details
import streamlit as st
import requests

def data_ingestion(video_link,session_id):
    #GETTING VIDEO INFO FROM YOUTUBE
    ytt_api = YouTubeTranscriptApi() #To Bypass IP Block on deployed server
    url = video_link.split("=")
    video_id = url[1]

    possible_languages = ['en','hi','en-IN','en-US','a.en','a.hi','bn','ta','te','ml','kn','mr','gu','pa','ur','fr','de','es','ja','ko','ar','ru']

    lang_success = False
    for lang_code in possible_languages:
        try:
            lang_list = []
            lang_list.append(lang_code)
            data = ytt_api.fetch(video_id,languages=lang_list)
            lang = lang_code
            lang_success = True
            break

        except:
            continue

    if not lang_success:
        raise Exception("No transcript available")

    text_data = '' #Adding all the text in string format in local language
    for sent in data.snippets:
        text = sent.text
        text_data = text_data + f"{text}"

    title,description,channel,views,duration,thumbnail = get_video_details(video_link)

    if lang != 'en': #If Lang is not english , then converting to eng
    
    #CHUNKIGN FOR TRANSLATION OF LANGUAGES OTHER THAN ENGLISH
        final_chunked_data_for_translation = []

        def chunking(chunk_size=min(4000,len(text_data))):  
            chunk_size_min = 0
            chunk_size_max = chunk_size
            
            while chunk_size_max < len(text_data) :
                final_chunked_data_for_translation.append(text_data[chunk_size_min:chunk_size_max])
                chunk_size_min = chunk_size_min + chunk_size
                chunk_size_max = chunk_size_max + chunk_size

        chunking()

    #TRANSLATION INTO ENGLISH
        output = []
        custom_timeout = httpx.Timeout(20.0, read=None) 
        translator = Translator(timeout = custom_timeout)
        for i in final_chunked_data_for_translation:
            result = translator.translate(i, dest='en')
            output.append(result.text)

        text_in_english  = ' ' #Adding all the text in string format in the language english
        for i in output:
            text_in_english  = text_in_english  + f"{i}" 
        text_in_english = text_in_english + f"\n\n\n\n Title = {title} \n Description = {description} \n Channel Name = {channel} \n View Count = {views} \n Duration = {duration} Seconds"

    else:
        text_in_english = text_data +  f"\n\n Title = {title} \n Description = {description} \n Channel Name = {channel} \n View Count = {views} \n Duration = {duration} Seconds"

    #EMBEDDING
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    documents = [Document(page_content=text_in_english)]


    text_splitter = RecursiveCharacterTextSplitter ( 
            separators=["\n\n", "\n", ".", " "],
            chunk_size = 1000,
            chunk_overlap = 250
        )
    #Made By Kunsh Bhatia
    chunks = text_splitter.split_documents(documents)


    for i, chunk in enumerate(chunks): # title,description,channel,views,duration
        chunk.metadata["source"] = video_link
        chunk.metadata["chunk_id"] = i
        chunk.metadata["language"] = lang

    vector_storage = Chroma.from_documents(
            documents=chunks,
            embedding=embedding,
            persist_directory=f"db/{session_id}",
            collection_metadata={"hnsw:space" : "cosine"}
        )
    #Made by Kunsh Bhatia
    return vector_storage,text_data,text_in_english,title,description,channel,views,duration,thumbnail # Gives Vector Storage , Text Data in local language and english language

if __name__ == '__main__':
    data_ingestion(input("Enter Video URL: "))
#Made by Kunsh Bhatia