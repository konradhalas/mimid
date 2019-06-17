from setuptools import setup

setup(
    name="mimid",
    version="0.0.5",
    description="Mocking library for Python.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Konrad Hałas",
    author_email="halas.konrad@gmail.com",
    url="https://github.com/konradhalas/mimid",
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Mocking",
    ],
    python_requires=">=3.6",
    keywords="testing mocking",
    py_modules=["mimid"],
    extras_require={"dev": ["pytest>=4", "pytest-cov", "coveralls", "black", "mypy", "pylint"]},
)
