from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain import hub
import os

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Initialize ChatOpenAI model
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Load prompt from hub
prompt = hub.pull("rlm/rag-prompt")

# Load text data from the binary file
file_path = '.\\downloaded_file_ddc0f3d0-e439-4291-9239-2b645ef66742.bin'
text_data = ''

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        text_data = file.read()

except FileNotFoundError:
    print(f"File not found: {file_path}")

except Exception as e:
    print(f"An error occurred: {e}")

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0, length_function=len)
all_splits = text_splitter.split_text(text_data)

# Create Chroma vectorstore from text chunks
vectorstore = Chroma.from_texts(all_splits, embedding=OpenAIEmbeddings())

# Create retriever
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

# Define a custom RAG prompt template
template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum and keep the answer as concise as possible.
Always say "thank you" at the end of the answer.

{context}

Question: {question}

Helpful Answer:"""
custom_rag_prompt = PromptTemplate.from_template(template)

# Define a RAG chain
rag_chain = (
    {"context": retriever | (lambda docs: "\n\n".join(doc.page_content for doc in docs)), "question": RunnablePassthrough()}
    | custom_rag_prompt
    | llm
    | StrOutputParser()
)

# Invoke the RAG chain with a sample question
result = rag_chain.invoke("Who is this article introducing?")

# Print the result
print(result)
