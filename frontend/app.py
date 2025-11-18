import base64
from io import BytesIO
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
    <br><br>
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

  
    # ------------------ File Upload --------------------------
    if "sample_file" not in st.session_state:
        st.session_state.sample_file = None
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
    
    uploaded_file = st.session_state.sample_file or st.file_uploader("", type=["pdf","docx","txt"])
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
"""
<p style="
    font-size:16px; 
    color:#ffffff;
    text-align:center;
">
    OR
</p>
""",
unsafe_allow_html=True
)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Use Sample Document"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sample_path = os.path.join(script_dir, "kome-text.pdf")

        with open(sample_path, "rb") as f:
            file_bytes = f.read()
            st.session_state.sample_file = BytesIO(file_bytes)
            st.session_state.sample_file.name = "kome-text.pdf"

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if uploaded_file:
        st.success(f"File ready: {uploaded_file.name}")


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

                        if tts and "audio" in result:

                            audio_bytes = base64.b64decode(result["audio"])

                            st.markdown("<br><br>", unsafe_allow_html=True)
                            st.markdown(
                                """
                                <label style="
                                    font-size:20px; 
                                    font-weight:600; 
                                    color:#CAE354;
                                ">
                                    Your speech is ready !
                                </label>
                                <br><br>
                                """,
                                unsafe_allow_html=True
                            )

                            st.audio(audio_bytes, format="audio/wav")

                except Exception as e:
                    st.error(f"Error: {e}")

                    


#------------------
# RAG - Intelligent Q&A
#------------------

if page == "RAG - Intelligent Q&A":
    st.markdown(
        """
        <h2 style='color:#ADD7FF; text-align:center;'>🤖 Intelligent Q&A</h2>
        <br>
        <h3 style='text-align:center; color:white;'>
            Ask questions about your legal document and receive a context aware AI-generated answer.
        </h3>
        <br>
        <br>
        """,
        unsafe_allow_html=True
    )


    # ------------------ File Upload for RAG ----------------------
    if "sample_file" not in st.session_state:
        st.session_state.sample_file = None
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
    
    uploaded_file = st.session_state.sample_file or st.file_uploader("", type=["pdf","docx","txt"])
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
"""
<p style="
    font-size:16px; 
    color:#ffffff;
    text-align:center;
">
    OR
</p>
""",
unsafe_allow_html=True
)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Use Sample Document"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sample_path = os.path.join(script_dir, "kome-text.pdf")

        with open(sample_path, "rb") as f:
            file_bytes = f.read()
            st.session_state.sample_file = BytesIO(file_bytes)
            st.session_state.sample_file.name = "kome-text.pdf"

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if uploaded_file:
        st.success(f"File ready: {uploaded_file.name}")


    if uploaded_file:

        try : 

            st.info("Processing your document...")

            #To convert Streamlit's upload file object into a real file that FastAPI can read as UploadFile.
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}

            response = requests.post(
                f"{FASTAPI_URL}/rag/index",
                files=files , 
                timeout = 40
            )

            # Handle response
            if response.status_code == 200:
                data = response.json()
                st.success("Index built successfully!")
                st.write(f"Chunks created: {data['chunks']}")

                st.markdown("<br><br>", unsafe_allow_html=True)

                st.session_state['rag_ready'] = True 

            else:
                st.error(f"Failed: {response.text}")

        except Exception as e:
            st.error(f"Error: {e}")

        
    
    #------------ Ask Question ------------
    if st.session_state.get('rag_ready'):
        st.markdown(
            """
            <label style="
                font-size:20px; 
                font-weight:600; 
                color:#CAE354;
            ">
                Ask a question about your document
            </label>
            <br>
            """,
        unsafe_allow_html=True
    )

        user_question = st.text_input(
        "",
            placeholder="e.g., What is the contract duration?"
        )

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown(
                """
                <label style="
                    font-size:20px; 
                    font-weight:600; 
                    color:#CAE354;
                ">
                    Specify Your Language for response
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

        # Ask button
        if st.button("Ask"):
            if not user_question.strip():
                st.warning("Please enter a question.")
        
            else:
                try :
                    with st.spinner("Getting answer..") :

                        payload = {"query": user_question , "language": language}

                        response = requests.post(
                        f"{FASTAPI_URL}/rag/ask",
                        json=payload
                    )           

                    # Handle response
                    if response.status_code == 200:
                        data = response.json()
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.success("Answer generated!")
                        st.write(data["answer"])

                        # Display source chunks if available
                        st.markdown("<br>", unsafe_allow_html=True)
                        if data.get("sources"):
                            st.markdown("### Retrieved Sources")
                            for idx, src in enumerate(data["sources"], 1):
                                with st.expander(f"Source {idx}"):
                                    st.write(src["content"])

                    else:
                        st.error(f"error generating answer: {response.text}")

                except Exception as e:
                    st.error(f"Error: {e}")

        

         


                  
           

# import streamlit as st
# import requests
# from streamlit_option_menu import option_menu
# import sys, os
# sys.path.append(os.path.abspath(".."))
# sys.path.append(os.path.abspath("."))

# from core.config import get_settings
# settings = get_settings()

# FASTAPI_URL = "http://127.0.0.1:8000"

# st.set_page_config(page_title="LawLens", layout="centered")

# # Initialize session state for each page
# if 'rag_ready' not in st.session_state:
#     st.session_state['rag_ready'] = False
# if 'current_page' not in st.session_state:
#     st.session_state['current_page'] = "Home"

# # Sidebar styling
# st.sidebar.markdown(
#     """
#     <div style="text-align: center;">
#         <h1 style="color:#61D640;">NAVIGATION</h1>
#         <br><br> 
#     """,
#     unsafe_allow_html=True
# )

# st.markdown(
#     """
#     <style>
#         .stApp {
#             background-color: #0d1117;
#         }
#         [data-testid="stSidebar"] {
#             background-color: #0d1117;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Sidebar menu
# with st.sidebar:
#     page = option_menu(
#         menu_title=None,
#         options=["Home", "Summarize Document", "RAG - Intelligent Q&A"],
#         icons=["house", "file-text", "chat-dots"],
#         default_index=0,
#         styles={
#             "container": {
#                 "padding": "0 !important",
#                 "background-color": "#0d1117",
#             },
#             "icon": {
#                 "color": "white",
#                 "font-size": "20px",
#             },
#             "nav-link": {
#                 "color": "white",
#                 "font-size": "18px",
#                 "text-align": "left",
#                 "margin": "5px 0",
#                 "--hover-color": "#1a1f24",
#             },
#             "nav-link-selected": {
#                 "background-color": "#161b22",
#                 "border-radius": "10px",
#                 "color": "white",
#                 "font-weight": "600",
#             },
#         }
#     )

# # Reset RAG state when navigating away from RAG page
# if st.session_state['current_page'] != page and page != "RAG - Intelligent Q&A":
#     st.session_state['rag_ready'] = False

# st.session_state['current_page'] = page

# # ==================== HOME PAGE ====================
# if page == "Home":
#     st.markdown(
#         """
#         <div style="text-align: center;">
#              <h1 style="color:#ADD7FF;">LawLens</h1>
#              <h2 style="color:#ADD7FF;">Voice enabled legal document summarizer with RAG</h2>   
#         </div>

#         <br><br>

#         <p style="text-align:center; font-size:18px; color:2687E0;">
#              Welcome to <strong>LawLens</strong> — an AI-powered platform that lets you 
#              effortlessly summarize legal documents and effortlessly interact with them through smart, context aware Q&A.
#         </p>
#         <br><br>
#         """,
#         unsafe_allow_html=True
#     )

# # ==================== SUMMARIZE DOCUMENT PAGE ====================
# elif page == "Summarize Document":
#     st.markdown(
#         """
#         <h2 style='color:#ADD7FF; text-align:center;'>📄 Summarize Your Legal Document</h2>
#         <br>
#         <h3 style='text-align:center; color:white;'>
#             Upload your document and receive an AI-generated summary instantly.
#         </h3>
#         <br>
#         <br>
#         """,
#         unsafe_allow_html=True
#     )

#     # File upload
#     st.markdown(
#         """
#         <label style="
#             font-size:20px; 
#             font-weight:600; 
#             color:#CAE354;
#         ">
#             Upload your legal document
#         </label>
#         <br>
#         """,
#         unsafe_allow_html=True
#     )

#     summarize_file = st.file_uploader(
#         "summarize_uploader",
#         type=["pdf", "docx", "txt"],
#         key="summarize_file_uploader"
#     )
#     st.markdown("<br><br>", unsafe_allow_html=True)

#     if summarize_file:
#         st.success(f"✓ File ready: {summarize_file.name}")

#     # Language selection
#     st.markdown(
#         """
#         <label style="
#             font-size:20px; 
#             font-weight:600; 
#             color:#CAE354;
#         ">
#             Choose a language
#         </label>
#         <br>
#         """,
#         unsafe_allow_html=True
#     )

#     summarize_language = st.selectbox(
#         "Language for summary",
#         settings.SUPPORTED_LANGUAGES,
#         key="summarize_language"
#     )
#     st.markdown("<br><br>", unsafe_allow_html=True)

#     # Text-to-Speech option
#     st.markdown(
#         """
#         <label style="
#             font-size:20px; 
#             font-weight:600; 
#             color:#CAE354;
#         ">
#             Do you want to listen to the summary?
#         </label>
#         <br>
#         """,
#         unsafe_allow_html=True
#     )

#     tts = st.checkbox(
#         "Enable Text-to-Speech",
#         value=False,
#         key="summarize_tts"
#     )
#     st.markdown("<br><br>", unsafe_allow_html=True)

#     # Summarize button
#     if st.button("Summarize Document", type="primary", key="summarize_btn"):
#         st.markdown("<br><br>", unsafe_allow_html=True)

#         if summarize_file is None:
#             st.error("❌ Please upload a document first.")
#         else:
#             with st.spinner("Summarizing your document..."):
#                 try:
#                     # Prepare files and data
#                     files = {"file": (summarize_file.name, summarize_file.getvalue())}
#                     data = {
#                         "language": summarize_language,
#                         "tts": str(tts)
#                     }

#                     response = requests.post(
#                         f"{FASTAPI_URL}/summarize",
#                         files=files,
#                         data=data,
#                         timeout=60
#                     )

#                     if response.status_code != 200:
#                         st.markdown("<br><br>", unsafe_allow_html=True)
#                         error_msg = response.json().get('detail', 'Unknown error')
#                         st.error(f"❌ Error: {error_msg}")
#                     else:
#                         result = response.json()
#                         st.success("✓ Summary generated!")
#                         st.markdown("<br><br>", unsafe_allow_html=True)

#                         st.markdown(
#                             f"""
#                             <div style="
#                                 background-color:#161b22;
#                                 padding:20px;
#                                 border-radius:12px;
#                                 color:#e5e5e5;
#                                 border:1px solid #2c323c;
#                                 font-size:16px;
#                             ">
#                                 {result.get("summary", "No summary returned.")}
#                             </div>
#                             """,
#                             unsafe_allow_html=True
#                         )

#                         if tts and "audio_bytes" in result:
#                             st.audio(bytes.fromhex(result["audio_bytes"]))

#                 except Exception as e:
#                     st.markdown("<br><br>", unsafe_allow_html=True)
#                     st.error(f"❌ Error: {str(e)}")

# # ==================== RAG PAGE ====================
# elif page == "RAG - Intelligent Q&A":
#     st.markdown(
#         """
#         <h2 style='color:#ADD7FF; text-align:center;'>🤖 Intelligent Q&A</h2>
#         <br>
#         <h3 style='text-align:center; color:white;'>
#             Ask questions about your legal document and receive a context aware AI-generated answer.
#         </h3>
#         <br>
#         <br>
#         """,
#         unsafe_allow_html=True
#     )

#     # File upload for RAG
#     st.markdown(
#         """
#         <label style="
#             font-size:20px; 
#             font-weight:600; 
#             color:#CAE354;
#         ">
#             Upload your legal document
#         </label>
#         <br>
#         """,
#         unsafe_allow_html=True
#     )

#     rag_file = st.file_uploader(
#         "rag_uploader",
#         type=["pdf", "docx", "txt"],
#         key="rag_file_uploader"
#     )
#     st.markdown("<br><br>", unsafe_allow_html=True)

#     if rag_file:
#         try:
#             st.info("🔄 Processing your document...")

#             files = {"file": (rag_file.name, rag_file.getvalue())}

#             response = requests.post(
#                 f"{FASTAPI_URL}/rag/index",
#                 files=files,
#                 timeout=60
#             )

#             if response.status_code == 200:
#                 data = response.json()
#                 st.success("✓ Index built successfully!")
#                 st.write(f"**Chunks created:** {data['chunks']}")
#                 st.markdown("<br><br>", unsafe_allow_html=True)
#                 st.session_state['rag_ready'] = True

#             else:
#                 st.error(f"❌ Failed: {response.text}")
#                 st.session_state['rag_ready'] = False

#         except Exception as e:
#             st.error(f"❌ Error: {str(e)}")
#             st.session_state['rag_ready'] = False

#     # Ask question section
#     if st.session_state.get('rag_ready'):
#         st.markdown(
#             """
#             <label style="
#                 font-size:20px; 
#                 font-weight:600; 
#                 color:#CAE354;
#             ">
#                 Ask a question about your document
#             </label>
#             <br>
#             """,
#             unsafe_allow_html=True
#         )

#         user_question = st.text_input(
#             "Your question",
#             placeholder="e.g., What is the contract duration?",
#             key="rag_question"
#         )

#         st.markdown("<br><br>", unsafe_allow_html=True)

#         st.markdown(
#             """
#             <label style="
#                 font-size:20px; 
#                 font-weight:600; 
#                 color:#CAE354;
#             ">
#                 Specify Your Language for response
#             </label>
#             <br><br>
#             """,
#             unsafe_allow_html=True
#         )

#         rag_language = st.selectbox(
#             "Response language",
#             settings.SUPPORTED_LANGUAGES,
#             key="rag_language"
#         )

#         st.markdown("<br><br>", unsafe_allow_html=True)

#         # Ask button
#         if st.button("Ask", key="ask_btn"):
#             if not user_question.strip():
#                 st.warning("⚠️ Please enter a question.")
#             else:
#                 with st.spinner("Getting answer..."):
#                     try:
#                         payload = {
#                             "query": user_question,
#                             "language": rag_language
#                         }

#                         response = requests.post(
#                             f"{FASTAPI_URL}/rag/ask",
#                             json=payload,
#                             timeout=60
#                         )

#                         if response.status_code == 200:
#                             data = response.json()
#                             st.success("✓ Answer generated!")
#                             st.markdown(
#                                 f"""
#                                 <div style="
#                                     background-color:#161b22;
#                                     padding:20px;
#                                     border-radius:12px;
#                                     color:#e5e5e5;
#                                     border:1px solid #2c323c;
#                                     font-size:16px;
#                                 ">
#                                     {data["answer"]}
#                                 </div>
#                                 """,
#                                 unsafe_allow_html=True
#                             )

#                             # Display sources
#                             if data.get("sources"):
#                                 st.markdown("---")
#                                 st.markdown("### 📄 Retrieved Sources")
#                                 for idx, src in enumerate(data["sources"], 1):
#                                     with st.expander(f"Source {idx}"):
#                                         st.write(src.get("content", src))

#                         else:
#                             st.error(f"❌ Error generating answer: {response.text}")

#                     except Exception as e:
#                         st.error(f"❌ Error: {str(e)}")

#     else:
#         st.warning("⚠️ Please upload a document first to ask questions.")


    
    

    

















