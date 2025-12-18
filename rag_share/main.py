from langchain_core.messages import HumanMessage, AIMessage
from rag.vectorstore import get_vectorstore
from rag.chain import get_rag_chain
from rag.config import TOP_K


def main():
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})
    rag_chain = get_rag_chain(retriever)

    chat_history = []

    print("BFC Deposit Assistant (type 'quit' to exit)")
    print("-" * 50)

    while True:
        question = input("\nQuestion: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            break
        if not question:
            continue

        result = rag_chain.invoke({"input": question, "chat_history": chat_history})
        answer = result["answer"]
        print(f"\nAnswer: {answer}")

        chat_history.extend([
            HumanMessage(content=question),
            AIMessage(content=answer),
        ])


if __name__ == "__main__":
    main()
