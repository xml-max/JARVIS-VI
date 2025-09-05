import os, time, threading
from watchdog.observers import Observer
from Jarvis.config import config
import json
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from datetime import datetime, timedelta
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.chat_models import ChatOpenAI
from langchain.llms import VertexAI
from langchain.schema.messages import SystemMessage, HumanMessage
from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredEPubLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

openai_api_key = config.openai_api_key or os.environ.get("OPENAI_API_KEY")
google_project_id = config.google_project_id or os.environ.get("GOOGLE_PROJECT_ID")
google_creds_path = config.google_creds_path or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

CHROMA_PATH = "./jarvis_chroma"
os.makedirs(CHROMA_PATH, exist_ok=True)

embedding = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)

ollama = config.ollama
openai = config.openai
vertexai = config.vertexai


# ⏱️ STM memory state
short_term_memory = {
    "messages": [],
    "last_updated": datetime.now()
}

# System instruction
SYSTEM_INSTRUCTION = """
You are JARVIS-VI, inspired by JARVIS from the MCU.

Reply ONLY in strict JSON format:
{
  "response": "...",
  "innerthought": "...",
  "protocol": "..."
}

Available protocols:
greeting, weather, system_stats, shutdown, reboot, hibernate, lock , emergency_shutdown, news, youtube, note, none, what can you do, exit.

If unsure, use protocol "none".
If user asks you to execute a non-existing protocol, first check for a similar one. If none, use "none".
If user requests system_stats or news, respond: "ok sir, waiting for API fetch", and wait for the next protocol response.
If protocol response is not empty, use it as context.
After receiving a protocol response, set protocol to "none".
"""
BOOKS_PATH = "./books"
os.makedirs(BOOKS_PATH, exist_ok=True)

def load_and_split_file(file_path):
    """Load and split a single book file into chunks."""
    if file_path.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")
    elif file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".epub"):
        loader = UnstructuredEPubLoader(file_path)
    else:
        return []

    try:
        docs = loader.load()
        for d in docs:
            d.metadata["source"] = os.path.basename(file_path)
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return splitter.split_documents(docs)
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return []

def index_books():
    """Index all non-indexed books in ./books."""
    existing = vectorstore.get(include=["metadatas"])
    existing_sources = {m.get("source") for m in existing["metadatas"] if m}

    BATCH_SIZE = 5000
    total_chunks = 0

    for fname in os.listdir(BOOKS_PATH):
        path = os.path.join(BOOKS_PATH, fname)
        if os.path.isfile(path) and fname not in existing_sources:
            print(f"📖 Indexing: {fname}")
            chunks = load_and_split_file(path)

            if chunks:
                # Process in batches
                for i in range(0, len(chunks), BATCH_SIZE):
                    batch = chunks[i : i + BATCH_SIZE]
                    vectorstore.add_documents(batch)
                    print(f"   📦 Added batch {i//BATCH_SIZE+1} with {len(batch)} chunks")

                # Only needed if you're using langchain_community.Chroma
                if hasattr(vectorstore, "persist"):
                    vectorstore.persist()

                total_chunks += len(chunks)
                print(f"✅ Finished indexing {fname} ({len(chunks)} chunks).")

    if total_chunks > 0:
        print(f"🎉 Added {total_chunks} chunks total into Chroma.")
    else:
        print("ℹ️ No new books to index.")


class BookWatcher(FileSystemEventHandler):
    """Watch for new books and index them automatically."""
    def on_created(self, event):
        if not event.is_directory:
            print(f"📂 New file detected: {event.src_path}")
            index_books()

def start_book_watcher():
    observer = Observer()
    observer.schedule(BookWatcher(), BOOKS_PATH, recursive=False)
    observer.start()
    print(f"👀 Watching {BOOKS_PATH} for new books...")

    def _keep_alive():
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    threading.Thread(target=_keep_alive, daemon=True).start()

def retrieve_memories(query: str, k: int = 3) -> str:
    """Retrieve relevant past memory or book knowledge."""
    try:
        data = json.loads(query.replace("'", '"'))  # replace single quotes if needed
        query = data.get("prompt", "")
    except Exception as e:
        query = query 
    try:
        results = vectorstore.similarity_search(query, k=k)
    except Exception as e:
        return f"[Memory retrieval error: {e}]"

    if not results:
        return ""

    formatted_results = []
    for doc in results:
        source = doc.metadata.get("source", "general memory")
        formatted_results.append(f"- From {source}: {doc.page_content}")

    return "\n".join(formatted_results)

def reset_short_term_memory():
    short_term_memory["messages"] = []
    short_term_memory["last_updated"] = datetime.now()

def chat(user_input: str) -> dict:
    if user_input.strip() == "":
        return {
            "response_text": "",
            "innerthought": "User input was empty.",
            "protocol": "none"
        }, ""
    else:
        now = datetime.now()
        # Clear STM if more than 1 hour passed
        if now - short_term_memory["last_updated"] > timedelta(hours=1):
            reset_short_term_memory()

        short_term_memory["last_updated"] = now

        # Retrieve long-term memory
        memories = retrieve_memories(user_input)
        memory_context = f"Relevant memories:\n{memories}\n\n" if memories else ""

        # Add new user message to STM
        user_msg = HumanMessage(content=f"{memory_context}User: {user_input}")
        short_term_memory["messages"].append(user_msg)

        # Combine messages
        messages = [SystemMessage(content=SYSTEM_INSTRUCTION)] + short_term_memory["messages"]

        if ollama:
            model = ChatOllama(model="llama3.2-vision", temperature=0.5)
            response = model(messages)
        elif openai:
            model = ChatOpenAI(
                model_name="gpt-4",
                temperature=0.7,
                openai_api_key=openai_api_key
            )
            response = model(messages)            
        elif vertexai:
            model = vertex_chat = VertexAI(
            model_name="gemini-pro",
            project=google_project_id,
            location="us-central1"  # adjust if needed
            )
            response = model(messages)

        try:
            parsed = json.loads(response.content)
            response_text = parsed.get("response", "No response text available.")
            innerthought = parsed.get("innerthought", "No inner thoughts available.")
            protocol = parsed.get("protocol", "none")
        except Exception as e:
            response_text = response.content
            innerthought = f"Parsing error: {str(e)}"
            protocol = "error"

        # Append assistant reply to STM
        short_term_memory["messages"].append(
            SystemMessage(content=json.dumps({
                "response": response_text,
                "innerthought": innerthought,
                "protocol": protocol
            }))
        )

        return {
            "response_text": response_text,
            "innerthought": innerthought,
            "protocol": protocol 
        },response.content
    
index_books()
print("📚 Initial book indexing complete.")
start_book_watcher()
print("👀 Book watcher started.")