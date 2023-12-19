from setuptools import setup, find_packages

setup(
    name="chatgpt-talk",
    version="0.1.0",
    author="retch",
    description="ChatGpt talk sample",
    #url="https://github.com/reatoretch/chatgpt-talk",
    install_requires=_requires_from_file('requirements.txt'),
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['chatgpttalk=chatgpttalk.main:main']
    },
    python_requires='>=3.11',
)