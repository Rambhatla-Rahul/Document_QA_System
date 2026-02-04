import streamlit as st
import requests

UPLOAD_API_URL = "http://127.0.0.1:8000/document/upload"
QUERY_API_URL = "http://127.0.0.1:8000/query"

st.set_page_config(page_title="PDF RAG System", layout="centered")
st.title("📄 PDF → RAG Question Answering")

# ---- SESSION STATE ----
if "file_id" not in st.session_state:
    st.session_state.file_id = None

# ---- FILE UPLOAD ----
uploaded_file = st.file_uploader(
    "Upload a PDF file",
    type=["pdf"]
)

if uploaded_file is not None:
    st.write("### File details")
    st.write({
        "filename": uploaded_file.name,
        "size_kb": round(uploaded_file.size / 1024, 2)
    })

    if st.button("Upload & Process"):
        with st.spinner("Uploading and processing PDF..."):
            try:
                files = {
                    "file": (uploaded_file.name, uploaded_file, "application/pdf")
                }

                response = requests.post(UPLOAD_API_URL, files=files)

                if response.status_code == 200:
                    data = response.json()
                    file_details = data["file_details"]

                    st.session_state.file_id = file_details["file_id"]

                    st.success("PDF ingested successfully ✅")

                    st.subheader("📊 Ingestion Summary")
                    st.write({
                        "Pages with text": file_details["pages_with_text"],
                        "Pages with OCR": file_details["pages_with_ocr"],
                        "Total characters": file_details["total_chars"],
                        "File ID": file_details["file_id"]
                    })

                else:
                    st.error(f"Upload failed ({response.status_code})")
                    st.json(response.json())

            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to FastAPI server")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

# ---- QUERY SECTION ----
if st.session_state.file_id:
    st.divider()
    st.subheader("💬 Ask a question about the document")

    question = st.text_input(
        "Enter your question",
        placeholder="What is this document about?"
    )

    if st.button("Ask"):
        if not question.strip():
            st.warning("Please enter a question")
        else:
            with st.spinner("Searching document and generating answer..."):
                try:
                    payload = {
                        "file_id": st.session_state.file_id,
                        "question": question
                    }

                    response = requests.post(QUERY_API_URL, json=payload)

                    if response.status_code == 200:
                        result = response.json()

                        st.success("Answer generated ✅")

                        st.markdown("### 🧠 Answer")
                        st.write(result.get("answer", ""))

                        if "sources" in result:
                            st.markdown("### 📚 Sources")
                            for src in result["sources"]:
                                meta = src.get("metadata", {})
                                page = meta.get("page", "Unknown")
                                chunk = meta.get("chunk_id", "Unknown")
                                score = round(src.get("score", 0), 3)

                                st.write(f"- Page {page} | Chunk {chunk} (score: {score})")

                    else:
                        st.error(f"Query failed ({response.status_code})")
                        st.json(response.json())

                except requests.exceptions.ConnectionError:
                    st.error("❌ Could not connect to FastAPI server")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")