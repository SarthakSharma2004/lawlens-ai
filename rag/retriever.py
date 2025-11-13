class RetrieverBuilder :
    """
    Creates a retriever from a vector store.
    This retriever will be used by the QA pipeline to fetch
    relevant document chunks for answering user queries.
    """
    @staticmethod

    def build_retriever(vectorstore , k : int = 3) :
        """
        Convert vectorstore into a retriever.
        """
        retriver = vectorstore.as_retriever(search_type = "similarity" , k = k)

        return retriver


         
