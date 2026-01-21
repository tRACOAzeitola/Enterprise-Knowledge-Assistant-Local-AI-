
import pkgutil
import langchain

def find_submodules(package):
    if hasattr(package, "__path__"):
        for _, name, _ in pkgutil.iter_modules(package.__path__):
            print(f"{package.__name__}.{name}")

print("Submodules of langchain:")
find_submodules(langchain)
