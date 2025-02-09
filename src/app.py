import chainlit as cl
import asyncio
from rag import extract_text_from_pdf, chunk_text, get_embeddings, retrieve_chunks, build_faiss_index
from websearchagent import search_agent
from ragagent import rag_agent
from mainagent import main_agent

vector_db = None
chunks = None

@cl.on_chat_start
async def start():
    global vector_db, chunks

    files = None
    while files is None:
        files = await cl.AskFileMessage(
            content="📁 Please upload PDF files to begin!", 
            accept={"application/pdf": [".pdf"]},
            max_files=5,
            max_size_mb=50
        ).send()

    status_msg = await cl.Message(content="📂 Loading PDFs... Please wait.").send()

    try:
        pdf_paths = [i.path for i in files]
        text = extract_text_from_pdf(pdf_paths)
    except Exception as e:
        await cl.Message(content=f"❌ Error loading PDFs: {str(e)}").send()
        return

    await cl.Message(content="📄 Chunking text... ⏳", id=status_msg.id).update()
    chunks = chunk_text(text)

    await cl.Message(content="🔢 Generating embeddings... ⏳", id=status_msg.id).update()
    embeddings = get_embeddings(chunks)

    await cl.Message(content="📦 Building vector database... ⏳", id=status_msg.id).update()
    vector_db = build_faiss_index(embeddings)

    await cl.Message(content="✅ All steps completed! You can now ask questions about the uploaded PDFs. 🎉").send()

# Handle user queries after initial setup
@cl.on_message
async def handle_message(message):
    global vector_db, chunks

    if not vector_db or not chunks:
        await cl.Message(content="⚠️ The vector database is not ready yet. Please upload PDFs to begin.").send()
        return

    query = message.content

    # Define wrapper functions within the message handler
    def retrieve_chunks_wrapper(query):
        return retrieve_chunks(query, index=vector_db, chunks=chunks, top_k=3)

    def rag_agent_wrapper(query):
        return rag_agent(query=query, retrieve_chunks=retrieve_chunks_wrapper)

    # Get response from main_agent
    response = main_agent(query=message.content,rag_agent=rag_agent_wrapper, search_agent=search_agent)

    # Send the response back to the user
    await cl.Message(content=f"🤖 {response}").send()
