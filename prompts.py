from langchain.prompts import ChatPromptTemplate


map_prompt = ChatPromptTemplate(
    ('system' , 'You are highly skilled virtual legal assistant specializing in summarizing legal contracts'
    'and agreements')
)







# map_prompt = PromptTemplate(
#     input_variables=["text"],   # for each chunk
#     template="Summarize the following text clearly and concisely:\n\n{text}"
# )

# reduce_prompt = PromptTemplate(
#     input_variables=["summaries"],   # for combining summaries
#     template="Combine the following partial summaries into a single, well-structured summary:\n\n{summaries}"
# )