from setuptools import setup


setup(
    name='python-muckrock',
    version='0.0.7',
    description='A simple python wrapper for the MuckRock API',
    author='The Los Angeles Times Data Desk',
    author_email='datadesk@latimes.com',
    url='http://www.github.com/datadesk/python-muckrock/',
    license="MIT",
    packages=('muckrock',),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        'requests>=2.21.0',
    ],
)
