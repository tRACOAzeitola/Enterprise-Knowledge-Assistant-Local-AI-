
try:
    from langchain_classic.chains import RetrievalQA
    print("Import successful from langchain_classic.chains")
except ImportError as e:
    print(f"Import failed: {e}")

try:
    from langchain.chains import RetrievalQA
    print("Import successful from langchain.chains")
except ImportError as e:
    print(f"Import from langchain.chains failed: {e}")
