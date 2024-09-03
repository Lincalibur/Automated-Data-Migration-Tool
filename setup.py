from setuptools import setup, find_packages

setup(
    name='admt',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pandas',
        'openpyxl',
        'pyyaml',
        'sqlalchemy',
        # Additional dependencies
    ],
    extras_require={
        'dev': [
            'pytest',
            'sphinx',
            # Additional development dependencies
        ],
    },
    entry_points={
        'console_scripts': [
            'admt=src.main:main',  # Ensure this matches the actual entry point
        ],
    },
    author='Liam Olivier',
    author_email='lincalibur@gmail.com',
    description='Automated Data Migration Tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/admt',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
