import os
import numpy as np
import fitz  # PyMuPDF
from PIL import Image as PILImage
import gradio as gr
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import PromptTemplate
try:
    from langchain.chains import RetrievalQA
except ImportError:
    from langchain_classic.chains import RetrievalQA

# Configuração do Modelo e Embeddings
LLM_MODEL_NAME = "llama3:8b"

print(f"⏳ Inicializando modelo {LLM_MODEL_NAME}...")
llm = ChatOllama(
    model=LLM_MODEL_NAME,
    temperature=0.2
)

embeddings = OllamaEmbeddings(
    model=LLM_MODEL_NAME
)
print("✅ LLM e embeddings locais configurados.")

# Configuração de Caminhos
BASE_DIR = "data"
DB_DIR = "db"

CATEGORIES = {
    "Informações Internas": "internas",
    "Peças / Material": "pecas",
    "Manuais": "manuais",
    "Outros": "outros"
}

# Criar pastas se não existirem
os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)

# Funções de Backend
def create_vector_db_for_category(category_name):
    folder_key = CATEGORIES[category_name]
    pdf_folder = os.path.join(BASE_DIR, folder_key)
    db_folder = os.path.join(DB_DIR, folder_key)

    os.makedirs(db_folder, exist_ok=True)

    if not os.path.isdir(pdf_folder):
        print(f"⚠️ Pasta não encontrada para categoria '{category_name}': {pdf_folder}")
        return

    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print(f"⚠️ Nenhum PDF encontrado em {pdf_folder}")
        return

    print(f"📚 Processando {len(pdf_files)} PDFs na categoria '{category_name}'...")
    all_docs = []

    for pdf in pdf_files:
        path = os.path.join(pdf_folder, pdf)
        loader = PyPDFLoader(path)
        docs = loader.load()

        for d in docs:
            d.metadata["source"] = pdf
            d.metadata["category"] = category_name

        all_docs.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", "!", "?", ","]
    )

    chunks = splitter.split_documents(all_docs)

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_folder
    )
    
    # Em versões mais recentes do Chroma a persistência é automática, mas mal não faz
    try:
        vector_store.persist() 
    except:
        pass
        
    print(f"✅ Base vetorial criada para categoria: {category_name} ({len(chunks)} chunks)")

def load_vector_store(category_name):
    folder_key = CATEGORIES[category_name]
    db_folder = os.path.join(DB_DIR, folder_key)

    if not os.path.isdir(db_folder):
        # Tenta criar se não existir (caso o user tenha posto PDFs mas não tenha corrido a indexação ainda)
        create_vector_db_for_category(category_name)
        if not os.path.isdir(db_folder):
             raise ValueError(f"Base vetorial não encontrada para categoria '{category_name}' em {db_folder}")

    vs = Chroma(
        embedding_function=embeddings,
        persist_directory=db_folder
    )
    return vs

REJECTION_PHRASE = "Não encontro essa informação nos documentos disponíveis"

prompt_template = """
És um assistente inteligente especializado em gestão de conhecimento empresarial.

Regras:
- Responde APENAS com base na informação dos documentos fornecidos.
- Se a resposta não estiver clara nos documentos, responde exatamente: "{rejection_phrase}".
- Usa linguagem profissional, corporativa e direta.
- Sempre que fizer sentido, organiza a resposta em pontos ou parágrafos curtos.

Categoria selecionada: {category}

Contexto (excerto dos documentos internos):
{context}

Pergunta do utilizador:
{question}

Resposta:
"""

qa_prompt = PromptTemplate(
    input_variables=["context", "question", "category", "rejection_phrase"],
    template=prompt_template
)

def create_rag_chain_for_category(category_name):
    vector_store = load_vector_store(category_name)

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 5}
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": qa_prompt.partial(
                category=category_name,
                rejection_phrase=REJECTION_PHRASE
            )
        }
    )
    return chain

def answer_question(category_name, user_question):
    if not user_question:
        return "Por favor, insira uma pergunta."

    try:
        qa_chain = create_rag_chain_for_category(category_name)
    except Exception as e:
        return f"Erro ao preparar o motor de pesquisa para a categoria '{category_name}': {e}"

    try:
        result = qa_chain.invoke({"query": user_question})
        answer_text = result["result"]
        source_docs = result.get("source_documents", [])

        # Acrescentar fontes no fim da resposta
        if source_docs:
            answer_text += "\n\nFontes consultadas:"
            unique_sources = set()
            for doc in source_docs:
                src = doc.metadata.get("source", "desconhecido")
                unique_sources.add(src)
            for src in unique_sources:
                answer_text += f"\n- {src}"

        return answer_text

    except Exception as e:
        return f"Ocorreu um erro ao consultar o modelo local: {e}"

# Interface Gradio
def gradio_answer(category, question):
    return answer_question(category, question)

if __name__ == "__main__":
    # check for pdfs and create dbs on startup if needed
    print("🔄 Verificando documentos e criando bases vetoriais...")
    for cat in CATEGORIES.keys():
        create_vector_db_for_category(cat)
    print("✅ Verificação concluída.")

    with gr.Blocks(title="🤖 Enterprise Knowledge Assistant") as demo:
        gr.Markdown("""
        # 🤖 Enterprise Knowledge Assistant (Local Secure AI)
        Assistente inteligente para consulta de documentação interna.
        Segurança total: todas as respostas são geradas localmente (LLaMA 3) sem envio de dados para a cloud.
        """)

        with gr.Row():
            category_input = gr.Dropdown(
                choices=list(CATEGORIES.keys()),
                value="Informações Internas",
                label="Categoria de documentos"
            )
            question_input = gr.Textbox(
                lines=4,
                label="Pergunta",
                placeholder="Ex.: Qual é a política de férias? / Como é o procedimento de segurança X?"
            )

        submit_btn = gr.Button("Obter resposta", variant="primary")

        answer_output = gr.Textbox(
            lines=12,
            label="Resposta do assistente"
        )

        submit_btn.click(
            fn=gradio_answer,
            inputs=[category_input, question_input],
            outputs=[answer_output]
        )

    print("🚀 A iniciar interface Gradio...")
    demo.launch(inbrowser=True)
