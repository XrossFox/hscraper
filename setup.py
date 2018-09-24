from setuptools import setup, find_packages
setup(name='hscraper',
    version='0.5',
    description='A tool to rip galleries from ehentai, r34.xxx, danbooru.donmai and hitomi.la',
    url='https://github.com/XrossFox/hscraper',
    author='XrossFox',
    author_email='warhead_1090@hotmail.com',
    license='MIT',
    packages=find_packages(exclude=["tests"],),
    zip_safe=False,
    install_requires=[
        'beautifulsoup4>=4.6.0',
        'urllib3>=1.22',
        'click>=6.7',
    ],
    entry_points={
        'console_scripts': [
            'hscraper = hscraper.h_core:clickerino'
        ]
    },
    data_files = [("",["LICENSE"])],
)