from tree_sitter import Parser, Language
from pkg_resources import resource_filename
import varwizard

from varwizard.utils.obfuscation import *
def prepare_input(input, lang, tokenizer, max_input_len: int = 400, prompt = ' Output'):
    parser = Parser()
    so_path = resource_filename('varwizard', f'libs/tree-sitter/{lang}.so')
    parser.set_language(Language(so_path, lang))
    
    bytes = input.encode()
    root = parser.parse(bytes).root_node
    idens = {'var_num': 0, 'vars': {}}
    idens = eval(f'get_{lang}_var_names')(root, bytes, idens)
    chosen_vars = [x for x in idens['vars'] if x != x.upper()]
    chosen_ids = list(map(idens['vars'].get, chosen_vars))
    chosen_tup = sorted(list(zip(chosen_vars, chosen_ids)), key = lambda x: x[1])
    for i, var_name in enumerate(chosen_tup):
        
        input = input.replace(' '+ var_name[0] + ' ', f' var{i} ')
    source_tokens = tokenizer.tokenize(input, truncation = True, max_length = max_input_len)
    prompt_tokens = tokenizer.tokenize(prompt)
    input_tokens = source_tokens + prompt_tokens
    input_ids = [tokenizer.bos_token_id] + tokenizer.convert_tokens_to_ids(input_tokens)
    return input_ids