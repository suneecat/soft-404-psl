from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='soft-404-psl',
    version='0.4.0',
    author='Konstantin Lopuhin',
    author_email='kostia.lopuhin@gmail.com',
    description='A classifier for detecting soft 404 pages',
    license='MIT',
    url='https://github.com/TeamHG-Memex/soft404',
    packages=['soft404'],
    include_package_data=True,
    install_requires=[
        'langdetect==1.0.8',
        'lxml==4.5.2',
        'numpy==1.19.1',
        'parsel>=1.6.0',
        'scikit-learn==0.23.2',
        'joblib==0.16.0',
        'scipy>=1.5.2',
        'webstruct==0.6',
        'html_text==0.5.2',
    ],
    long_description=readme,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)
