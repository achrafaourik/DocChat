from langchain.document_loaders import WebBaseLoader, DirectoryLoader, TextLoader, PyPDFLoader


def read_urls_from_file(file_path):
    url_list = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.isspace():
                url_list.append(line)

    return url_list

def get_all_loaders():
    # loading from urls
    loader_urls = WebBaseLoader(read_urls_from_file('data/urls.txt'))

    # loading from text files
    text_loader_kwargs={'autodetect_encoding': True}
    loader_directory = DirectoryLoader('data/text_files',
                                       glob="*.txt",
                                       loader_cls=TextLoader,
                                       loader_kwargs=text_loader_kwargs,
                                       use_multithreading=True)

    # loading from pdf files
    loader_pdfs = DirectoryLoader('data/pdf_files',
                                  glob="*.pdf",
                                  loader_cls=PyPDFLoader)

    return [loader_pdfs, loader_directory, loader_urls]
