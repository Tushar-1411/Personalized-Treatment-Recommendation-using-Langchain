from cgitb import handler
from fastapi import FastAPI
import os
from langchain.vectorstores import FAISS
from langchain_community.embeddings.huggingface import HuggingFaceInstructEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFaceHub
from dotenv import load_dotenv
load_dotenv()

HUGGING_FACE_API = os.getenv("HUGGINGFACEHUB_API_TOKEN")
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
embeddings = HuggingFaceInstructEmbeddings()
vector_db_file_path = "faiss_index"


query_prompt = PromptTemplate(
    template= """From the retreived similar documents only state the medications name along with their use case and the lifestyle modifications
     and if you dont find a match in the knowledge base just reply I DONT KNOW and dont make up an answer. Keep the answer short and concise.
    Question : {query} """,
    input_variables= []
)


def get_vector_db(vector_db_path, embeddings = embeddings):
    return FAISS.load_local(vector_db_path, embeddings)

def initialize_llm_qa_chain(repo_id, temperature = 0.2):
    repo_id = repo_id
    llm = HuggingFaceHub(
        repo_id = repo_id, model_kwargs = {"temperature": temperature},
        huggingfacehub_api_token = HUGGING_FACE_API,
    )

    qa = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type = "stuff",
        retriever = database.as_retriever(search_kwargs={"k": 6})
    )
    return qa

def get_output(query, qa_chain):
    formatted_query = query_prompt.format(query = query)
    output = qa_chain.run(formatted_query)
    return output 

database = get_vector_db(vector_db_file_path)
qa_chain = initialize_llm_qa_chain(repo_id = repo_id)

app = FastAPI()

@app.get("/diabetes/recommendation/{input}")
def generate_treatment(input : str):
    output = get_output(query = input, qa_chain = qa_chain)
    return {"treatment" : output}

