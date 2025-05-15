# core/java_parser.py

import javalang

def extract_methods_from_code(code: str) -> list:
    """
    Returns a list of method declarations from the given Java source code.
    """
    try:
        tree = javalang.parse.parse(code)
        return [node for path, node in tree.filter(javalang.tree.MethodDeclaration)]
    except Exception:
        return []

def extract_classes_and_interfaces(code: str) -> list:
    """
    Returns a list of classes and interfaces in the Java code.
    """
    try:
        tree = javalang.parse.parse(code)
        declarations = []
        for path, node in tree.filter(javalang.tree.TypeDeclaration):
            declarations.append({
                "name": node.name,
                "type": "class" if isinstance(node, javalang.tree.ClassDeclaration) else "interface"
            })
        return declarations
    except Exception:
        return []
