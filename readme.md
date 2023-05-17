### VarWizard
***
1. Introduction

VarWizard is a language model-based tool to help generate more meaningful variable names in source code than the original version. It supports 10 programming languages: c, cpp, java, javascript, go, python, php, c\_sharp, ruby, rust.

2. Installation

You can easily install this package by the command
```
    pip install varwizard
```
3. Usage
    * Command-line
    
    You can use VarWizard by running the command
```
varwizard [--model-name {bloom-560m}]
            --input INPUT --lang {c,cpp,java,php,go,javascript,ruby,rust,python,c_sharp} 
            [--output-path OUTPUT_PATH] [--max-input-len MAX_INPUT_LEN]
            [--device DEVICE] [--penalty-alpha PENALTY_ALPHA] [--top-k TOP_K] [--max-new-tokens MAX_NEW_TOKENS]
```
Details for each argument can be found by 
```varwizard --help```


 * Python API
Another way is to Python methods.
Here is a simple example of VarWizard.
```
from varwizard import VarWizard

model = VarWizard()
code = """
static void lsp2poly ( int * var0, const int16_t * var1, int var2 ) { int var3, var4 ; var0 [ 0 ] = 0x400000 ; // 1.0 in (3.22) var0 [ 1 ] = - var1 [ 0 ] << 8 ; // *2 and (0.15) -> (3.22) for ( var3 = 2 ; var3 <= var2 ; var3 ++ ) { var0 [ var3 ] = var0 [ var3 - 2 ] ; for ( var4 = var3 ; var4 > 1 ; var4 -- ) var0 [ var4 ] -= MULL ( var0 [ var4 - 1 ], var1 [ 2 * var3 - 2 ], FRAC_BITS ) - var0 [ var4 - 2 ] ; var0 [ 1 ] -= var1 [ 2 * var3 - 2 ] << 8 ; } }"""
print(model.make_new_code(code, 'cpp', device = 'cuda:0'))
```
VarWizard produces the output
```
static void lsp2poly ( int * lsp, const int16_t * lsp2, int nbits ) { int index, count ; lsp [ 0 ] = 0x400000 ; // 1.0 in (3.22) lsp [ 1 ] = - lsp2 [ 0 ] << 8 ; // *2 and (0.15) -> (3.22) for ( index = 2 ; index <= nbits ; index ++ ) { lsp [ index ] = lsp [ index - 2 ] ; for ( count = index ; count > 1 ; count -- ) lsp [ count ] -= MULL ( lsp [ count - 1 ], lsp2 [ 2 * index - 2 ], FRAC_BITS ) - lsp [ count - 2 ] ; lsp [ 1 ] -= lsp2 [ 2 * index - 2 ] << 8 ; } }
```