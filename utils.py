from decouple import config, AutoConfig
from typing import List
from mistralai import Mistral

from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import UpstashVectorStore
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

config = AutoConfig(search_path="/home/harry/Chatbot")

MISTRAL_API_KEY = config("MISTRAL_API_KEY")
UPSTASH_VECTOR_REST_URL = config("UPSTASH_VECTOR_REST_URL")
UPSTASH_VECTOR_REST_TOKEN = config("UPSTASH_VECTOR_REST_TOKEN")

class MistralEmbeddings(Embeddings):
    def __init__(self, model: str = "mistral-embed"):
        self.model = model
        self.client = Mistral(api_key=MISTRAL_API_KEY)
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        cleaned_texts = [t.replace("\n", " ") for t in texts]
        response = self.client.embeddings.create(
            model=self.model,
            inputs=cleaned_texts
        )
        return [e.embedding for e in response.data]
    
    def embed_query(self, text: str) -> List[float]:
        text = text.replace("\n", " ")
        response = self.client.embeddings.create(
            model=self.model,
            inputs=[text]
        )
        return response.data[0].embedding

embeddings = MistralEmbeddings()
store = UpstashVectorStore(
    embedding=embeddings,
    index_url=UPSTASH_VECTOR_REST_URL,
    index_token=UPSTASH_VECTOR_REST_TOKEN
)

retriever = store.as_retriever(
    search_type='similarity',
    search_kwargs={'k': 2}
)

LLM_CONFIG = {
    "api_key" : MISTRAL_API_KEY, 
}

model = ChatMistralAI(**LLM_CONFIG)

message = """
Answer the following question with insights drawn directly from the context. Be sure to include specific details from 
the provided context and keep your answer clear and relevant. Avoid using general phrases like 'based on Wikipedia' 
or 'according to sources.'

{question}

Context:
{context}
"""


prompt = ChatPromptTemplate.from_messages([("human", message)])

parser = StrOutputParser()

def get_chain():
    return {"context": retriever, "question": RunnablePassthrough()} | prompt | model | parser



