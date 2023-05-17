from tree_sitter import Parser, Language
from pkg_resources import resource_filename
import varwizard

from varwizard.utils.obfuscation import *

from codetext.parser import GoParser, PhpParser, RubyParser, JavaParser, JavascriptParser, PythonParser, CppParser, CsharpParser, RustParser

def beautify(function_root, function_bytes, vmap, new_function_bytes = None, offset = 0):
    if len(function_root.children) == 0:
        node_token = function_bytes[function_root.start_byte: function_root.end_byte].decode()
        if function_root.type == 'identifier': 
            if node_token in vmap:
                if new_function_bytes is None:
                    new_function_bytes = function_bytes
                new_function_bytes = new_function_bytes[:function_root.start_byte + offset] + vmap[node_token].encode() + new_function_bytes[function_root.end_byte + offset:]
                offset += len(vmap[node_token].encode()) - function_root.end_byte + function_root.start_byte
                return new_function_bytes, offset
    for child in function_root.children:
        new_function_bytes, offset = beautify(child, function_bytes, vmap, new_function_bytes, offset)
    return new_function_bytes, offset
def prepare_input(input, lang, tokenizer, max_input_len: int = 400, prompt = ' Output var0 ='):
    parser = Parser()
    so_path = resource_filename('varwizard', f'libs/tree-sitter/{lang}.so')
    parser.set_language(Language(so_path, lang))
    
    bytes = input.encode()
    root = parser.parse(bytes).root_node
    code_parser = lang.replace('_', '')
    code_parser = code_parser[0].upper() + code_parser[1:] + "Parser"
    code_parser = eval(code_parser)
    function_lst = code_parser.get_function_list(root)
    for function_node in function_lst:
        function_bytes = bytes[function_node.start_byte: function_node.end_byte]
        new_function_bytes = function_bytes[:]
        function_root = parser.parse(function_bytes).root_node
        idens = {'var_num': 0, 'vars': {}}
        idens = eval(f'get_{lang}_var_names')(function_root, function_bytes, idens)
        chosen_vars = [x for x in idens['vars'] if x != x.upper()]
        chosen_ids = list(map(idens['vars'].get, chosen_vars))
        chosen_tup = sorted(list(zip(chosen_vars, chosen_ids)), key = lambda x: x[1])
        vmap = {}
        for i, var_name in enumerate(chosen_tup):
            vmap[var_name[0]] = f'var{i}'
        new_function_bytes, _ = beautify(function_root, function_bytes, vmap)
        function_code = new_function_bytes.decode()
        source_tokens = tokenizer.tokenize(function_code, truncation = True, max_length = max_input_len)
        prompt_tokens = tokenizer.tokenize(prompt)
        input_tokens = source_tokens + prompt_tokens
        input_ids = [tokenizer.bos_token_id] + tokenizer.convert_tokens_to_ids(input_tokens)
        yield input_ids, {v: k for k, v in vmap.items()}