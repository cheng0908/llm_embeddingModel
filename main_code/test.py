import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate

os.environ["OPENAI_API_KEY"] = "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"
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
prompt = hub.pull("rlm/rag-prompt")

# Only keep post title, headers, and content from the full HTML.
bs4_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs={"parse_only": bs4_strainer},
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)

docs = loader.load()
all_splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})


vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum and keep the answer as concise as possible.
Always say "thank you" at the end of the answer.

{context}

Question: {question}

Helpful Answer:"""
custom_rag_prompt = PromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | custom_rag_prompt
    | llm
    | StrOutputParser()
)

print(rag_chain.invoke("What is Task Decomposition?"))

