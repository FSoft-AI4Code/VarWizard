
def get_java_var_names(root, bytes, idens = {'var_num': 0, 'vars': {}}, KEYWORDS = {
    'String',
    'System',
    'Logger',
    'Float',
    'Integer',
    'Double',
    'A'
}):
    children = root.children
    if root.type == 'method_declaration':
        _children = []
        for child in children:
            if child.type == 'identifier':
                node_token = bytes[child.start_byte:child.end_byte].decode()
                idens['func'] = node_token
            else:
                _children.append(child)
        children = _children
    elif root.type == 'annotation': children = []
    elif root.type == 'method_invocation':
        _children = []
        i = 0
        flag = False
        while i < len(children):
            if i == 0:
                node = children[i]
                if node.type == 'identifier':
                    node_token = bytes[node.start_byte:node.end_byte].decode()
                    if node_token[0].isupper():
                        i += 1
                        continue
            _children.append(children[i])
            if children[i].type == '.':
                i += 1
                flag = True
            i += 1
        if not flag:
            _children.pop(0)
        children = _children
    elif root.type == 'field_access':
        children = children[0:1]
        node = children[0]
        node_token = bytes[node.start_byte:node.end_byte].decode()
        if node_token[0].isupper():
            children = []
    elif root.type == 'identifier':
        node_token = bytes[root.start_byte:root.end_byte].decode()
        if node_token not in KEYWORDS and node_token not in idens['vars']:
            idens['vars'][node_token] = idens['var_num']
            idens['var_num'] += 1
        return idens
    for child in children:
        get_java_var_names(child, bytes, idens)
    return idens

def get_c_sharp_var_names(root, bytes, idens = {'var_num': 0, 'vars': {}}):
    children = root.children
    # print('type', root.type)
    if root.type == 'local_function_statement':
        _children = []
        for child in children:
            if child.type == 'identifier':
                node_token = bytes[child.start_byte:child.end_byte].decode()
                idens['func'] = node_token
            else:
                _children.append(child)
        children = _children
    elif root.type == 'invocation_expression':
        if children[0].type == 'identifier':
            children.pop(0)
    elif root.type == 'member_access_expression':
        children = children[0:1]
    elif root.type == 'identifier':
        node_token = bytes[root.start_byte:root.end_byte].decode()
        if node_token and not node_token[0].isupper() and node_token not in idens['vars']:
            idens['vars'][node_token] = idens['var_num']
            idens['var_num'] += 1
        return idens
    for child in children:
        get_c_sharp_var_names(child, bytes, idens)
    return idens
def get_cpp_var_names(root, bytes, idens = {'var_num': 0, 'vars': {}}):
    children = root.children
    if root.type == 'function_declarator':
        _children = []
        for child in children:
            if child.type == 'identifier':
                node_token = bytes[child.start_byte:child.end_byte].decode()
                idens['func'] = node_token
            else:
                _children.append(child)
        children = _children
    elif root.type == 'qualified_identifier':
        children = []
    elif root.type == 'call_expression':
        _children = []
        i = 0
        flag = False
        while i < len(children):
            if i == 0:
                node = children[i]
                if node.type == 'identifier':
                    node_token = bytes[node.start_byte:node.end_byte].decode()
                    if node_token[i].isupper():
                        i += 1
                        continue
            _children.append(children[i])
            if i == 1 and children[i].type == '.':
                i += 1
                flag = True
            i += 1
        if not flag:
            _children.pop(0)
        children = _children
    # elif root.type == 'field_expression':
    #     children = children[0:]
    elif root.type == 'identifier':
        node_token = bytes[root.start_byte:root.end_byte].decode()
        if node_token not in idens['vars']:
            idens['vars'][node_token] = idens['var_num']
            idens['var_num'] += 1
        return idens
    for child in children:
        get_cpp_var_names(child, bytes, idens)
    return idens

def get_c_var_names(root, bytes, idens = {'var_num': 0, 'vars': {}}):
    children = root.children
    if root.type == 'function_declarator':
        _children = []
        for child in children:
            if child.type == 'identifier':
                node_token = bytes[child.start_byte:child.end_byte].decode()
                idens['func'] = node_token
            else:
                _children.append(child)
        children = _children
    elif root.type == 'call_expression':
        _children = []
        i = 0
        flag = False
        while i < len(children):
            if i == 0:
                node = children[i]
                if node.type == 'identifier':
                    node_token = bytes[node.start_byte:node.end_byte].decode()
                    if node_token[i].isupper():
                        i += 1
                        continue
            _children.append(children[i])
            if i == 1 and children[i].type == '.':
                i += 1
                flag = True
            i += 1
        if not flag:
            _children.pop(0)
        children = _children
    # elif root.type == 'field_expression':
    #     children = children[0:]
    elif root.type == 'identifier':
        node_token = bytes[root.start_byte:root.end_byte].decode()
        if node_token not in idens['vars']:
            idens['vars'][node_token] = idens['var_num']
            idens['var_num'] += 1
        return idens
    for child in children:
        get_c_var_names(child, bytes, idens)
    return idens
def get_php_var_names(root, bytes, idens = {'var_num': 0, 'vars': {}}, KEYWORDS = ['A', '__CLASS__', '__METHOD__', '__FUNCTION__', 'GLOBAL']):
    children = root.children
    if root.type == 'method_declaration':
        _children = []
        for child in children:
            if child.type == 'name':
                node_token = bytes[child.start_byte:child.end_byte].decode()
                idens['func'] = node_token
            else:
                _children.append(child)
        children = _children
    elif root.type == 'function_call_expression':
        children.pop(0)
    elif root.type == 'scoped_property_access_expression':
        children = []
    elif root.type == 'member_call_expression':
        children.pop(2)
    elif root.type == 'class_constant_access_expression':
        children = []
    elif root.type == 'scoped_call_expression':
        # children.pop(2)
        while children[0].type != 'arguments':
            children.pop(0)
    elif root.type == 'member_access_expression':
        children = children[:1]
    elif root.type == 'name':
        node_token = bytes[root.start_byte:root.end_byte].decode()
        if node_token not in KEYWORDS and node_token not in idens['vars']:
            idens['vars'][node_token] = idens['var_num']
            idens['var_num'] += 1
        return idens
    for child in children:
        get_php_var_names(child, bytes, idens)
    return idens
def get_go_var_names(root, bytes, idens = {'var_num': 0, 'vars': {}}, KEYWORDS = ['float64', 'math', '_']):
    children = root.children
    if root.type == 'function_declaration':
        _children = []
        for child in children:
            if child.type == 'identifier':
                node_token = bytes[child.start_byte:child.end_byte].decode()
                idens['func'] = node_token
            else:
                _children.append(child)
        children = _children
    elif root.type == 'identifier':
        node_token = bytes[root.start_byte:root.end_byte].decode()
        if node_token not in KEYWORDS and node_token not in idens['vars']:
            idens['vars'][node_token] = idens['var_num']
            idens['var_num'] += 1
        return idens
    for child in children:
        get_go_var_names(child, bytes, idens)
    return idens
def get_ruby_var_names(root, bytes, idens = {'var_num': 0, 'vars': {}}, KEYWORDS = ['float64', 'math', '_']):
    children = root.children
    if root.type == 'method':
        _children = []
        for child in children:
            if child.type == 'identifier':
                node_token = bytes[child.start_byte:child.end_byte].decode()
                idens['func'] = node_token
            else:
                _children.append(child)
        children = _children
    elif root.type == 'call':
        flag = False
        for i in range(len(children)):
            child = children[i]
            child_token = bytes[child.start_byte:child.end_byte].decode()
            if child_token == '.':
                children.pop(2)
                flag = True
                break
        if not flag:
            children.pop(0)
    elif root.type == 'identifier':
        node_token = bytes[root.start_byte:root.end_byte].decode()
        if node_token not in KEYWORDS and node_token not in idens['vars']:
            idens['vars'][node_token] = idens['var_num']
            idens['var_num'] += 1
        return idens
    for child in children:
        get_ruby_var_names(child, bytes, idens)
    return idens
def get_rust_var_names(root, bytes, idens = {'var_num': 0, 'vars': {}}, KEYWORDS = set(['let', 'u8', 'u16', 'u32', 'u64', 'u128', 'usize', 'i8', 'i16', 'i32', 'i64', 'i128', 'isize'])):
    children = root.children
    if root.type == 'function_item':
        _children = []
        for child in children:
            if child.type == 'identifier':
                node_token = bytes[child.start_byte:child.end_byte].decode()
                idens['func'] = node_token
            else:
                _children.append(child)
        children = _children
    elif root.type == 'scoped_identifier':
        # children.pop(0)
        children = []
    elif root.type == 'call_expression':
        if children[0].type in ['identifier', 'scoped_identifier']:
            children.pop(0)
    elif root.type == 'macro_invocation':
        children.pop(0)
    elif root.type == 'identifier':
        node_token = bytes[root.start_byte:root.end_byte].decode()
        if node_token not in KEYWORDS and node_token not in idens['vars']:
            idens['vars'][node_token] = idens['var_num']
            idens['var_num'] += 1
        return idens
    for child in children:
        get_rust_var_names(child, bytes, idens)
    return idens
def get_javascript_var_names(root, bytes, idens = {'var_num': 0, 'vars': {}}):
    children = root.children
    if root.type == 'function_declaration':
        _children = []
        for child in children:
            if child.type == 'identifier':
                node_token = bytes[child.start_byte:child.end_byte].decode()
                idens['func'] = node_token
            else:
                _children.append(child)
        children = _children
    elif root.type == 'call_expression':
        _children = []
        i = 0
        flag = False
        while i < len(children):
            if i == 0:
                node = children[i]
                if node.type == 'identifier':
                    node_token = bytes[node.start_byte:node.end_byte].decode()
                    if node_token[i].isupper():
                        i += 1
                        continue
            _children.append(children[i])
            if i == 1 and children[i].type == '.':
                i += 1
                flag = True
            i += 1
        if not flag:
            _children.pop(0)
        children = _children
    # elif root.type == 'field_expression':
    #     children = children[0:]
    elif root.type == 'identifier':
        node_token = bytes[root.start_byte:root.end_byte].decode()
        if node_token not in idens['vars']:
            idens['vars'][node_token] = idens['var_num']
            idens['var_num'] += 1
        return idens
    for child in children:
        get_javascript_var_names(child, bytes, idens)
    return idens

def get_python_var_names(root, bytes, idens = {'var_num': 0, 'vars': {}}, KEYWORDS = ['self', 'int', '_', 'float', 'int']):
    children = root.children
    if root.type == 'function_definition':
        _children = []
        for child in children:
            if child.type == 'identifier':
                node_token = bytes[child.start_byte:child.end_byte].decode()
                idens['func'] = node_token
            else:
                _children.append(child)
        children = _children
    elif root.type == 'attribute':
        children = children[:1]
    elif root.type == 'call':
        if children[0].type == 'identifier':
            children.pop(0)
    # elif root.type == 'field_expression':
    #     children = children[0:]
    elif root.type == 'identifier':
        node_token = bytes[root.start_byte:root.end_byte].decode()
        if node_token not in KEYWORDS and node_token not in idens['vars']:
            idens['vars'][node_token] = idens['var_num']
            idens['var_num'] += 1
        return idens
    for child in children:
        get_python_var_names(child, bytes, idens)
    return idens
