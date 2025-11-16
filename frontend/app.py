import streamlit as st
import requests
from streamlit_option_menu import option_menu
import sys, os
sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("."))

from core.config import get_settings
settings = get_settings()

FASTAPI_URL = "http://127.0.0.1:8000"   # your backend


st.set_page_config(page_title="LawLens", layout="centered")



# st.markdown(
#     """
#     <div style="text-align: center;">
#         <h1 style="color:#ADD7FF;">LawLens</h1>
#         <h2 style="color:#ADD7FF;">Voice enabled legal document summarizer with RAG</h3>   
#     </div>

#     <br><br>

#     <p style="text-align:center; font-size:18px; color:2687E0;">
#         Welcome to <strong>LawLens</strong> — an AI-powered platform that lets you 
#         effortlessly summarize legal documents and effortlessly interact with them through smart, context aware Q&A.
#     </p>
#     """,
#     unsafe_allow_html=True
# )



# ---------------------------
# Sidebar Title
# ---------------------------
st.sidebar.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color:#61D640;">NAVIGATION</h1>
        <br><br> 
    """,
    unsafe_allow_html=True
)


# ------------------ Sidebar Styling ------------------
st.markdown(
    """
    <style>
        .stApp {
            background-color: #0d1117;
        }
        [data-testid="stSidebar"] {
            background-color: #0d1117;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------ Sidebar Menu ----------------------
with st.sidebar:
    page = option_menu(
        menu_title=None,
        options=["Home" , "Summarize Document", "RAG - Intelligent Q&A"],
        icons=["house" , "file-text", "chat-dots"],
        default_index=0,
        styles={
            "container": {
                "padding": "0 !important",
                "background-color": "#0d1117",
            },
            "icon": {
                "color": "white",
                "font-size": "20px",
            },
            "nav-link": {
                "color": "white",
                "font-size": "18px",
                "text-align": "left",
                "margin": "5px 0",
                "--hover-color": "#1a1f24",
            },
            "nav-link-selected": {
                "background-color": "#161b22",
                "border-radius": "10px",
                "color": "white",
                "font-weight": "600",
            },
        }
    )

# ------------------ Page Display ----------------------

# ------------------ Page Display ----------------------
if page == "Home":

    st.markdown(
    """
    <div style="text-align: center;">
         <h1 style="color:#ADD7FF;">LawLens</h1>
         <h2 style="color:#ADD7FF;">Voice enabled legal document summarizer with RAG</h2>   
    </div>

    <br><br>

    <p style="text-align:center; font-size:18px; color:2687E0;">
         Welcome to <strong>LawLens</strong> — an AI-powered platform that lets you 
         effortlessly summarize legal documents and effortlessly interact with them through smart, context aware Q&A.
    </p>
    """,
     unsafe_allow_html=True
 )


#-------------------------
# Summarize Document Page
#-------------------------
if page == "Summarize Document":

    st.markdown(
        """
        <h2 style='color:#ADD7FF; text-align:center;'>📄 Summarize Your Legal Document</h2>
        <br>
        <h3 style='text-align:center; color:white;'>
            Upload your document and receive an AI-generated summary instantly.
        </h3>
        <br>
        <br>
        """,
        unsafe_allow_html=True
    )

    ## ------------------ File Upload ----------------------
    st.markdown(
    """
    <label style="
        font-size:20px; 
        font-weight:600; 
        color:#CAE354;
    ">
        Upload your legal document
    </label>
    <br>
    """,
    unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
    "",
    type=["pdf", "docx", "txt"]
    )   
    st.markdown("<br><br>", unsafe_allow_html=True)



    # ------------------ Language Selection ----------------------
    st.markdown(
    """
    <label style="
        font-size:20px; 
        font-weight:600; 
        color:#CAE354;
    ">
        Choose a language
    </label>
    <br>
    """,
    unsafe_allow_html=True
    )

    language = st.selectbox(
        "",
        settings.SUPPORTED_LANGUAGES

    )
    st.markdown("<br><br>", unsafe_allow_html=True)


    # ------------------ Text-to-Speech ----------------------
    st.markdown(
    """
    <label style="
        font-size:20px; 
        font-weight:600; 
        color:#CAE354;
    ">
        Do you want to listen to the summary?
    </label>
    <br>
    """,
    unsafe_allow_html=True
    )

    tts = st.checkbox(
        "Enable Text-to-Speech",
        value = False
    )
    st.markdown("<br><br>", unsafe_allow_html=True)




    # ------------------ Summarize Button ----------------------
    
    if st.button("Summarize Document", type="primary"):
        st.markdown("<br><br>", unsafe_allow_html=True)

        # If user didn't upload anything
        if uploaded_file is None:
            st.error("Please upload a document first.")

        else:
            # Show loading animation while processing
            with st.spinner("Summarizing your document..."):
                try:
                    # Send file + data to FastAPI backend
                    response = requests.post(
                        f"{FASTAPI_URL}/summarize",
                        files={"file": uploaded_file},
                        data={"language": language, "tts": tts}
                    )
                    if response.status_code != 200:
                        st.markdown("<br><br>", unsafe_allow_html=True)
                        st.error(f"Error: {response.json().get('detail')}")

                    else:
                        result = response.json()

                        st.success("Summary generated!")
                        st.markdown("<br><br>", unsafe_allow_html=True)

                        st.markdown(
                            f"""
                            <div style="
                                background-color:#161b22;
                                padding:20px;
                                border-radius:12px;
                                color:#e5e5e5;
                                border:1px solid #2c323c;
                                font-size:16px;
                            ">
                                {result.get("summary", "No summary returned.")}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        if tts and "audio_bytes" in result:
                            st.audio(bytes.fromhex(result["audio_bytes"]))

                except Exception as e:
                    st.error(f"Error: {e}")

                    


    

    

















