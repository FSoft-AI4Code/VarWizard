### VarWizard
***
1. Installation
You can easily install this package by the command
```
    pip install varwizard
```
2. Tutorial
Here is a simple example of VarWizard.
```
from varwizard import VarWizard

model = VarWizard()
code = """
def add_numbers(num1, num2):
    sum = num1 + num2
    print("Sum: ",sum)"""
print(model.make_new_code(code, 'python'))
```