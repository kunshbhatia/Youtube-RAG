import streamlit as st
import uuid
from data_inegstion import data_ingestion
from RAG_retriever import rag_retriever
import random

#Page Config
st.set_page_config(page_title="YouTube RAG Chat",page_icon="https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg"
                   ,initial_sidebar_state="expanded",layout="wide")

#Creating Session_id to make sure any number of active users can use the app at same time with no data exchange
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4()) #TO make sure no two sessions merge at one time
#Made by Kunsh Bhatia
if "messages" not in st.session_state: #Response by RAG
    st.session_state.messages = []

if "queries" not in st.session_state: #Queries asked
    st.session_state.queries = []

if "video_processed" not in st.session_state: #Allowing sidebar to load first then chat
    st.session_state.video_processed = False

if "video_details" not in st.session_state: #Details of the video 
    st.session_state.video_details = {}

st.markdown( #Heading
    """
    <h1 style='display: flex; align-items: center; gap: 10px;'>
        <img src='https://cdn-icons-png.flaticon.com/512/1384/1384060.png' width='40'>
        YouTube RAG Chat
    </h1>
    """,
    unsafe_allow_html=True
)
#Made by Kunsh Bhatia
with st.sidebar:

    st.header("Upload YouTube Video")

    url = st.text_input("Enter YouTube URL")

    if st.button("Process Video"):

        # Reset old chat when a new link is given by user
        st.session_state.messages = []
        st.session_state.queries = []

        if url:

            with st.spinner("Processing Video... 👀\nThis will take a few seconds"):

                (_,text_data,text_in_english,title,description,channel,views,duration,thumbnail) = data_ingestion(video_link=url,
                                                                session_id=st.session_state.session_id)

            st.session_state.video_details = { #Basic info of video
                "title": title,
                "description": description,
                "channel": channel,
                "views": views,
                "duration": duration,
                "thumbnail": thumbnail,
                'Transcript':text_data if text_data else " ",
                "English_Transcript":text_in_english}

            st.session_state.video_processed = True
            st.success("Video Processed Successfully ✅")

        else:
            st.warning("Please enter a YouTube URL")
    #Made by Kunsh Bhatia
    if st.session_state.video_details:

        details = st.session_state.video_details

        st.image(details["thumbnail"],use_container_width=True)

        st.markdown(f"### {details['title']}")

        st.markdown(f"**Channel :** {details['channel']}")

        st.markdown(f"**Views :** {details['views']:,}")

        minutes = details["duration"] // 60
        seconds = details["duration"] % 60

        st.markdown(f"**Duration :** {minutes} min {seconds} sec")

        with st.spinner("Loading Desctiption"):
            with st.expander("Video Description"):
                st.write(details["description"])
        
        with st.expander("Video Transcript in Original Language"): #To download video's transcript
            st.download_button(label="Download Text File" , data = details["Transcript"],
                file_name = f"transcript_downloaded.txt", mime = "text/plain")
            
        with st.expander("Video Transcript in English Language"):
            st.download_button(label="Download Text File",data=details["English_Transcript"],
                file_name=f"English_transcript_downloaded.txt",mime="text/plain")
            
        st.markdown(""" <hr style="margin-top: 2rem; margin-bottom: 0;"> <div style="text-align: center; color: grey; font-size: 14px; padding: 0px 0;"> Made by Kunsh Bhatia </div> """, unsafe_allow_html=True)

chat_container = st.container()

with chat_container:

    for role, message in st.session_state.messages: #TO make sure old messages stay in place when new query is processed by user
        with st.chat_message(role):
            st.markdown(message)
#Made by Kunsh Bhatia
if st.session_state.video_processed:

    query = st.chat_input("Ask Question From Video")

    if query:
        st.session_state.messages.append(("user", query))
        st.session_state.queries.insert(0,query)

        with chat_container:

            with st.chat_message("user"):
                st.markdown(query)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                wait_choices = ["🔍 Analysing Query...", "🧠 Understanding your question...", "📚 Searching video knowledge base...", "🎥 Looking through video transcript...", "⚡ Retrieving relevant context...", "🤖 Generating intelligent response...", "📝 Preparing final answer...", "🔎 Finding the most relevant chunks...", "📖 Reading transcript sections...", "💡 Thinking about the best response...", "🚀 Running RAG pipeline...", "🧩 Connecting important information...", "📡 Fetching semantic matches...", "🛠️ Processing embeddings...", "🎯 Finding accurate answer...", "🧠 Reasoning over transcript...", "📂 Searching vector database...", "✨ Crafting response for you...", "⏳ Almost done...", "🔬 Deeply analysing the video content..."]
                with st.spinner(random.choice(wait_choices)):
                    answer,_ = rag_retriever(query=query,session_id=st.session_state.session_id,
                        queries=st.session_state.queries) #Loading RAG's answer
                message_placeholder.markdown(answer)

        st.session_state.messages.append(("assistant", answer))
        #Made by Kunsh Bhatia
else:
    st.info("Please process a YouTube video from the sidebar first.")

#Footer
st.markdown(
    """
    <style>
    .footer {position: fixed;bottom: 0;left: 0;width: 100%;background-color: white;text-align: center;padding: 10px;color: grey;font-size: 14px;border-top: 1px solid #e6e6e6;z-index: 100;}
    .block-container {padding-bottom: 3rem;}
    </style>

    <div class="footer">
        This is an AI system. AI can make mistakes.
    </div>
    """,
    unsafe_allow_html=True)