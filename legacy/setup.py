from distutils.core import setup


setup(
    name = 'euterpe',
    version = '0.0.0.1.dev',
    description = 'Self-hosted blind-test server',
    url = 'https://gitgud.io/Ninjananas/Euterpe',
    author = 'Paul Charles & Arsène Volte',
    author_email = 'ninjananas@tuta.io',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GPL3 License',
        'Programming Language :: Python :: 3.7'
    ],
    keywords = 'blind-test',
    packages = ('euterpe',
                'euterpe.analyzer',
                'euterpe.cli',
                'euterpe.cli.songs',
                'euterpe.database',
                'euterpe.extraction',
                'euterpe.misc',
                'euterpe.validation'),
)
