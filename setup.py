from setuptools import setup, find_packages
setup(name='hscraper',
    version='0.2',
    description='A tool to rip galleries from ehentai, r34.xxx, danbooru.donmai and hitomi.la',
    url='https://github.com/XrossFox/hscraper',
    author='XrossFox',
    author_email='warhead_1090@hotmail.com',
    license='MIT',
    packages=find_packages(exclude="tests",),
    zip_safe=False,
    install_requires=[
        'beautifulsoup4',
        'urllib3',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'hscraper = hscraper.h_core:clickerino'
        ]
    },
)