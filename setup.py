from setuptools import setup, find_packages
setup(name='varwizard',
version='0.1',
description='An Automated Tool for Improving Code Quality Through Variable Name Refinement with Language Models',
url='https://github.com/FSoft-AI4Code/VarWizard',
author='FSoft-AI4Code',
author_email='support.aic@fpt.com',
license='Apache-2.0',
python_requires=">=3.7",
include_package_data=True,
install_requires=[
          'torch>=1.12.1',
          'peft',
          'transformers>=4.28.0',
          'tree-sitter'
      ],
packages=find_packages(),
zip_safe=False)