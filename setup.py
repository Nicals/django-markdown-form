from setuptools import setup

setup(
    name='django-markdown-form',
    version='',
    description='Markdown support for Django forms framework',
    long_description='Fill form fields with some uploaded markdown meta-data',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing',
    ],
    url='https://github.com/Nicals/django-markdown-form',
    author='Nicolas A.',
    license='GPLv3',
    packages=[
        'markdown_form',
        'markdown_form/rest',
        'markdown_form/tests'],
    install_requires=[
        'django',
        'markdown',
    ],
    zip_safe=False,
)
