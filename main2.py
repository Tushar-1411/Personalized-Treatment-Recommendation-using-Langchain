from fastapi import FastAPI
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
load_dotenv()

llm = GoogleGenerativeAI(model = "gemini-pro",
                        client = "",
                        client_options="", transport="", # type: ignore
                        temperature = 0.3) # type: ignore
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001") # type: ignore
vector_db_file_path = "Gemini_Indexes"


template = """Your task is to recommend a treatment for diabetic pateints. You will be provided with a patient description including Age, BMI, primary symptoms,
secondary complications and allergies if any present. 
Generate a custom deatiled treatment such that it includes medications treating all the symptoms and complications listed in the description and how they help achieving it.
And you can change the treatment based on the knowledge because of the allergies mentioned accordingly. 
Only display the treatment as the output.
Use the provided context as a reference.
Stick STRICTLY to the context for answering:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)


def get_vector_db(vector_db_path, embeddings = embeddings):
    return FAISS.load_local(vector_db_path, embeddings)

def initialize_llm_qa_chain(retriever_object):
    chain = (
        {"context": retriever_object, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

def get_output(query, chain):
    output = chain.invoke(query)
    return output 

database = get_vector_db(vector_db_file_path)
retriever = database.as_retriever()
chain = initialize_llm_qa_chain(retriever)

app = FastAPI()

@app.get("/diabetes/recommendation/{input}")
def generate_treatment(input : str):
    output = get_output(query = input, chain = chain)
    return {"treatment" : output}


