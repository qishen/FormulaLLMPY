from typing import List
import os, glob

from langchain_community.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    PyMuPDFLoader,
    TextLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from multiprocessing import Pool
from tqdm import tqdm
import base64
from io import BytesIO
from IPython.display import HTML, display

LOADER_MAPPING = {
    ".csv": (CSVLoader, dict()),
    ".doc": (UnstructuredWordDocumentLoader, dict()),
    ".docx": (UnstructuredWordDocumentLoader, dict()),
    ".enex": (EverNoteLoader, dict()),
    ".epub": (UnstructuredEPubLoader, dict()),
    ".html": (UnstructuredHTMLLoader, dict()),
    ".md": (UnstructuredMarkdownLoader, dict()),
    ".odt": (UnstructuredODTLoader, dict()),
    ".pdf": (PyMuPDFLoader, dict()),
    ".PDF": (PyMuPDFLoader, dict()),
    ".ppt": (UnstructuredPowerPointLoader, dict()),
    ".pptx": (UnstructuredPowerPointLoader, dict()),
    ".txt": (TextLoader, dict({"encoding": "utf8"}))
}

def load_single_document(file_path: str) -> List[Document]:
    ext = "." + file_path.rsplit(".", 1)[-1]
    if ext in LOADER_MAPPING:
        loader_class, loader_args = LOADER_MAPPING[ext]
        loader = loader_class(file_path, **loader_args)
        return loader.load()

    raise ValueError(f"Unsupported file extension '{ext}'")

def plt_img_base64(img_base64):
    """
    Display base64 encoded string as image

    :param img_base64:  Base64 string
    """
    # Create an HTML img tag with the base64 string as the source
    image_html = f'<img src="data:image/jpeg;base64,{img_base64}" width="320" height="240"/>'
    # Display the image by rendering the HTML
    display(HTML(image_html))

def convert_to_base64(pil_image, type):
    """
    Convert PIL images to Base64 encoded strings

    :param pil_image: PIL image
    :return: Re-sized Base64 string
    """

    buffered = BytesIO()
    pil_image.save(buffered, format=type) 
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def process_document(file: str, chunk_size = 512, chunk_overlap = 0) -> List[Document]:
    """
    Load documents and split in chunks
    """
    documents = load_doc(file)
    if not documents:
        print("No new documents to load")
        exit(0)
    print(f"Loaded {len(documents)} new documents")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks of text (max. {chunk_size} tokens each)")
    return texts

def load_doc(file: str) -> List[Document]:
    all_files = [file]

    with Pool(processes=os.cpu_count()) as pool:
        results = []
        with tqdm(total=len(all_files), desc='Loading new documents', ncols=80) as pbar:
            for i, docs in enumerate(pool.imap_unordered(load_single_document, all_files)):
                results.extend(docs)
                pbar.update()

    return results

def process_documents(files: str, chunk_size = 512, chunk_overlap = 0) -> List[Document]:
    """
    Load documents and split in chunks
    """
    documents = load_docs(files)
    if not documents:
        print("No new documents to load")
        exit(0)
    print(f"Loaded {len(documents)} new documents")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks of text (max. {chunk_size} tokens each)")
    return texts

def load_docs(files: str) -> List[Document]:
    all_files = glob.glob(os.path.join(files, "*"))

    with Pool(processes=os.cpu_count()) as pool:
        results = []
        with tqdm(total=len(all_files), desc='Loading new documents', ncols=80) as pbar:
            for i, docs in enumerate(pool.imap_unordered(load_single_document, all_files)):
                results.extend(docs)
                pbar.update()

    return results