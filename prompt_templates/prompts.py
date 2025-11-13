from langchain.prompts import ChatPromptTemplate
class PromptManager :
    '''
    This class contains all the prompts and chains used for summarization.
    ''' 

    @staticmethod
    def get_map_prompt() -> ChatPromptTemplate :
        '''
        Prompt for summarizing individual document chunks (MAP phase).
        This runs on each chunk separately.
        '''

        system_template = "You are a skilled legal document summarizer that creates clear and consise summaries of legal text chunks"

        user_template = "Summarize the following text chunk by extracting the main points and key information clearly. \n\n{text}"

        prompt = ChatPromptTemplate.from_messages([
            ("system" , system_template),
            ("user" , user_template)
        ])

        return prompt   
    
    
    @staticmethod
    def get_reduce_prompt() -> ChatPromptTemplate :
        """
        Prompt for combining all chunk summaries (REDUCE phase).
        This creates the final comprehensive summary.
        """

        # system_template = "You are a legal document summarizer skilled at creating clear and consise summaries from legal text chunks"
        system_template = "You are a legal document summarizer skilled at combining multiple partial summaries from legal text chunks into a single final summary"

        user_template = """Combine the following partial summaries into a single, cohesive well-structured summary
        Requirements:
        1. Create a clear and descriptive title
        2. Organize information logically
        3. Cover all main themes and key points
        4. Make it coherent and easy to read \n {text}"""
        

        prompt = ChatPromptTemplate.from_messages([
            ("system" , system_template),
            ("user" , user_template)
        ])

        return prompt
    
    
    @staticmethod
    def get_stuff_prompt() -> ChatPromptTemplate :
        """
        Prompt template for the 'stuff' summarization chain.
        Used for short legal documents that can be summarized directly.
        """



        system_template = """You are a professional legal assistant skilled at summarising legal documents.
        Your task is to read the provided legal document and genrate a clear, concise and well structured summary in {language}
        """

        user_template = "Provide a summary of the following legal document: \n\n {text}"

        prompt = ChatPromptTemplate.from_messages([
            ("system" , system_template),
            ("user" , user_template)
        ])

        return prompt

    @staticmethod
    def get_rag_prompt() -> ChatPromptTemplate :
        """
        Prompt template for the RAG chain
        """

        system_template = """You are a legal document assistant. 
        Use the provided retrieved document context from a legal document to answer the user's question. 
        If the answer is not in the context, say 'I cannot find the information in the document'.
        Do NOT hallucinate."""

        user_template = "\n\n Context : {context}. \n\n Question : {input}. Provide a clear factual based answer based on the context provided in {language}."

        prompt = ChatPromptTemplate.from_messages([
            ("system" , system_template),
            ("user" , user_template)
        ])

        return prompt