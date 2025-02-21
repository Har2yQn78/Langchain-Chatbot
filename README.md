# Langchain Chatbot

This is a simple test project that demonstrates the integration of several cutting-edge technologies to build a question-answering system using vector search and language models.

## Overview

This project leverages the following key technologies:
- **Mistralai:** Used for generating embeddings and powering the chat model.
- **Langchain:** Provides a structured way to chain together language model calls, manage document processing, and handle prompt templates.
- **Upstash:** Acts as the vector store for document embeddings and similarity search.
- **FastAPI:** Serves as the web framework to expose the endpoints for the chain.

The system retrieves relevant Wikipedia content about cities, splits the text into manageable chunks, stores the embeddings, and answers user questions using context retrieved from the vector store.

## Repository

The repository for this project is available on GitHub:  
[https://github.com/Har2yQn78/Langchain-Chatbot.git](https://github.com/Har2yQn78/Langchain-Chatbot.git)

## File Structure

- **main.py:** Sets up a FastAPI web server with endpoints to interact with the language model chain.
- **utils.py:** Contains utility functions and configurations to create embeddings, set up the vector store, and build the model chain.
- **Configuration Files:** Environment variables and API keys are managed via `decouple`.

## Setup & Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Har2yQn78/Langchain-Chatbot.git
   cd Langchain-Chatbot

2. **Create a Virtual Environment and Install Dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**

   Create a .env file in the project root and include the following keys:
   1.  MISTRAL_API_KEY
   2. HF_TOKEN
   3. UPSTASH_VECTOR_REST_URL
   4. UPSTASH_VECTOR_REST_TOKEN

4. **Run the Application**

   ```bash
   uvicorn main:app --host localhost --port 8100
   ```
   
Visit http://localhost:8100 to see the home page.

## Usage
1. Home Endpoint:

   Accessing the root endpoint (/) returns a simple welcome message.
   
2. Chain Endpoint:

   The /chain/playground/ endpoint integrates the document retrieval and language model chain to answer queries using context derived
from Wikipedia.


## Future Improvements
This is a simple test implementation. Future updates include:
1. Expanding and modifying data sources.
2. Redesigning the user interface (UI) for an enhanced user experience.
3. Adding new features and refining overall functionality.



