from setuptools import setup, find_packages

setup(
    name="promptsmith",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv",
        "dspy",
        "openai",
        "ydata-profiling",
        "pandas",
        "numpy", 
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "ipywidgets",
        "streamlit"
        
    ],
)