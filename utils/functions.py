import os
import chromadb
from chromadb.config import Settings
import uuid


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
