from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEndpoint
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableLambda
from langchain_core.prompt_values import StringPromptValue 
from langchain_core.prompt_values import ChatPromptValue

title="ஜெயகாந்தனின்  சிறுகதைகள் -  தொகுப்பு - 1"
db_folder ="../vectordbs/content/"
embedding_model = "l3cube-pune/tamil-sentence-bert-nli"
vectordb = Chroma(persist_directory=f"{db_folder}{title}", embedding_function=HuggingFaceEmbeddings(model_name=embedding_model))

def prepare_input(prompt_value):
    if isinstance(prompt_value,StringPromptValue):
        return str(prompt_value.text)
    elif isinstance(prompt_value, ChatPromptValue):
        print(prompt_value)
        messages = [f"{msg.content}" for msg in prompt_value.messages]
        return "\n".join(messages)  
    
def gradio_predict(inputs):
    from gradio_client import Client

    client = Client("yuntian-deng/ChatGPT4Turbo")
    print(type(inputs))
    inputs = prepare_input(inputs)
    print("input\n",inputs)
    result = client.predict(
        inputs=inputs,
        top_p=1,
        temperature=0.5,
        chat_counter=0,
        chatbot=[],
        api_name="/predict"
    )
    print("output\n",result[0][0][-1])
    return result[0][0][-1]

gradio_runnable = RunnableLambda(lambda inputs: str(gradio_predict(inputs)))


QUERY_PROMPT_TAMIL = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language model assistant proficient in Tamil.
    The user has provided a specific textbook as the source of information.
    Your task is to generate five different versions of the given user question
    to help retrieve relevant sections or information from this textbook,
    while accounting for different ways the question might be asked.
    Ensure that each question maintains the core meaning but offers
    different perspectives or phrasings, helping overcome any limitations
    in retrieving relevant content from a vector database.
    if the given question is in English or other language
    Provide these alternative questions in Tamil with same context, separated by newlines.
    Original question: {question}""",
)

retriever_tamil = MultiQueryRetriever.from_llm(
    vectordb.as_retriever(),
    gradio_runnable,
    prompt=QUERY_PROMPT_TAMIL
)


def inspect(state):
    """Print the state passed between Runnables in a langchain and pass it on"""
    print("state :\n",state) # {'context': [Document(metadata={}, page_content='எபி. 6:..'),..}
    content = []
    for i in state['context']:
      content.append(i.page_content)
    state['context'] = "\n".join(content)
    print(state['context'])
    return state

def get_answer(question):
  template_tamil = """
  உங்களுக்கு கொடுக்கப்பட்டுள்ள உள்ளடக்கத்தை மட்டுமே பயன்படுத்தி கேள்விக்கு பதிலளியுங்கள். 
  கேள்வியை சரியாகப் புரிந்து கொண்டு, தமிழில் மட்டுமே பதில் அளிக்கவும். 
  ஆவணத்தில் தவறுகள் இருந்தால், சரியான தமிழ் பதிலை வழங்குங்கள்.

  தலைப்பு: """+title+"""

  {context}

  கேள்வி : {question}
  """ #பற்றி இந்த கதை என்ன கூறு கிறது
  prompt_tamil = ChatPromptTemplate.from_template(template_tamil)

  chain_tamil = (
      {'context': retriever_tamil, 'question': RunnablePassthrough()}
      | RunnableLambda(inspect)  # Assuming inspect is a defined function
      | prompt_tamil
      | gradio_runnable  # Use the Gradio model here
      | StrOutputParser()
  )
  return chain_tamil.invoke(question)


