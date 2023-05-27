### VarWizard
***
1. Introduction

VarWizard is a language model-based tool to help generate more meaningful variable names in source code than the original version. It supports 10 programming languages: c, cpp, java, javascript, go, python, php, c\_sharp, ruby, rust.

2. Installation

You can easily install this package by the command
```bash
    pip install varwizard
```
3. Usage
    * Command-line
    
    You can use VarWizard by running the command
```bash
varwizard [--model-name {bloom-560m, codet5-base} (default: bloom-560m)]
            --input INPUT --lang {c,cpp,java,php,go,javascript,ruby,rust,python,c_sharp} 
            [--output-path OUTPUT_PATH (default: None)] [--max-input-len MAX_INPUT_LEN (default: 400)]
            [--device DEVICE (default: cpu)] [--penalty-alpha PENALTY_ALPHA (default: 0.6)] [--top-k TOP_K (default: 4)] [--max-new-tokens MAX_NEW_TOKENS (default: 100)]
```
Details for each argument can be found by 
```varwizard --help```


 * Python API

    Another way is to Python methods.
Here is a simple example of VarWizard.
```python
from varwizard import VarWizard

model = VarWizard(model_name = "codet5-base")
code = """
function chunkData(str, chunk) {
  var chunk = [];
  var length = str.length;
  var i = 0;
  for (; i < length; i += chunk) {
    if (i + chunk < length) {
      chunk.push(str.substring(i, i + chunk));
    } else {
      chunk.push(str.substring(i, length));
    }
  }
  return chunk;
}
"""
print(model.make_new_code(code, 'javascript', device = 'cuda:0'))
```
VarWizard produces the output
```javascript
function chunkData(str, chunk) {
  var chunk = [];
  var length = str.length;
  var i = 0;
  for (; i < length; i += chunk) {
    if (i + chunk < length) {
      chunk.push(str.substring(i, i + chunk));
    } else {
      chunk.push(str.substring(i, length));
    }
  }
  return chunk;
}
```

4. Playground: You can play at the link: https://varwizard.loca.lt. At the first time to access, you may need to enter: 4.193.50.237
5. Examples

There are some examples for varWizard's usage. We can navigate to the folder $examples$ and then go to any subfolder to run the script.