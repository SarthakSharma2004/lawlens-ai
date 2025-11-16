
class RetrieverBuilder :
    """
    Creates a retriever from a vector store.
    This retriever will be used by the pipeline to fetch
    relevant document chunks for answering user queries.
    """
    @staticmethod

    def build_retriever(vectorstore , k : int = 3) :
        """
        Convert vectorstore into a retriever.
        """
        retriever = vectorstore.as_retriever(search_type = "similarity" , search_kwargs = {"k" : k})

        return retriever


         
