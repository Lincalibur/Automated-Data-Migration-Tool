from setuptools import setup, find_packages

setup(
    name='admt',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'flask',
        'pypdf',
        'python-docx',
        'pandas',
        'openpyxl',
        'sqlalchemy',
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'admt=main:main',
        ],
    },
    author='Liam Olivier',
    author_email='lincalibur@gmail.com',
    description='Automated Data Migration Tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Lincalibur/Automated-Data-Migration-Tool',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.9',
)
