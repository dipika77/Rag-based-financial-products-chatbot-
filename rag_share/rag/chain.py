from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_groq import ChatGroq
from .config import GROQ_API_KEY, LLM_MODEL


CONTEXTUALIZE_PROMPT = """Given the chat history and the latest user question, \
rewrite the question as a fully standalone question that can be understood \
without the chat history. Do NOT answer it — just rewrite if needed, otherwise return it as-is."""

SYSTEM_PROMPT = """You are a precise assistant for Best Finance Company (BFC). You answer questions about BFC deposit products using ONLY the information in the provided context.

## RULES

1. Answer ONLY from the provided context. Never use outside knowledge or make assumptions.
2. If the answer is not explicitly present in the context, respond with: "Sorry, I couldn't find this information in the provided documents."
3. When quoting charges, rates, balances, or document lists, reproduce them exactly as stated in the context — do not paraphrase numbers or requirements.
4. If multiple products match the question, list all of them with their details clearly.
5. Be concise and structured. Use bullet points or tables when the context presents data that way.
6. Never guess, infer, or extrapolate beyond what the context states.

CONTEXT:
{context}"""


def _get_llm():
    return ChatGroq(model=LLM_MODEL, api_key=GROQ_API_KEY, temperature=0)


def _format_docs(docs):
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def get_rag_chain(retriever):
    llm = _get_llm()

    contextualize_prompt = ChatPromptTemplate.from_messages([
        ("system", CONTEXTUALIZE_PROMPT),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    def invoke(inp: dict) -> dict:
        # Rewrite follow-up question into standalone only when there is history
        if inp["chat_history"]:
            standalone = (contextualize_prompt | llm | StrOutputParser()).invoke(inp)
        else:
            standalone = inp["input"]

        docs = retriever.invoke(standalone)
        context = _format_docs(docs)

        answer = (qa_prompt | llm | StrOutputParser()).invoke({
            "input": inp["input"],
            "chat_history": inp["chat_history"],
            "context": context,
        })
        return {"answer": answer}

    return RunnableLambda(invoke)
