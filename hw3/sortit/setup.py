from setuptools import setup, find_namespace_packages

setup(
    name='sorthis',
    version='0.2.0',
    description='sort every folder',
    url = '',
    author='webba1065',
    author_email='webba1065@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    install_requires=['prompt-toolkit','loguru'],
    entry_points={'console_scripts': ['sortit = main:main']}
)