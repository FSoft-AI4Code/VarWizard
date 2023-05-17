from setuptools import setup, find_packages
setup(name='varwizard',
version='0.2',
description='An Automated Tool for Improving Code Quality Through Variable Name Refinement with Language Models',
url='https://github.com/FSoft-AI4Code/VarWizard',
author='FSoft-AI4Code',
author_email='support.aic@fpt.com',
license='Apache-2.0',
python_requires=">=3.7",
include_package_data=True,
entry_points={
        'console_scripts': ['varwizard=varwizard:main'],
},
install_requires=[
          'torch>=1.12.1',
          'peft==0.1.0',
          'transformers>=4.28.0',
          'tree-sitter',
          'codetext'
      ],
packages=find_packages(),
zip_safe=False)