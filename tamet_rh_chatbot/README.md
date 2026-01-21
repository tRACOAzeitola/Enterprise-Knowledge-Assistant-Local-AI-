# 🏢 Enterprise Knowledge Assistant (Local AI)

O **Enterprise Knowledge Assistant** é uma solução de Inteligência Artificial Generativa projetada para transformar a forma como as empresas acedem à sua informação interna.

Ao contrário de soluções na cloud (como ChatGPT ou Claude), este assistente corre **100% localmente** na infraestrutura da empresa, garantindo **privacidade total** e **zero fuga de dados**.

---

## 💡 Porquê adotar esta solução na sua empresa?

### 🔐 1. Privacidade e Segurança de Dados (Zero Trust)
A sua documentação confidencial (Políticas de RH, Segredos Industriais, Dados Financeiros) **nunca sai dos seus servidores**. O modelo de IA (LLaMA 3) corre inteiramente na sua máquina, eliminando riscos de compliance e GDPR associados a APIs externas.

### ⚡ 2. Eficiência Operacional
Reduza drasticamente o tempo que os colaboradores perdem à procura de informação. Em vez de abrir 10 PDFs diferentes para encontrar "como pedir férias" ou "especificações da peça X", o colaborador faz uma pergunta natural e recebe uma resposta imediata e citada.

### 💰 3. Redução de Custos
- **Zero custos por token**: Não paga APIs mensais (OpenAI/Azure).
- **Sem custos de internet**: Funciona offline.
- **Onboarding acelerado**: Novos colaboradores aprendem processos internos muito mais rápido conversando com a base de conhecimento.

### 🧠 4. Preservação do Conhecimento
Centraliza o conhecimento disperso da empresa (Manuais, PDFs, Procedimentos) numa interface única e acessível, evitando a perda de informação quando colaboradores saem.

---

## � Funcionalidades Técnicas

- **RAG (Retrieval-Augmented Generation)**: O modelo não "alucina" com base no vazio; ele responde estritamente com base nos documentos que a empresa fornecer.
- **Categorização Inteligente**: Suporta múltiplos departamentos (RH, Técnico, Financeiro, Manuais).
- **Citações Precisas**: Cada resposta indica exatamente qual o documento fonte, permitindo verificação humana imediata.
- **Modelo Open-Source**: Baseado no LLaMA 3 (Meta), um dos modelos abertos mais potentes do mundo.

---

## 🛠️ Pré-requisitos Técnicos

- **Sistema Operativo**: Windows, macOS ou Linux.
- **Hardware**: Recomendado 16GB RAM (mínimo 8GB). Não requer GPU dedicada (mas funciona mais rápido com uma).
- **Software**:
    - Python 3.10+
    - [Ollama](https://ollama.com) (Motor de inferência local)

---

## 📦 Instalação Rápida

1.  **Instale o Motor de IA (Ollama)**:
    Descarregue em [ollama.com](https://ollama.com) e instale.
    No terminal, descarregue o "cérebro" do assistente:
    ```bash
    ollama pull llama3:8b
    ```

2.  **Configure o Projeto**:
    ```bash
    # Criar ambiente virtual
    python -m venv venv
    
    # Ativar ambiente
    # Windows: venv\Scripts\activate
    # Mac/Linux: source venv/bin/activate
    
    # Instalar dependências
    pip install -r requirements.txt
    ```

3.  **Carregue o Conhecimento da Empresa**:
    Coloque os PDFs nas pastas dentro de `data/`:
    - `data/internas/`: Políticas Gerais, Regulamentos.
    - `data/pecas/`: Fichas Técnicas, Catálogos.
    - `data/manuais/`: Manuais de Procedimentos.
    - `data/outros/`: Outros documentos.

4.  **Inicie o Assistente**:
    ```bash
    python app.py
    ```
    Aceda via browser no link indicado (ex: `http://127.0.0.1:7860`).

---

## 📂 Estrutura de Pastas

```plaintext
projeto/
├── app.py                 # Cérebro da aplicação
├── data/                  # Repositório de documentos (Input)
├── db/                    # Memória Vetorial (Gerada automaticamente)
└── requirements.txt       # Lista de componentes necessários
```

---

*Enterprise Knowledge Solution - Potencialize o seu capital intelectual com segurança.*
