from setuptools import setup

setup(
    name="mimid",
    version="0.0.1",
    description="Mocking library for Python.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Konrad Hałas",
    author_email="halas.konrad@gmail.com",
    url="https://github.com/konradhalas/mimid",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    keywords="testing mocking",
    py_modules=["mimid"],
    extras_require={"dev": ["pytest>=4", "pytest-cov", "coveralls", "black", "mypy", "pylint"]},
)