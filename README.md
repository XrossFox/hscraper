# HenScrapper
A web scrapping tool to rip images from Ehentai, Danbooru, R34 and hitomi.la.

## **A HUGE NSFW WARNING:** None of these pages could be considered suitable for work nor school.

- I made this as both, practice and as an utilitarian tool for myself (lel).
- It works as a common CLI that lets you save galleries to your hard drive easily.
- It Supports Batch downloads from a 'txt' file with links (must specify number of pages too).
- Finally usable.
- It requires click, urllib3 and beautiful soup 4 to work.
- Made in Python 3.

### Installation:
As easy as:
> pip install hscraper

*It'll also install dependencies if you don't have them already.*

### Usage
- hscraper [OPTIONS]
- **-b:** To set a txt with links in it, give it the path to it. Overrides -u and -p. It must be <url>,<page> per line.
- **-u**: To set the url to the gallery.
- **-p**: The number of pages to download. Defaults to 1 if not set.
- **-o**: Output directory for the gallery.
- **-w**: Wait time between downloaded image (just in case, so you don't get ip banned from nowhere). Defaults to 1.0 second if not set.
- **--help**: *HALP!*

And that's it folks.







