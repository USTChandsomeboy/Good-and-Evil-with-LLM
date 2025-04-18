import os
import logging
import getpass
import os

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"
# from dotenv import load_dotenv
# load_dotenv(override=True)
temperature = 0.4


# def create_hf_llm(model_type="prometheus"):
#     from langchain_huggingface import HuggingFacePipeline
#     if model_type == "prometheus":
#         hf_llm = HuggingFacePipeline(
#             model_id="prometheus-eval/prometheus-7b-v2.0",
#             # task="text-generation",
#         )
#     elif model_type == "gpt2":
#         hf_llm = HuggingFacePipeline(
#             model_id="gpt2",
#             task="text-generation",
#         )
#     else:
#         raise ValueError(f"Unsupported model type: {model_type}")
#     return hf_llm

# def create_llama_llm():
#     from langchain_ollama import ChatOllama
#     llama_llm = ChatOllama(
#         model="llama3.2",
#         temperature=temperature,
#         max_tokens=50000,
#     )
#     return llama_llm

def create_gpt4o_llm():
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=temperature,
        # max_tokens=50000,
    )
    return llm

def create_llm(backbone="gpt4o"):
    if backbone == "gpt4o":
        logging.info("Creating OpenAI LLM")
        return create_gpt4o_llm()
    # elif backbone == "llama":
    #     return create_llama_llm()
    else:
        raise ValueError(f"Unsupported backbone: {backbone}")


if __name__ == "__main__":
    llm = create_gpt4o_llm()
    # llm = create_llama_llm()
    query = "How to create a chatbot"
    response = llm.invoke(query)
    print(response)
