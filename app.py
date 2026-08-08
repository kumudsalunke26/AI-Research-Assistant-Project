import streamlit as st
from dotenv import load_dotenv
from graph.workflow import workflow
from utils.pdf_loader import extract_text
from utils.chunking import split_text
from utils.embeddings import create_embeddings
from database.chroma_db import store_embeddings
from memory.long_term_memory import save_memory
# -------------------------
# Load Environment Variables
# -------------------------
load_dotenv()
# -------------------------
# Streamlit Page
# -------------------------
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="📚",
)
st.title("📚 AI Research Assistant")
# -------------------------
# Chat History
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()
# -------------------------
# Sidebar
# -------------------------
with st.sidebar:
    st.header("⚙️ Options")
    uploaded_files = st.file_uploader(
        "📄 Upload Research Papers",
        type=["pdf"],
        accept_multiple_files=True
    )
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
# -------------------------
# PDF Processing
# -------------------------

if uploaded_files:

    for uploaded_file in uploaded_files:

        file_name = uploaded_file.name

        if file_name in st.session_state.processed_files:
            continue

        # Extract pages
        pages = extract_text(uploaded_file)

        # Split into chunks with page numbers
        chunks = split_text(pages)

        # Create embeddings
        embeddings = create_embeddings(chunks)

        # Store into Chroma
        store_embeddings(
            chunks,
            embeddings,
            file_name
        )

        st.session_state.processed_files.add(
            file_name
        )

        st.success(
            f"✅ {file_name} processed successfully!"
        )

        st.write(
            f"Pages: {len(pages)}"
        )

        st.write(
            f"Chunks: {len(chunks)}"
        )

        st.write(
            f"Embeddings: {len(embeddings)}"
        )
# -------------------------
# Display Previous Messages
# -------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(
            message["content"]
        )
# -------------------------
# Chat Input
# -------------------------
prompt = st.chat_input(
    "Ask me anything..."
)
# -------------------------
# User Query
# -------------------------
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )
    # Save user query into long-term memory
    save_memory(prompt)
    try:
        state = {
            "question": prompt,
            "messages": st.session_state.messages,
            "search_query": "",
            "documents": [],
            "context": "",
            "memory": "",
            "tool": "",
            "answer": ""
        }
        result = workflow.invoke(state)
        print("\n========== WORKFLOW ==========")
        print(result)
        print("==============================")
        answer = result["answer"]
        documents = result["documents"]
        tool = result["tool"]
        st.info(
            f"🛠 Tool Used: {tool}"
        )
        with st.chat_message("assistant"):
            st.markdown(answer)
            st.markdown(
                "### 📌 Sources"
            )
            if documents:
                shown = set()
                for doc in documents:
                    source = doc.metadata.get(
                        "source",
                        "Unknown"
                    )
                    page = doc.metadata.get(
                        "page",
                        "?"
                    )
                    key = (source, page)
                    if key in shown:
                        continue
                    shown.add(key)
                    if isinstance(page, int):
                        page += 1
                    st.markdown(
                        f"- {source} | Page {page}"
                    )
            else:
                st.write(
                    "No sources retrieved."
                )
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )
    except Exception as e:
        st.error(
            f"⚠️ Error: {e}"
        )