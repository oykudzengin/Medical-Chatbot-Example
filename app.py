from flask import Flask, render_template, jsonify, request
from src.helper import download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import create_retrieval_chain
#from langchain.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os


#initialize the flask app
app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY= os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY= os.getenv("GOOGLE_API_KEY")
#OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY #saving it as an environment variable
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

embedding = download_embeddings()

index_name = "medical-chatbot"

docsearch = PineconeVectorStore.from_existing_index(
    embedding=embedding,
    index_name=index_name
)

#creating the chat now
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})
#creting the retriever to bring the top 3 most relevant documents

chatModel = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("user", "{input}"),
    ]

)

question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


#creating a basic home route
@app.route('/')
def index():
    return render_template('chat.html')


#another route to handle the chat messages
@app.route('/get', methods=["GET", "POST"])
def chat():
    msg= request.form["msg"]
    input = msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    print("Response: ", response["answer"])
    return str(response["answer"])



#execute the app
if __name__== '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

