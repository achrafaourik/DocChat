from langchain.embeddings import HuggingFaceInstructEmbeddings


class InstructorEmbeddings:
    """Class with only class methods"""

    # Class variable for the model pipeline
    instructor_ef = None

    @classmethod
    def load(cls):
        # Only load one instance of the model
        if cls.instructor_ef is None:
            cls.instructor_ef = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl",
                                                      model_kwargs={"device": "cuda"})

    @classmethod
    def get_embedding_function(cls):
        # load the embedding model if not loaded yet
        cls.load()

        # get the embedding function
        return cls.instructor_ef
