from distutils.core import setup
import euterpe


setup(
    name = "euterpe",
    description = "Self-hosted blind-test server",
    author = "Paul Charles & Arsène Volte",
    version = euterpe.__version__,
    classifiers = [
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GPL3 License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords = "blind_test",
    packages = (
        "euterpe",
    )
)
