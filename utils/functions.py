import os
import chromadb
from chromadb.config import Settings
import uuid
from utils.instructor_embeddings import InstructorEmbeddings



def get_chroma_client():
    chroma_client = chromadb.Client(
        Settings(chroma_api_impl="rest",
                 chroma_server_host=os.environ.get('CHROMA_SERVER_HOST'),
                 chroma_server_http_port="8000"))
    return chroma_client

def convert_to_multiline_string(string_variable):
    multiline_string = f"""{string_variable}"""
    return multiline_string


def generate_unique_id():
    return str(uuid.uuid4())

def get_related_history(user_email, current_input):
    """
    Returns the related history of interactions between the given user and the chatbot
    """
    client = get_chroma_client()

    instructor_ef = InstructorEmbeddings().get_embedding_function()

    collection = client.get_or_create_collection(name="user_embeddings",
                                                 embedding_function=instructor_ef)

    res = collection.query(
        query_texts=[current_input],
        # n_results=int(os.environ.get('N_RELATED_INTERACTIONS', 5)), #TODO: update this back and uncomment
        n_results=3,
        where={"email": user_email})

    related_interactions = res['documents'][0]
    related_history ="\n".join(related_interactions)

    print(f'user input: {current_input}')
    print(f'related history of the client:\n{related_history}')

    return related_history

def return_last_n_interactions(user_email, n_interactions):
    client = get_chroma_client()

    collection = client.get_or_create_collection(name="user_embeddings")

    res = collection.get(where={'email': user_email}, include=["metadatas"])
    if len(res['metadatas']) == 0:
        return ''
    else:
        nbr_last_interaction = max([x['nbr_inter'] for x in res['metadatas']])
        last_interactions = collection.get(where={
        "$and": [{"email": {'$eq': user_email}},
                 {"nbr_inter": {'$gte': nbr_last_interaction - n_interactions + 1}}]})
        l = sorted(list(zip([x['nbr_inter'] for x in last_interactions['metadatas']],
                            last_interactions['documents'])))
        return '\n'.join([x[1] for x in l])

def write_current_interaction(user_email, current_interaction):
    client = get_chroma_client()
    instructor_ef = InstructorEmbeddings().get_embedding_function()

    collection = client.get_or_create_collection(name="user_embeddings",
                                                 embedding_function=instructor_ef)
    nbr_interaction = get_nbr_last_interaction(user_email) + 1

    collection.add(
        documents=[current_interaction],
        metadatas=[{'email': user_email, 'nbr_inter': nbr_interaction}],
        ids=generate_unique_id())

def get_nbr_last_interaction(user_email):
    client = get_chroma_client()
    collection = client.get_or_create_collection(name="user_embeddings")

    res = collection.get(where={'email': user_email}, include=["metadatas"])
    if len(res['metadatas']) == 0:
        return 0
    else:
        nbr_last_interaction = max([x['nbr_inter'] for x in res['metadatas']])
        return nbr_last_interaction


def delete_past_history(user_email):
    client = get_chroma_client()
    collection = client.get_or_create_collection(name="user_embeddings")

    collection.delete(where={'email': user_email})

