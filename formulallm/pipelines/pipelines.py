from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

from .loader import process_document, process_documents, convert_to_base64, plt_img_base64

from PIL import Image

from typing import List
from abc import ABC, abstractmethod

class QAPipeline(ABC):
    def __init__(self, llm="mistral", img_caption="bakllava", llm_temp=0.0, multi_modal_temp=0.0, oembed_temp=0.0):
        self.llm = Ollama(base_url='http://localhost:11434', model=llm, temperature=llm_temp)
        self.multi_modal = Ollama(base_url='http://localhost:11434', model=img_caption, temperature=multi_modal_temp)
        self.oembed = OllamaEmbeddings(base_url="http://localhost:11434", model=llm, temperature=oembed_temp)
        self.vectorstore = None
        self.qachain = None

    @abstractmethod
    def run(self, question: str):
        raise NotImplementedError
    
    def prompt(self, prompt: str):
        return self.llm.predict(prompt)
    
    def run_multi_modal(self, images: List[str], prompt: str, display_img = False):
        images_b64 = []
        for img in images:
            pil_image = Image.open(img)
            image_b64 = convert_to_base64(pil_image)
            images_b64.append(image_b64)
            if display_img:
                plt_img_base64(image_b64)
        llm_with_image_context = self.multi_modal.bind(images=images_b64)
        return llm_with_image_context.invoke(prompt)

class OllamaQAPipeline(QAPipeline): 
    def load_document(self, file: str, chunk_size = 512, chunk_overlap = 0):
        self.vectorstore = Chroma.from_documents(documents=process_document(file, chunk_size, chunk_overlap), embedding=self.oembed)
        self.qachain = RetrievalQA.from_chain_type(self.llm, retriever=self.vectorstore.as_retriever())
    
    def run(self, question: str):
        return self.qachain({"query": question})['result']

class OllamaMultiQAPipeline(QAPipeline):
    def load_documents(self, source_path: str, chunk_size = 512, chunk_overlap = 0):
        self.vectorstore = Chroma.from_documents(documents=process_documents(source_path, chunk_size, chunk_overlap), embedding=self.oembed)
        self.qachain = RetrievalQA.from_chain_type(self.llm, retriever=self.vectorstore.as_retriever())
    
    def extract_image_data(self, image: str):
        prompt = "what is in this image?"
        results = []
        for _ in range(10):
            res = self.run_multi_modal([image], prompt)
            results.append(res)

        for res in results:
            docs = self.vectorstore.similarity_search(res)
            for doc in docs:
                print(doc.metadata["source"])
                print(doc.page_content)
                print()

    def run(self, question: str):
        return self.qachain({"query": question})['result']