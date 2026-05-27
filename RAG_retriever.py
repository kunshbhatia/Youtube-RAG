import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import streamlit as st

def rag_retriever(query,session_id,queries=[]):
    try:
        groq_api = st.secrets["GROQ_API_KEY"] #Streamlit Use
    except:
        groq_api = "GROQ_API_KEY" #Personal Use
    
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    #Made by Kunsh Bhatia
    database = Chroma(
        embedding_function=embedding,
        persist_directory= f"db/{session_id}",
        collection_metadata={"hnsw:space": "cosine"}
    )

    load_dotenv()
    model = ChatGroq(
        api_key=os.getenv(groq_api),
        temperature=0,
        model_name="llama-3.1-8b-instant"
    )

    #queries.insert(0, query) #Insert new query at first position
    latest_query = query #Latest One
    history = queries[1:5] 

    rewrite_messages = [
        SystemMessage(content="Rewrite the new question in easy language to be standalone and searchable. Just return the rewritten question."),
    ] + history + [
        HumanMessage(content=f"New question: {latest_query} . Context : Its basically a transcript of a Youtube Video. If the question is from a new topic , then DO NOT change the question . Only use chat history provided if the questions needs to be rewritten")
    ]

    rewritten_query = model.invoke(rewrite_messages).content #Gies us a normal query "What is his name?"
    #Made by Kunsh Bhatia
    retriever = database.as_retriever(search_kwargs={"k": 5}) #Top 5 best results

    relevant_docs = retriever.invoke(rewritten_query) #context

    video_context = "\n\n".join([doc.page_content for doc in relevant_docs])

    model = ChatGroq(
        api_key=os.getenv(groq_api),
        temperature=0.1,
        model_name="llama-3.1-8b-instant"
            )

    final_prompt = f"""You are a precise video question-answering assistant.
        Answer ONLY from the retrieved context.
        
        Retrieved Context : {video_context}
        User Question : {rewritten_query}
        
        Instructions:
        - We are making a RAG for transcript of a Youtube Video.
        - Focus only on the user's question.
        - If exact answer is unavailable, say : "I don't know based on this video."
        - Keep answer long enough and properly informative with respect to the context to keep the user engaged 
        - You are allowed to use internet and external sources to gather information about a specific part of context to make user understand better."""

    final_messages = [
            SystemMessage(content="You answer questions from retrieved context."),
            HumanMessage(content=final_prompt)]
    #Made by Kunsh Bhatia
    result = model.invoke(final_messages)

        #print(f"Query:{query}")
        #print(f"Rewritten Query:{rewritten_query}")
        #print(f"Result:{result.content}")
        #print("\n" + "=" * 70)

    return result.content,rewritten_query

if __name__ == '__main__':
    rag_retriever()

    ## Can also download english as well as local language transcript
    ## Making sure DB doesn't get mixed for multiple users

#Made by Kunsh Bhatia