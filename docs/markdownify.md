# markdownify


---

## 1. 

Convert HTML to markdown.

## Project description

## Installation

pip install markdownify

## Usage

Convert some HTML to Markdown:

```
frommarkdownifyimport markdownify as mdmd('<b>Yay</b> <a href="http://github.com">GitHub</a>')  # > '**Yay** [GitHub](http://github.com)'
```

Specify tags to exclude:

```
frommarkdownifyimport markdownify as mdmd('<b>Yay</b> <a href="http://github.com">GitHub</a>', strip=['a'])  # > '**Yay** GitHub'
```

...or specify the tags you want to include:

```
frommarkdownifyimport markdownify as mdmd('<b>Yay</b> <a href="http://github.com">GitHub</a>', convert=['b'])  # > '**Yay** GitHub'
```

## Options

Markdownify supports the following options:

strip
:   A list of tags to strip. This option can’t be used with the
    convert option.

convert
:   A list of tags to convert. This option can’t be used with the
    strip option.

autolinks
:   A boolean indicating whether the “automatic link” style should be used when
    a a tag’s contents match its href. Defaults to True.

default\_title
:   A boolean to enable setting the title of a link to its href, if no title is
    given. Defaults to False.

heading\_style
:   Defines how headings should be converted. Accepted values are ATX,
    ATX\_CLOSED, SETEXT, and UNDERLINED (which is an alias for
    SETEXT). Defaults to UNDERLINED.

bullets
:   An iterable (string, list, or tuple) of bullet styles to be used. If the
    iterable only contains one item, it will be used regardless of how deeply
    lists are nested. Otherwise, the bullet will alternate based on nesting
    level. Defaults to '\*+-'.

strong\_em\_symbol
:   In markdown, both \* and \_ are used to encode **strong** or
    *emphasized* texts. Either of these symbols can be chosen by the options
    ASTERISK (default) or UNDERSCORE respectively.

sub\_symbol, sup\_symbol
:   Define the chars that surround <sub> and <sup> text. Defaults to an
    empty string, because this is non-standard behavior. Could be something like
    ~ and ^ to result in ~sub~ and ^sup^. If the value starts
    with < and ends with >, it is treated as an HTML tag and a / is
    inserted after the < in the string used after the text; this allows
    specifying <sub> to use raw HTML in the output for subscripts, for
    example.

newline\_style
:   Defines the style of marking linebreaks (<br>) in markdown. The default
    value SPACES of this option will adopt the usual two spaces and a newline,
    while BACKSLASH will convert a linebreak to \\n (a backslash and a
    newline). While the latter convention is non-standard, it is commonly
    preferred and supported by a lot of interpreters.

code\_language
:   Defines the language that should be assumed for all <pre> sections.
    Useful, if all code on a page is in the same programming language and
    should be annotated with ```python or similar.
    Defaults to '' (empty string) and can be any string.

code\_language\_callback
:   When the HTML code contains pre tags that in some way provide the code
    language, for example as class, this callback can be used to extract the
    language from the tag and prefix it to the converted pre tag.
    The callback gets one single argument, a BeautifulSoup object, and returns
    a string containing the code language, or None.
    An example to use the class name as code language could be:

    ```
    def callback(el):
        return el['class'][0] if el.has_attr('class') else None
    ```

    Defaults to None.

escape\_asterisks
:   If set to False, do not escape \* to \\* in text.
    Defaults to True.

escape\_underscores
:   If set to False, do not escape \_ to \\_ in text.
    Defaults to True.

escape\_misc
:   If set to True, escape miscellaneous punctuation characters
    that sometimes have Markdown significance in text.
    Defaults to False.

keep\_inline\_images\_in
:   Images are converted to their alt-text when the images are located inside
    headlines or table cells. If some inline images should be converted to
    markdown images instead, this option can be set to a list of parent tags
    that should be allowed to contain inline images, for example ['td'].
    Defaults to an empty list.

table\_infer\_header
:   Controls handling of tables with no header row (as indicated by <thead>
    or <th>). When set to True, the first body row is used as the header row.
    Defaults to False, which leaves the header row empty.

wrap, wrap\_width
:   If wrap is set to True, all text paragraphs are wrapped at
    wrap\_width characters. Defaults to False and 80.
    Use with newline\_style=BACKSLASH to keep line breaks in paragraphs.
    A wrap\_width value of None reflows lines to unlimited line length.

strip\_document
:   Controls whether leading and/or trailing separation newlines are removed from
    the final converted document. Supported values are LSTRIP (leading),
    RSTRIP (trailing), STRIP (both), and None (neither). Newlines
    within the document are unaffected.
    Defaults to STRIP.

strip\_pre
:   Controls whether leading/trailing blank lines are removed from <pre>
    tags. Supported values are STRIP (all leading/trailing blank lines),
    STRIP\_ONE (one leading/trailing blank line), and None (neither).
    Defaults to STRIP.

bs4\_options
:   Specify additional configuration options for the BeautifulSoup object
    used to interpret the HTML markup. String and list values (such as lxml
    or html5lib) are treated as features arguments to control parser
    selection. Dictionary values (such as {"from\_encoding": "iso-8859-8"})
    are treated as full kwargs to be used for the BeautifulSoup constructor,
    allowing specification of any parameter. For parameter details, see the
    Beautiful Soup documentation at:

Options may be specified as kwargs to the markdownify function, or as a
nested Options class in MarkdownConverter subclasses.

## Converting BeautifulSoup objects

```
frommarkdownifyimport MarkdownConverter# Create shorthand method for conversiondefmd(soup, **options):    return MarkdownConverter(**options).convert_soup(soup)
```

## Creating Custom Converters

If you have a special usecase that calls for a special conversion, you can
always inherit from MarkdownConverter and override the method you want to
change.
The function that handles a HTML tag named abc is called
convert\_abc(self, el, text, parent\_tags) and returns a string
containing the converted HTML tag.
The MarkdownConverter object will handle the conversion based on the
function names:

```
frommarkdownifyimport MarkdownConverterclassImageBlockConverter(MarkdownConverter):"""
    Create a custom MarkdownConverter that adds two newlines after an image
    """    defconvert_img(self, el, text, parent_tags):        return super().convert_img(el, text, parent_tags) + '\n\n'# Create shorthand method for conversiondefmd(html, **options):    return ImageBlockConverter(**options).convert(html)
```

```
frommarkdownifyimport MarkdownConverterclassIgnoreParagraphsConverter(MarkdownConverter):"""
    Create a custom MarkdownConverter that ignores paragraphs
    """    defconvert_p(self, el, text, parent_tags):        return ''# Create shorthand method for conversiondefmd(html, **options):    return IgnoreParagraphsConverter(**options).convert(html)
```

## Command Line Interface

Use markdownify example.html > example.md or pipe input from stdin
(cat example.html | markdownify > example.md).
Call markdownify -h to see all available options.
They are the same as listed above and take the same arguments.

## Development

To run tests and the linter run pip install tox once, then tox.

## Project details

## Release history [Release notifications](/help/#project-release-notifications) | [RSS feed](/rss/project/markdownify/releases.xml)

This version

[1.2.2

Nov 16, 2025](/project/markdownify/1.2.2/)

[1.2.0

Aug 9, 2025](/project/markdownify/1.2.0/)

[1.1.0

Mar 5, 2025](/project/markdownify/1.1.0/)

[1.0.0

Feb 24, 2025](/project/markdownify/1.0.0/)

[0.14.1

Nov 24, 2024](/project/markdownify/0.14.1/)

[0.14.0

Nov 24, 2024](/project/markdownify/0.14.0/)

[0.13.1

Jul 14, 2024](/project/markdownify/0.13.1/)

[0.13.0

Jul 14, 2024](/project/markdownify/0.13.0/)

[0.12.1

Mar 26, 2024](/project/markdownify/0.12.1/)

[0.11.6

Sep 2, 2022](/project/markdownify/0.11.6/)

[0.11.5

Aug 31, 2022](/project/markdownify/0.11.5/)

[0.11.4

Aug 28, 2022](/project/markdownify/0.11.4/)

[0.11.2

Apr 24, 2022](/project/markdownify/0.11.2/)

[0.11.1

Apr 14, 2022](/project/markdownify/0.11.1/)

[0.11.0

Apr 13, 2022](/project/markdownify/0.11.0/)

[0.10.3

Jan 23, 2022](/project/markdownify/0.10.3/)

[0.10.2

Jan 18, 2022](/project/markdownify/0.10.2/)

[0.10.1

Dec 11, 2021](/project/markdownify/0.10.1/)

[0.10.0

Nov 17, 2021](/project/markdownify/0.10.0/)

[0.9.4

Sep 4, 2021](/project/markdownify/0.9.4/)

[0.9.3

Aug 25, 2021](/project/markdownify/0.9.3/)

[0.9.2

Jul 11, 2021](/project/markdownify/0.9.2/)

[0.9.0

May 30, 2021](/project/markdownify/0.9.0/)

[0.8.1

May 30, 2021](/project/markdownify/0.8.1/)

[0.8.0

May 21, 2021](/project/markdownify/0.8.0/)

[0.7.4

May 18, 2021](/project/markdownify/0.7.4/)

[0.7.3

May 16, 2021](/project/markdownify/0.7.3/)

[0.7.2

May 2, 2021](/project/markdownify/0.7.2/)

[0.7.1

May 2, 2021](/project/markdownify/0.7.1/)

[0.7.0

Apr 22, 2021](/project/markdownify/0.7.0/)

[0.6.6

Apr 22, 2021](/project/markdownify/0.6.6/)

[0.6.5

Feb 21, 2021](/project/markdownify/0.6.5/)

[0.6.4

Feb 21, 2021](/project/markdownify/0.6.4/)

[0.6.3

Jan 12, 2021](/project/markdownify/0.6.3/)

[0.6.1

Jan 4, 2021](/project/markdownify/0.6.1/)

[0.6.0

Dec 13, 2020](/project/markdownify/0.6.0/)

[0.5.3

Sep 1, 2020](/project/markdownify/0.5.3/)

[0.5.2

Aug 18, 2020](/project/markdownify/0.5.2/)

[0.5.1

Aug 11, 2020](/project/markdownify/0.5.1/)

[0.4.1

Nov 27, 2017](/project/markdownify/0.4.1/)

[0.4.0

Aug 1, 2013](/project/markdownify/0.4.0/)

[0.3.0

Jul 31, 2013](/project/markdownify/0.3.0/)

[0.2.0

Jul 31, 2013](/project/markdownify/0.2.0/)

## Download files

Download the file for your platform. If you're not sure which to choose, learn more about [installing packages](https://packaging.python.org/tutorials/installing-packages/ "External link").

### Source Distribution

[markdownify-1.2.2.tar.gz](https://files.pythonhosted.org/packages/3f/bc/c8c8eea5335341306b0fa7e1cb33c5e1c8d24ef70ddd684da65f41c49c92/markdownify-1.2.2.tar.gz)
(18.8 kB
[view details](#markdownify-1.2.2.tar.gz))

Uploaded 
Nov 16, 2025
`Source`

### Built Distribution

Filter files by name, interpreter, ABI, and platform.

If you're not sure about the file name format, learn more about [wheel file names](https://packaging.python.org/en/latest/specifications/binary-distribution-format/ "External link").

Copy a direct link to the current filters

Interpreter
py3

ABI
none

Platform
any

[markdownify-1.2.2-py3-none-any.whl](https://files.pythonhosted.org/packages/43/ce/f1e3e9d959db134cedf06825fae8d5b294bd368aacdd0831a3975b7c4d55/markdownify-1.2.2-py3-none-any.whl)
(15.7 kB
[view details](#markdownify-1.2.2-py3-none-any.whl))

Uploaded 
Nov 16, 2025
`Python 3`

## File details

Details for the file `markdownify-1.2.2.tar.gz`.

### File metadata

* Download URL: [markdownify-1.2.2.tar.gz](https://files.pythonhosted.org/packages/3f/bc/c8c8eea5335341306b0fa7e1cb33c5e1c8d24ef70ddd684da65f41c49c92/markdownify-1.2.2.tar.gz)
* Upload date: 
  Nov 16, 2025
* Size: 18.8 kB
* Tags: Source
* Uploaded using Trusted Publishing? No
* Uploaded via: twine/6.1.0 CPython/3.8.18

### File hashes

Hashes for markdownify-1.2.2.tar.gz

| Algorithm | Hash digest |  |
| --- | --- | --- |
| SHA256 | `b274f1b5943180b031b699b199cbaeb1e2ac938b75851849a31fd0c3d6603d09` |  |
| MD5 | `15bd29cdcf8c6b2ef03102ac7c2c737c` |  |
| BLAKE2b-256 | `3fbcc8c8eea5335341306b0fa7e1cb33c5e1c8d24ef70ddd684da65f41c49c92` |  |

[See more details on using hashes here.](https://pip.pypa.io/en/stable/topics/secure-installs/#hash-checking-mode "External link")

## File details

Details for the file `markdownify-1.2.2-py3-none-any.whl`.

### File metadata

* Download URL: [markdownify-1.2.2-py3-none-any.whl](https://files.pythonhosted.org/packages/43/ce/f1e3e9d959db134cedf06825fae8d5b294bd368aacdd0831a3975b7c4d55/markdownify-1.2.2-py3-none-any.whl)
* Upload date: 
  Nov 16, 2025
* Size: 15.7 kB
* Tags: Python 3
* Uploaded using Trusted Publishing? No
* Uploaded via: twine/6.1.0 CPython/3.8.18

### File hashes

Hashes for markdownify-1.2.2-py3-none-any.whl

| Algorithm | Hash digest |  |
| --- | --- | --- |
| SHA256 | `3f02d3cc52714084d6e589f70397b6fc9f2f3a8531481bf35e8cc39f975e186a` |  |
| MD5 | `1854f3f3eb3384c71741bff763f5cac4` |  |
| BLAKE2b-256 | `43cef1e3e9d959db134cedf06825fae8d5b294bd368aacdd0831a3975b7c4d55` |  |

[See more details on using hashes here.](https://pip.pypa.io/en/stable/topics/secure-installs/#hash-checking-mode "External link")

---

## Bibliography

1. [](https://pypi.org/project/markdownify/)