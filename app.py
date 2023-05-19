import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.chains.conversation.memory import (ConversationBufferWindowMemory,)

# new code
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator


# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

#Langchain implementation
template = """
    Human: {human_input}
    Assistant:"""

prompt = PromptTemplate(
    input_variables=["human_input"], 
    template=template
)

# new code
root_dir = "./"

pdf_folder_path = f'{root_dir}/pdfs/'
os.listdir(pdf_folder_path)

# location of the pdf file/files. 
loaders = [UnstructuredPDFLoader(os.path.join(pdf_folder_path, fn)) for fn in os.listdir(pdf_folder_path)]
CHESSGPT = VectorstoreIndexCreator().from_loaders(loaders)

"""
chatgpt_chain = LLMChain(
    llm=OpenAI(temperature=0), 
    prompt=prompt, 
    verbose=True,
    memory=ConversationBufferWindowMemory(k=1),
)
"""

#Message handler for Slack
@app.message(".*")
def message_handler(message, say, logger):
    print(message)
    
    output = CHESSGPT.query(message)
    say(output)
    

# Start 
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
