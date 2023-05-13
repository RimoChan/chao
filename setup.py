import setuptools


setuptools.setup(
    name='chao',
    version='0.0.1',
    author='RimoChan',
    author_email='the@librian.net',
    description='librian',
    long_description=open('readme.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/RimoChan/chao',
    packages=[
        '超',
    ],
    package_data={},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[],
    python_requires='>=3.8',
)
