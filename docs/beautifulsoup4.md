# BeautifulSoup4


---

## 1. Beautiful Soup Documentation

[Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/) is a
Python library for pulling data out of HTML and XML files. It works
with your favorite parser to provide idiomatic ways of navigating,
searching, and modifying the parse tree. It commonly saves programmers
hours or days of work.

These instructions illustrate all major features of Beautiful Soup 4,
with examples. I show you what the library is good for, how it works,
how to use it, how to make it do what you want, and what to do when it
violates your expectations.

This document covers Beautiful Soup version 4.14.3. The examples in
this documentation were written for Python 3.8.

You might be looking for the documentation for [Beautiful Soup 3](http://www.crummy.com/software/BeautifulSoup/bs3/documentation.html).
If so, you should know that Beautiful Soup 3 is no longer being
developed and that all support for it was dropped on December
31, 2020. If you want to learn about the differences between Beautiful
Soup 3 and Beautiful Soup 4, see [Porting code to BS4](#porting-code-to-bs4).

This documentation has been translated into other languages by
Beautiful Soup users:

* [这篇文档当然还有中文版.](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/)
* このページは日本語で利用できます([外部リンク](http://kondou.com/BS4/))
* [이 문서는 한국어 번역도 가능합니다.](https://www.crummy.com/software/BeautifulSoup/bs4/doc.ko/)
* [Este documento também está disponível em Português do Brasil.](https://www.crummy.com/software/BeautifulSoup/bs4/doc.ptbr)
* [Este documento también está disponible en una traducción al español.](https://www.crummy.com/software/BeautifulSoup/bs4/doc.es/)
* [Эта документация доступна на русском языке.](https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru/)

## Getting help

If you have questions about Beautiful Soup, or run into problems,
[send mail to the discussion group](https://groups.google.com/forum/?fromgroups#!forum/beautifulsoup). If
your problem involves parsing an HTML document, be sure to mention
[what the diagnose() function says](#diagnose) about
that document.

When reporting an error in this documentation, please mention which
translation you're reading.

### API documentation

This document is written like an instruction manual, but you can also read
[traditional API documentation](api/modules.html)
generated from the Beautiful Soup source code. If you want details
about Beautiful Soup's internals, or a feature not covered in this
document, try the API documentation.

# Quick Start

Here's an HTML document I'll be using as an example throughout this
document. It's part of a story from *Alice in Wonderland*:

```
html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
```

Running the "three sisters" document through Beautiful Soup gives us a
`BeautifulSoup` object, which represents the document as a nested
data structure:

```
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.prettify())
# <html>
#  <head>
#   <title>
#    The Dormouse's story
#   </title>
#  </head>
#  <body>
#   <p class="title">
#    <b>
#     The Dormouse's story
#    </b>
#   </p>
#   <p class="story">
#    Once upon a time there were three little sisters; and their names were
#    <a class="sister" href="http://example.com/elsie" id="link1">
#     Elsie
#    </a>
#    ,
#    <a class="sister" href="http://example.com/lacie" id="link2">
#     Lacie
#    </a>
#    and
#    <a class="sister" href="http://example.com/tillie" id="link3">
#     Tillie
#    </a>
#    ; and they lived at the bottom of a well.
#   </p>
#   <p class="story">
#    ...
#   </p>
#  </body>
# </html>
```

Here are some simple ways to navigate that data structure:

```
soup.title
# <title>The Dormouse's story</title>

soup.title.name
# u'title'

soup.title.string
# u'The Dormouse's story'

soup.title.parent.name
# u'head'

soup.p
# <p class="title"><b>The Dormouse's story</b></p>

soup.p['class']
# u'title'

soup.a
# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

soup.find_all('a')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.find(id="link3")
# <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
```

One common task is extracting all the URLs found within a page's <a> tags:

```
for link in soup.find_all('a'):
    print(link.get('href'))
# http://example.com/elsie
# http://example.com/lacie
# http://example.com/tillie
```

Another common task is extracting all the text from a page:

```
print(soup.get_text())
# The Dormouse's story
#
# The Dormouse's story
#
# Once upon a time there were three little sisters; and their names were
# Elsie,
# Lacie and
# Tillie;
# and they lived at the bottom of a well.
#
# ...
```

Does this look like what you need? If so, read on.

# Installing Beautiful Soup

If you're using a recent version of Debian or Ubuntu Linux, you can
install Beautiful Soup with the system package manager:

`$ apt-get install python3-bs4`

Beautiful Soup 4 is published through PyPi, so if you can't install it
with the system packager, you can install it with `easy_install` or
`pip`. The package name is `beautifulsoup4`. Make sure you use the
right version of `pip` or `easy_install` for your Python version
(these may be named `pip3` and `easy_install3` respectively).

`$ easy_install beautifulsoup4`

`$ pip install beautifulsoup4`

(The `BeautifulSoup` package is *not* what you want. That's
the previous major release, [Beautiful Soup 3](http://www.crummy.com/software/BeautifulSoup/bs3/documentation.html). Lots of software uses
BS3, so it's still available, but if you're writing new code you
should install `beautifulsoup4`.)

If you don't have `easy_install` or `pip` installed, you can
[download the Beautiful Soup 4 source tarball](http://www.crummy.com/software/BeautifulSoup/download/4.x/) and
install it with `setup.py`.

`$ python setup.py install`

If all else fails, the license for Beautiful Soup allows you to
package the entire library with your application. You can download the
tarball, copy its `bs4` directory into your application's codebase,
and use Beautiful Soup without installing it at all.

I use Python 3.10 to develop Beautiful Soup, but it should work with
other recent versions.

## Installing a parser

Beautiful Soup supports the HTML parser included in Python's standard
library, but it also supports a number of third-party Python parsers.
One is the [lxml parser](http://lxml.de/). Depending on your setup,
you might install lxml with one of these commands:

`$ apt-get install python-lxml`

`$ easy_install lxml`

`$ pip install lxml`

Another alternative is the pure-Python [html5lib parser](http://code.google.com/p/html5lib/), which parses HTML the way a
web browser does. Depending on your setup, you might install html5lib
with one of these commands:

`$ apt-get install python3-html5lib`

`$ pip install html5lib`

This table summarizes the advantages and disadvantages of each parser library:

|  |  |  |  |
| --- | --- | --- | --- |
| Parser | Typical usage | Advantages | Disadvantages |
| Python's html.parser | `BeautifulSoup(markup, "html.parser")` | * Batteries included * Decent speed | * Not as fast as lxml,   less lenient than   html5lib. |
| lxml's HTML parser | `BeautifulSoup(markup, "lxml")` | * Very fast | * External C dependency |
| lxml's XML parser | `BeautifulSoup(markup, "lxml-xml")` `BeautifulSoup(markup, "xml")` | * Very fast * The only currently supported   XML parser | * External C dependency |
| html5lib | `BeautifulSoup(markup, "html5lib")` | * Extremely lenient * Parses pages the same way a   web browser does * Creates valid HTML5 | * Very slow * External Python   dependency |

If you can, I recommend you install and use lxml for speed.

Note that if a document is invalid, different parsers will generate
different Beautiful Soup trees for it. See [Differences
between parsers](#differences-between-parsers) for details.

# Making the soup

To parse a document, pass it into the `BeautifulSoup`
constructor. You can pass in a string or an open filehandle:

```
from bs4 import BeautifulSoup

with open("index.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

soup = BeautifulSoup("<html>a web page</html>", 'html.parser')
```

First, the document is converted to Unicode, and HTML entities are
converted to Unicode characters:

```
print(BeautifulSoup("<html><head></head><body>Sacr&eacute; bleu!</body></html>", "html.parser"))
# <html><head></head><body>Sacré bleu!</body></html>
```

Beautiful Soup then parses the document using the best available
parser. It will use an HTML parser unless you specifically tell it to
use an XML parser. (See [Parsing XML](#id15).)

# Kinds of objects

Beautiful Soup transforms a complex HTML document into a complex tree
of Python objects. But you'll only ever have to deal with about four
*kinds* of objects: [`Tag`](#Tag "Tag"), [`NavigableString`](#NavigableString "NavigableString"), `BeautifulSoup`,
and [`Comment`](#Comment "Comment"). These objects represent the HTML *elements*
that comprise the page.

*class*Tag
:   A [`Tag`](#Tag "Tag") object corresponds to an XML or HTML tag in the original document.

    ```
    soup = BeautifulSoup('<b class="boldest">Extremely bold</b>', 'html.parser')
    tag = soup.b
    type(tag)
    # <class 'bs4.element.Tag'>
    ```

    Tags have a lot of attributes and methods, and I'll cover most of them
    in [Navigating the tree](#navigating-the-tree) and [Searching the tree](#searching-the-tree). For now, the most
    important methods of a tag are for accessing its name and attributes.

    name
    :   Every tag has a name:

        ```
        tag.name
        # 'b'
        ```

        If you change a tag's name, the change will be reflected in any
        markup generated by Beautiful Soup down the line:

        ```
        tag.name = "blockquote"
        tag
        # <blockquote class="boldest">Extremely bold</blockquote>
        ```

    attrs
    :   An HTML or XML tag may have any number of attributes. The tag `<b
        id="boldest">` has an attribute "id" whose value is
        "boldest". You can access a tag's attributes by treating the tag like
        a dictionary:

        ```
        tag = BeautifulSoup('<b id="boldest">bold</b>', 'html.parser').b
        tag['id']
        # 'boldest'
        ```

        You can access the dictionary of attributes directly as `.attrs`:

        ```
        tag.attrs
        # {'id': 'boldest'}
        tag.attrs.keys()
        # dict_keys(['id'])
        ```

        You can add, remove, and modify a tag's attributes. Again, this is
        done by treating the tag as a dictionary:

        ```
        tag['id'] = 'verybold'
        tag['another-attribute'] = 1
        tag
        # <b another-attribute="1" id="verybold"></b>

        del tag['id']
        del tag['another-attribute']
        tag
        # <b>bold</b>

        tag['id']
        # KeyError: 'id'
        tag.get('id')
        # None
        ```

        ## Multi-valued attributes

        HTML 4 defines a few attributes that can have multiple values. HTML 5
        removes a couple of them, but defines a few more. The most common
        multi-valued attribute is `class` (that is, a tag can have more than
        one CSS class). Others include `rel`, `rev`, `accept-charset`,
        `headers`, and `accesskey`. By default, Beautiful Soup stores the value(s)
        of a multi-valued attribute as a list:

        ```
        css_soup = BeautifulSoup('<p class="body"></p>', 'html.parser')
        css_soup.p['class']
        # ['body']

        css_soup = BeautifulSoup('<p class="body strikeout"></p>', 'html.parser')
        css_soup.p['class']
        # ['body', 'strikeout']
        ```

        When you turn a tag back into a string, the values of any multi-valued
        attributes are consolidated:

        ```
        rel_soup = BeautifulSoup('<p>Back to the <a rel="index first">homepage</a></p>', 'html.parser')
        rel_soup.a['rel']
        # ['index', 'first']
        rel_soup.a['rel'] = ['index', 'contents']
        print(rel_soup.p)
        # <p>Back to the <a rel="index contents">homepage</a></p>
        ```

        If an attribute *looks* like it has more than one value, but it's not
        a multi-valued attribute as defined by any version of the HTML
        standard, Beautiful Soup stores it as a simple string:

        ```
        id_soup = BeautifulSoup('<p id="my id"></p>', 'html.parser')
        id_soup.p['id']
        # 'my id'
        ```

        You can force all attributes to be stored as strings by passing
        `multi_valued_attributes=None` as a keyword argument into the
        `BeautifulSoup` constructor:

        ```
        no_list_soup = BeautifulSoup('<p class="body strikeout"></p>', 'html.parser', multi_valued_attributes=None)
        no_list_soup.p['class']
        # 'body strikeout'
        ```

        You can use `get_attribute_list` to always return the value in a list
        container, whether it's a string or multi-valued attribute value:

        ```
        id_soup.p['id']
        # 'my id'
        id_soup.p.get_attribute_list('id')
        # ["my id"]
        ```

        If you parse a document as XML, there are no multi-valued attributes:

        ```
        xml_soup = BeautifulSoup('<p class="body strikeout"></p>', 'xml')
        xml_soup.p['class']
        # 'body strikeout'
        ```

        Again, you can configure this using the `multi_valued_attributes` argument:

        ```
        class_is_multi= { '*' : 'class'}
        xml_soup = BeautifulSoup('<p class="body strikeout"></p>', 'xml', multi_valued_attributes=class_is_multi)
        xml_soup.p['class']
        # ['body', 'strikeout']
        ```

        You probably won't need to do this, but if you do, use the defaults as
        a guide. They implement the rules described in the HTML specification:

        ```
        from bs4.builder import builder_registry
        builder_registry.lookup('html').DEFAULT_CDATA_LIST_ATTRIBUTES
        ```

*class*NavigableString

---

A tag can contain strings as pieces of text. Beautiful Soup
uses the [`NavigableString`](#NavigableString "NavigableString") class to contain these pieces of text:

```
soup = BeautifulSoup('<b class="boldest">Extremely bold</b>', 'html.parser')
tag = soup.b
tag.string
# 'Extremely bold'
type(tag.string)
# <class 'bs4.element.NavigableString'>
```

A [`NavigableString`](#NavigableString "NavigableString") is just like a Python Unicode string, except
that it also supports some of the features described in [Navigating
the tree](#navigating-the-tree) and [Searching the tree](#searching-the-tree). You can convert a
[`NavigableString`](#NavigableString "NavigableString") to a Unicode string with `str`:

```
unicode_string = str(tag.string)
unicode_string
# 'Extremely bold'
type(unicode_string)
# <type 'str'>
```

You can't edit a string in place, but you can replace one string with
another, using [replace\_with()](#replace-with):

```
tag.string.replace_with("No longer bold")
tag
# <b class="boldest">No longer bold</b>
```

[`NavigableString`](#NavigableString "NavigableString") supports most of the features described in
[Navigating the tree](#navigating-the-tree) and [Searching the tree](#searching-the-tree), but not all of
them. In particular, since a string can't contain anything (the way a
tag may contain a string or another tag), strings don't support the
`.contents` or `.string` attributes, or the `find()` method.

If you want to use a [`NavigableString`](#NavigableString "NavigableString") outside of Beautiful Soup,
you should call `unicode()` on it to turn it into a normal Python
Unicode string. If you don't, your string will carry around a
reference to the entire Beautiful Soup parse tree, even when you're
done using Beautiful Soup. This is a big waste of memory.

---

The `BeautifulSoup` object represents the parsed document as a
whole. For most purposes, you can treat it as a [`Tag`](#Tag "Tag")
object. This means it supports most of the methods described in
[Navigating the tree](#navigating-the-tree) and [Searching the tree](#searching-the-tree).

You can also pass a `BeautifulSoup` object into one of the methods
defined in [Modifying the tree](#modifying-the-tree), just as you would a [`Tag`](#Tag "Tag"). This
lets you do things like combine two parsed documents:

```
doc = BeautifulSoup("<document><content/>INSERT FOOTER HERE</document", "xml")
footer = BeautifulSoup("<footer>Here's the footer</footer>", "xml")
doc.find(text="INSERT FOOTER HERE").replace_with(footer)
# 'INSERT FOOTER HERE'
print(doc)
# <?xml version="1.0" encoding="utf-8"?>
# <document><content/><footer>Here's the footer</footer></document>
```

Since the `BeautifulSoup` object doesn't correspond to an actual
HTML or XML tag, it has no name and no attributes. But sometimes it's
useful to reference its `.name` (such as when writing code that works
with both [`Tag`](#Tag "Tag") and `BeautifulSoup` objects),
so it's been given the special `.name` "[document]":

```
soup.name
# '[document]'
```

## Special strings

[`Tag`](#Tag "Tag"), [`NavigableString`](#NavigableString "NavigableString"), and
`BeautifulSoup` cover almost everything you'll see in an
HTML or XML file, but there are a few leftover bits. The main one
you'll probably encounter is the [`Comment`](#Comment "Comment").

*class*Comment

```
markup = "<b><!--Hey, buddy. Want to buy a used parser?--></b>"
soup = BeautifulSoup(markup, 'html.parser')
comment = soup.b.string
type(comment)
# <class 'bs4.element.Comment'>
```

The [`Comment`](#Comment "Comment") object is just a special type of [`NavigableString`](#NavigableString "NavigableString"):

```
comment
# 'Hey, buddy. Want to buy a used parser'
```

But when it appears as part of an HTML document, a [`Comment`](#Comment "Comment") is
displayed with special formatting:

```
print(soup.b.prettify())
# <b>
#  <!--Hey, buddy. Want to buy a used parser?-->
# </b>
```

### For HTML documents

Beautiful Soup defines a few [`NavigableString`](#NavigableString "NavigableString") subclasses to
contain strings found inside specific HTML tags. This makes it easier
to pick out the main body of the page, by ignoring strings that
probably represent programming directives found within the
page. *(These classes are new in Beautiful Soup 4.9.0, and the
html5lib parser doesn't use them.)*

*class*Stylesheet

A [`NavigableString`](#NavigableString "NavigableString") subclass that represents embedded CSS
stylesheets; that is, any strings found inside a `<style>` tag
during document parsing.

*class*Script

A [`NavigableString`](#NavigableString "NavigableString") subclass that represents embedded
Javascript; that is, any strings found inside a `<script>` tag
during document parsing.

*class*Template

A [`NavigableString`](#NavigableString "NavigableString") subclass that represents embedded HTML
templates; that is, any strings found inside a `<template>` tag during
document parsing.

### For XML documents

Beautiful Soup defines some [`NavigableString`](#NavigableString "NavigableString") classes for
holding special types of strings that can be found in XML
documents. Like [`Comment`](#Comment "Comment"), these classes are subclasses of
[`NavigableString`](#NavigableString "NavigableString") that add something extra to the string on
output.

*class*Declaration

A [`NavigableString`](#NavigableString "NavigableString") subclass representing the [declaration](https://www.w3.org/TR/REC-xml/#sec-prolog-dtd) at the beginning of
an XML document.

*class*Doctype

A [`NavigableString`](#NavigableString "NavigableString") subclass representing the [document type
declaration](https://www.w3.org/TR/REC-xml/#dt-doctype) which may
be found near the beginning of an XML document.

*class*CData

A [`NavigableString`](#NavigableString "NavigableString") subclass that represents a [CData section](https://www.w3.org/TR/REC-xml/#sec-cdata-sect).

*class*ProcessingInstruction

A [`NavigableString`](#NavigableString "NavigableString") subclass that represents the contents
of an [XML processing instruction](https://www.w3.org/TR/REC-xml/#sec-pi).

# Modifying the tree

Beautiful Soup's main strength is in searching the parse tree, but you
can also modify the tree and write your changes as a new HTML or XML
document.

## Changing tag names and attributes

I covered this earlier, in [`Tag.attrs`](#Tag.attrs "Tag.attrs"), but it bears repeating. You
can rename a tag, change the values of its attributes, add new
attributes, and delete attributes:

```
soup = BeautifulSoup('<b class="boldest">Extremely bold</b>', 'html.parser')
tag = soup.b

tag.name = "blockquote"
tag['class'] = 'verybold'
tag['id'] = 1
tag
# <blockquote class="verybold" id="1">Extremely bold</blockquote>

del tag['class']
del tag['id']
tag
# <blockquote>Extremely bold</blockquote>
```

## Modifying `.string`

If you set a tag's `.string` attribute to a new string, the tag's contents are
replaced with that string:

```
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')

tag = soup.a
tag.string = "New link text."
tag
# <a href="http://example.com/">New link text.</a>
```

Be careful: if the tag contained other tags, they and all their
contents will be destroyed.

## `append()`

You can add to a tag's contents with `Tag.append()`. It works just
like calling `.append()` on a Python list:

```
soup = BeautifulSoup("<a>Foo</a>", 'html.parser')
new_string = soup.a.append("Bar")

soup
# <a>FooBar</a>
soup.a.contents
# ['Foo', 'Bar']
new_string
# 'Bar'
```

`Tag.append()` returns the newly appended element.

## `extend()`

Starting in Beautiful Soup 4.7.0, [`Tag`](#Tag "Tag") also supports a method
called `.extend()`, which adds every element of a list to a [`Tag`](#Tag "Tag"),
in order:

```
soup = BeautifulSoup("<a>Soup</a>", 'html.parser')
soup.a.extend(["'s", " ", "on"])

soup
# <a>Soup's on</a>
soup.a.contents
# ['Soup', ''s', ' ', 'on']
```

`Tag.extend()` returns the list of appended elements.

## `insert()`

`Tag.insert()` is just like `Tag.append()`, except the new element
doesn't necessarily go at the end of its parent's
`.contents`. It will be inserted at whatever numeric position you
say, similar to `.insert()` on a Python list:

```
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')
tag = soup.a

new_string = tag.insert(1, "but did not endorse ")
tag
# <a href="http://example.com/">I linked to but did not endorse <i>example.com</i></a>
tag.contents
# ['I linked to ', 'but did not endorse ', <i>example.com</i>]
new_string
# 'but did not endorse '
```

You can pass more than one element into `Tag.insert()`. All the
elements will be inserted, starting at the numeric position you
provide.

`Tag.insert()` returns the list of newly inserted elements.

## `insert_before()` and `insert_after()`

The `insert_before()` method inserts tags or strings immediately
before something else in the parse tree:

```
soup = BeautifulSoup("<b>leave</b>", 'html.parser')
tag = soup.new_tag("i")
tag.string = "Don't"
soup.b.string.insert_before(tag)
soup.b
# <b><i>Don't</i>leave</b>
```

The `insert_after()` method inserts tags or strings immediately
after something else in the parse tree:

```
div = soup.new_tag('div')
div.string = 'ever'
soup.b.i.insert_after(" you ", div)
soup.b
# <b><i>Don't</i> you <div>ever</div> leave</b>
soup.b.contents
# [<i>Don't</i>, ' you', <div>ever</div>, 'leave']
```

Both methods return the list of newly inserted elements.

## `clear()`

`Tag.clear()` removes the contents of a tag:

```
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')
tag = soup.a

tag.clear()
tag
# <a href="http://example.com/"></a>
```

## `extract()`

`PageElement.extract()` removes a tag or string from the tree. It
returns the tag or string that was extracted:

```
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')
a_tag = soup.a

i_tag = soup.i.extract()

a_tag
# <a href="http://example.com/">I linked to</a>

i_tag
# <i>example.com</i>

print(i_tag.parent)
# None
```

At this point you effectively have two parse trees: one rooted at the
`BeautifulSoup` object you used to parse the document, and one rooted
at the tag that was extracted. You can go on to call `extract()` on
a child of the element you extracted:

```
my_string = i_tag.string.extract()
my_string
# 'example.com'

print(my_string.parent)
# None
i_tag
# <i></i>
```

## `decompose()`

`Tag.decompose()` removes a tag from the tree, then *completely
destroys it and its contents*:

```
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')
a_tag = soup.a
i_tag = soup.i

i_tag.decompose()
a_tag
# <a href="http://example.com/">I linked to</a>
```

The behavior of a decomposed [`Tag`](#Tag "Tag") or [`NavigableString`](#NavigableString "NavigableString") is not
defined and you should not use it for anything. If you're not sure
whether something has been decomposed, you can check its
`.decomposed` property *(new in Beautiful Soup 4.9.0)*:

```
i_tag.decomposed
# True

a_tag.decomposed
# False
```

## `replace_with()`

`PageElement.replace_with()` extracts a tag or string from the tree,
then replaces it with one or more tags or strings of your choice:

```
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')
a_tag = soup.a

new_tag = soup.new_tag("b")
new_tag.string = "example.com"
a_tag.i.replace_with(new_tag)

a_tag
# <a href="http://example.com/">I linked to <b>example.com</b></a>

bold_tag = soup.new_tag("b")
bold_tag.string = "example"
i_tag = soup.new_tag("i")
i_tag.string = "net"
a_tag.b.replace_with(bold_tag, ".", i_tag)

a_tag
# <a href="http://example.com/">I linked to <b>example</b>.<i>net</i></a>
```

`replace_with()` returns the tag or string that got replaced, so
that you can examine it or add it back to another part of the tree.

*The ability to pass multiple arguments into replace\_with() is new
in Beautiful Soup 4.10.0.*

## `wrap()`

`PageElement.wrap()` wraps an element in the [`Tag`](#Tag "Tag") object you specify. It
returns the new wrapper:

```
soup = BeautifulSoup("<p>I wish I was bold.</p>", 'html.parser')
soup.p.string.wrap(soup.new_tag("b"))
# <b>I wish I was bold.</b>

soup.p.wrap(soup.new_tag("div"))
# <div><p><b>I wish I was bold.</b></p></div>
```

*This method is new in Beautiful Soup 4.0.5.*

## `unwrap()`

`Tag.unwrap()` is the opposite of `wrap()`. It replaces a tag with
whatever's inside that tag. It's good for stripping out markup:

```
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')
a_tag = soup.a

a_tag.i.unwrap()
a_tag
# <a href="http://example.com/">I linked to example.com</a>
```

Like `replace_with()`, `unwrap()` returns the tag
that was replaced.

## `smooth()`

After calling a bunch of methods that modify the parse tree, you may end up
with two or more [`NavigableString`](#NavigableString "NavigableString") objects next to each other.
Beautiful Soup doesn't have any problems with this, but since it can't happen
in a freshly parsed document, you might not expect behavior like the
following:

```
soup = BeautifulSoup("<p>A one</p>", 'html.parser')
soup.p.append(", a two")

soup.p.contents
# ['A one', ', a two']

print(soup.p.encode())
# b'<p>A one, a two</p>'

print(soup.p.prettify())
# <p>
#  A one
#  , a two
# </p>
```

You can call `Tag.smooth()` to clean up the parse tree by consolidating adjacent strings:

```
soup.smooth()

soup.p.contents
# ['A one, a two']

print(soup.p.prettify())
# <p>
#  A one, a two
# </p>
```

*This method is new in Beautiful Soup 4.8.0.*

# Output

## Pretty-printing

The `prettify()` method will turn a Beautiful Soup parse tree into a
nicely formatted Unicode string, with a separate line for each
tag and each string:

```
markup = '<html><head><body><a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')
soup.prettify()
# '<html>\n <head>\n </head>\n <body>\n  <a href="http://example.com/">\n...'

print(soup.prettify())
# <html>
#  <head>
#  </head>
#  <body>
#   <a href="http://example.com/">
#    I linked to
#    <i>
#     example.com
#    </i>
#   </a>
#  </body>
# </html>
```

You can call `prettify()` on the top-level `BeautifulSoup` object,
or on any of its [`Tag`](#Tag "Tag") objects:

```
print(soup.a.prettify())
# <a href="http://example.com/">
#  I linked to
#  <i>
#   example.com
#  </i>
# </a>
```

Since it adds whitespace (in the form of newlines), `prettify()`
changes the meaning of an HTML document and should not be used to
reformat one. The goal of `prettify()` is to help you visually
understand the structure of the documents you work with.

## Non-pretty printing

If you just want a string, with no fancy formatting, you can call
`str()` on a `BeautifulSoup` object, or on a [`Tag`](#Tag "Tag") within it:

```
str(soup)
# '<html><head></head><body><a href="http://example.com/">I linked to <i>example.com</i></a></body></html>'

str(soup.a)
# '<a href="http://example.com/">I linked to <i>example.com</i></a>'
```

The `str()` function returns a string encoded in UTF-8. See
[Encodings](#encodings) for other options.

You can also call `encode()` to get a bytestring, and `decode()`
to get Unicode.

## Output formatters

If you give Beautiful Soup a document that contains HTML entities like
"&lquot;", they'll be converted to Unicode characters:

```
soup = BeautifulSoup("&ldquo;Dammit!&rdquo; he said.", 'html.parser')
str(soup)
# '“Dammit!” he said.'
```

If you then convert the document to a bytestring, the Unicode characters
will be encoded as UTF-8. You won't get the HTML entities back:

```
soup.encode("utf8")
# b'\xe2\x80\x9cDammit!\xe2\x80\x9d he said.'
```

By default, the only characters that are escaped upon output are bare
ampersands and angle brackets. These get turned into "&amp;", "&lt;",
and "&gt;", so that Beautiful Soup doesn't inadvertently generate
invalid HTML or XML:

```
soup = BeautifulSoup("<p>The law firm of Dewey, Cheatem, & Howe</p>", 'html.parser')
soup.p
# <p>The law firm of Dewey, Cheatem, &amp; Howe</p>

soup = BeautifulSoup('<a href="http://example.com/?foo=val1&bar=val2">A link</a>', 'html.parser')
soup.a
# <a href="http://example.com/?foo=val1&amp;bar=val2">A link</a>
```

You can change this behavior by providing a value for the
`formatter` argument to `prettify()`, `encode()`, or
`decode()`. Beautiful Soup recognizes five possible values for
`formatter`.

The default is `formatter="minimal"`. Strings will only be processed
enough to ensure that Beautiful Soup generates valid HTML/XML:

```
french = "<p>Il a dit &lt;&lt;Sacr&eacute; bleu!&gt;&gt;</p>"
soup = BeautifulSoup(french, 'html.parser')
print(soup.prettify(formatter="minimal"))
# <p>
#  Il a dit &lt;&lt;Sacré bleu!&gt;&gt;
# </p>
```

If you pass in `formatter="html"`, Beautiful Soup will convert
Unicode characters to HTML entities whenever possible:

```
print(soup.prettify(formatter="html"))
# <p>
#  Il a dit &lt;&lt;Sacr&eacute; bleu!&gt;&gt;
# </p>
```

If you pass in `formatter="html5"`, it's similar to
`formatter="html"`, but Beautiful Soup will
omit the closing slash in HTML void tags like "br":

```
br = BeautifulSoup("<br>", 'html.parser').br

print(br.encode(formatter="html"))
# b'<br/>'

print(br.encode(formatter="html5"))
# b'<br>'
```

In addition, any attributes whose values are the empty string
will become HTML-style Boolean attributes:

```
option = BeautifulSoup('<option selected=""></option>').option
print(option.encode(formatter="html"))
# b'<option selected=""></option>'

print(option.encode(formatter="html5"))
# b'<option selected></option>'
```

*(This behavior is new as of Beautiful Soup 4.10.0.)*

If you pass in `formatter=None`, Beautiful Soup will not modify
strings at all on output. This is the fastest option, but it may lead
to Beautiful Soup generating invalid HTML/XML, as in these examples:

```
print(soup.prettify(formatter=None))
# <p>
#  Il a dit <<Sacré bleu!>>
# </p>

link_soup = BeautifulSoup('<a href="http://example.com/?foo=val1&bar=val2">A link</a>', 'html.parser')
print(link_soup.a.encode(formatter=None))
# b'<a href="http://example.com/?foo=val1&bar=val2">A link</a>'
```

### Formatter objects

If you need more sophisticated control over your output, you can
instantiate one of Beautiful Soup's formatter classes and pass that
object in as `formatter`.

*class*HTMLFormatter

Used to customize the formatting rules for HTML documents.

Here's a formatter that converts strings to uppercase, whether they
occur in a string object or an attribute value:

```
from bs4.formatter import HTMLFormatter
def uppercase(str):
    return str.upper()

formatter = HTMLFormatter(uppercase)

print(soup.prettify(formatter=formatter))
# <p>
#  IL A DIT <<SACRÉ BLEU!>>
# </p>

print(link_soup.a.prettify(formatter=formatter))
# <a href="HTTP://EXAMPLE.COM/?FOO=VAL1&BAR=VAL2">
#  A LINK
# </a>
```

Here's a formatter that increases the indentation width when pretty-printing:

```
formatter = HTMLFormatter(indent=8)
print(link_soup.a.prettify(formatter=formatter))
# <a href="http://example.com/?foo=val1&bar=val2">
#         A link
# </a>
```

*class*XMLFormatter

Used to customize the formatting rules for XML documents.

### Writing your own formatter

Subclassing [`HTMLFormatter`](#HTMLFormatter "HTMLFormatter") or [`XMLFormatter`](#XMLFormatter "XMLFormatter") will
give you even more control over the output. For example, Beautiful
Soup sorts the attributes in every tag by default:

```
attr_soup = BeautifulSoup(b'<p z="1" m="2" a="3"></p>', 'html.parser')
print(attr_soup.p.encode())
# <p a="3" m="2" z="1"></p>
```

To turn this off, you can subclass the `Formatter.attributes()`
method, which controls which attributes are output and in what
order. This implementation also filters out the attribute called "m"
whenever it appears:

```
class UnsortedAttributes(HTMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            if k == 'm':
                continue
            yield k, v

print(attr_soup.p.encode(formatter=UnsortedAttributes()))
# <p z="1" a="3"></p>
```

One last caveat: if you create a [`CData`](#CData "CData") object, the text inside
that object is always presented *exactly as it appears, with no
formatting*. Beautiful Soup will call your entity substitution
function, just in case you've written a custom function that counts
all the strings in the document or something, but it will ignore the
return value:

```
from bs4.element import CData
soup = BeautifulSoup("<a></a>", 'html.parser')
soup.a.string = CData("one < three")
print(soup.a.prettify(formatter="html"))
# <a>
#  <![CDATA[one < three]]>
# </a>
```

## `get_text()`

If you only want the human-readable text inside a document or tag, you can use the
`get_text()` method. It returns all the text in a document or
beneath a tag, as a single Unicode string:

```
markup = '<a href="http://example.com/">\nI linked to <i>example.com</i>\n</a>'
soup = BeautifulSoup(markup, 'html.parser')

soup.get_text()
'\nI linked to example.com\n'
soup.i.get_text()
'example.com'
```

You can specify a string to be used to join the bits of text
together:

```
# soup.get_text("|")
'\nI linked to |example.com|\n'
```

You can tell Beautiful Soup to strip whitespace from the beginning and
end of each bit of text:

```
# soup.get_text("|", strip=True)
'I linked to|example.com'
```

But at that point you might want to use the [.stripped\_strings](#string-generators)
generator instead, and process the text yourself:

```
[text for text in soup.stripped_strings]
# ['I linked to', 'example.com']
```

*As of Beautiful Soup version 4.9.0, when lxml or html.parser are in
use, the contents of <script>, <style>, and <template>
tags are generally not considered to be 'text', since those tags are not part of
the human-visible content of the page.*

*As of Beautiful Soup version 4.10.0, you can call get\_text(),
.strings, or .stripped\_strings on a NavigableString object. It will
either return the object itself, or nothing, so the only reason to do
this is when you're iterating over a mixed list.*

*As of Beautiful Soup version 4.13.0, you can call .string on a
NavigableString object. It will return the object itself, so again,
the only reason to do this is when you're iterating over a mixed
list.*

# Specifying the parser to use

If you just need to parse some HTML, you can dump the markup into the
`BeautifulSoup` constructor, and it'll probably be fine. Beautiful
Soup will pick a parser for you and parse the data. But there are a
few additional arguments you can pass in to the constructor to change
which parser is used.

The first argument to the `BeautifulSoup` constructor is a string or
an open filehandle—the source of the markup you want parsed. The second
argument is *how* you'd like the markup parsed.

If you don't specify anything, you'll get the best HTML parser that's
installed. Beautiful Soup ranks lxml's parser as being the best, then
html5lib's, then Python's built-in parser. You can override this by
specifying one of the following:

* What type of markup you want to parse. Currently supported values are
  "html", "xml", and "html5".
* The name of the parser library you want to use. Currently supported
  options are "lxml", "html5lib", and "html.parser" (Python's
  built-in HTML parser).

The section [Installing a parser](#installing-a-parser) contrasts the supported parsers.

If you ask for a parser that isn't installed, Beautiful Soup will
raise an exception so that you don't inadvertently parse a document
under an unknown set of rules. For example, right now, the only
supported XML parser is lxml. If you don't have lxml installed, asking
for an XML parser won't give you one, and asking for "lxml" won't work
either.

## Differences between parsers

Beautiful Soup presents the same interface to a number of different
parsers, but each parser is different. Different parsers will create
different parse trees from the same document. The biggest differences
are between the HTML parsers and the XML parsers. Here's a short
document, parsed as HTML using the parser that comes with Python:

```
BeautifulSoup("<a><b/></a>", "html.parser")
# <a><b></b></a>
```

Since a standalone <b/> tag is not valid HTML, html.parser turns it into
a <b></b> tag pair.

Here's the same document parsed as XML (running this requires that you
have lxml installed). Note that the standalone <b/> tag is left alone, and
that the document is given an XML declaration instead of being put
into an <html> tag.:

```
print(BeautifulSoup("<a><b/></a>", "xml"))
# <?xml version="1.0" encoding="utf-8"?>
# <a><b/></a>
```

There are also differences between HTML parsers. If you give Beautiful
Soup a perfectly-formed HTML document, these differences won't
matter. One parser will be faster than another, but they'll all give
you a data structure that looks exactly like the original HTML
document.

But if the document is not perfectly-formed, different parsers will
give different results. Here's a short, invalid document parsed using
lxml's HTML parser. Note that the <a> tag gets wrapped in <body> and
<html> tags, and the dangling </p> tag is simply ignored:

```
BeautifulSoup("<a></p>", "lxml")
# <html><body><a></a></body></html>
```

Here's the same document parsed using html5lib:

```
BeautifulSoup("<a></p>", "html5lib")
# <html><head></head><body><a><p></p></a></body></html>
```

Instead of ignoring the dangling </p> tag, html5lib pairs it with an
opening <p> tag. html5lib also adds an empty <head> tag; lxml didn't
bother.

Here's the same document parsed with Python's built-in HTML
parser:

```
BeautifulSoup("<a></p>", "html.parser")
# <a></a>
```

Like lxml, this parser ignores the closing </p> tag. Unlike
html5lib or lxml, this parser makes no attempt to create a
well-formed HTML document by adding <html> or <body> tags.

Since the document "<a></p>" is invalid, none of these techniques is
the 'correct' way to handle it. The html5lib parser uses techniques
that are part of the HTML5 standard, so it has the best claim on being
the 'correct' way, but all three techniques are legitimate.

Differences between parsers can affect your script. If you're planning
on distributing your script to other people, or running it on multiple
machines, you should specify a parser in the `BeautifulSoup`
constructor. That will reduce the chances that your users parse a
document differently from the way you parse it.

# Encodings

Any HTML or XML document is written in a specific encoding like ASCII
or UTF-8. But when you load that document into Beautiful Soup, you'll
discover it's been converted to Unicode:

```
markup = b"<h1>Sacr\xc3\xa9 bleu!</h1>"
soup = BeautifulSoup(markup, 'html.parser')
soup.h1
# <h1>Sacré bleu!</h1>
soup.h1.string
# 'Sacr\xe9 bleu!'
```

It's not magic. (That sure would be nice.) Beautiful Soup uses a
sub-library called [Unicode, Dammit](#unicode-dammit) to detect a document's encoding
and convert it to Unicode. The autodetected encoding is available as
the `.original_encoding` attribute of the `BeautifulSoup` object:

```
soup.original_encoding
# 'utf-8'
```

If `.original_encoding` is `None`, that means the document was
already Unicode when it was passed into Beautiful Soup:

```
markup = "<h1>Sacré bleu!</h1>"
soup = BeautifulSoup(markup, 'html.parser')
print(soup.original_encoding)
# None
```

Unicode, Dammit guesses correctly most of the time, but sometimes it
makes mistakes. Sometimes it guesses correctly, but only after a
byte-by-byte search of the document that takes a very long time. If
you happen to know a document's encoding ahead of time, you can avoid
mistakes and delays by passing it to the `BeautifulSoup` constructor
as `from_encoding`.

Here's a document written in ISO-8859-8. The document is so short that
Unicode, Dammit can't get a lock on it, and misidentifies it as
ISO-8859-7:

```
markup = b"<h1>\xed\xe5\xec\xf9</h1>"
soup = BeautifulSoup(markup, 'html.parser')
print(soup.h1)
# <h1>νεμω</h1>
print(soup.original_encoding)
# iso-8859-7
```

We can fix this by passing in the correct `from_encoding`:

```
soup = BeautifulSoup(markup, 'html.parser', from_encoding="iso-8859-8")
print(soup.h1)
# <h1>םולש</h1>
print(soup.original_encoding)
# iso8859-8
```

If you don't know what the correct encoding is, but you know that
Unicode, Dammit is guessing wrong, you can pass the wrong guesses in
as `exclude_encodings`:

```
soup = BeautifulSoup(markup, 'html.parser', exclude_encodings=["iso-8859-7"])
print(soup.h1)
# <h1>םולש</h1>
print(soup.original_encoding)
# WINDOWS-1255
```

Windows-1255 isn't 100% correct, but that encoding is a compatible
superset of ISO-8859-8, so it's close enough. (`exclude_encodings`
is a new feature in Beautiful Soup 4.4.0.)

In rare cases (usually when a UTF-8 document contains text written in
a completely different encoding), the only way to get Unicode may be
to replace some characters with the special Unicode character
"REPLACEMENT CHARACTER" (U+FFFD, �). If Unicode, Dammit needs to do
this, it will set the `.contains_replacement_characters` attribute
to `True` on the `UnicodeDammit` or `BeautifulSoup` object. This
lets you know that the Unicode representation is not an exact
representation of the original—some data was lost. If a document
contains �, but `.contains_replacement_characters` is `False`,
you'll know that the � was there originally (as it is in this
paragraph) and doesn't stand in for missing data.

## Output encoding

When you write out an output document from Beautiful Soup, you get a UTF-8
document, even if the input document wasn't in UTF-8 to begin with. Here's a
document written in the Latin-1 encoding:

```
markup = b'''
 <html>
  <head>
   <meta content="text/html; charset=ISO-Latin-1" http-equiv="Content-type" />
  </head>
  <body>
   <p>Sacr\xe9 bleu!</p>
  </body>
 </html>
'''

soup = BeautifulSoup(markup, 'html.parser')
print(soup.prettify())
# <html>
#  <head>
#   <meta content="text/html; charset=utf-8" http-equiv="Content-type" />
#  </head>
#  <body>
#   <p>
#    Sacré bleu!
#   </p>
#  </body>
# </html>
```

Note that the <meta> tag has been rewritten to reflect the fact that
the document is now in UTF-8.

If you don't want UTF-8, you can pass an encoding into `prettify()`:

```
print(soup.prettify("latin-1"))
# <html>
#  <head>
#   <meta content="text/html; charset=latin-1" http-equiv="Content-type" />
# ...
```

You can also call encode() on the `BeautifulSoup` object, or any
element in the soup, just as if it were a Python string:

```
soup.p.encode("latin-1")
# b'<p>Sacr\xe9 bleu!</p>'

soup.p.encode("utf-8")
# b'<p>Sacr\xc3\xa9 bleu!</p>'
```

Any characters that can't be represented in your chosen encoding will
be converted into numeric XML entity references. Here's a document
that includes the Unicode character SNOWMAN:

```
markup = u"<b>\N{SNOWMAN}</b>"
snowman_soup = BeautifulSoup(markup, 'html.parser')
tag = snowman_soup.b
```

The SNOWMAN character can be part of a UTF-8 document (it looks like
☃), but there's no representation for that character in ISO-Latin-1 or
ASCII, so it's converted into "&#9731" for those encodings:

```
print(tag.encode("utf-8"))
# b'<b>\xe2\x98\x83</b>'

print(tag.encode("latin-1"))
# b'<b>&#9731;</b>'

print(tag.encode("ascii"))
# b'<b>&#9731;</b>'
```

## Unicode, Dammit

You can use Unicode, Dammit without using Beautiful Soup. It's useful
whenever you have data in an unknown encoding and you just want it to
become Unicode:

```
from bs4 import UnicodeDammit
dammit = UnicodeDammit(b"\xc2\xabSacr\xc3\xa9 bleu!\xc2\xbb")
print(dammit.unicode_markup)
# «Sacré bleu!»
dammit.original_encoding
# 'utf-8'
```

Unicode, Dammit's guesses will get a lot more accurate if you install
one of these Python libraries: `charset-normalizer`, `chardet`, or
`cchardet`. The more data you give Unicode, Dammit, the more
accurately it will guess. If you have your own suspicions as to what
the encoding might be, you can pass them in as a list:

```
dammit = UnicodeDammit("Sacr\xe9 bleu!", ["latin-1", "iso-8859-1"])
print(dammit.unicode_markup)
# Sacré bleu!
dammit.original_encoding
# 'latin-1'
```

Unicode, Dammit has two special features that Beautiful Soup doesn't
use.

### Smart quotes

You can use Unicode, Dammit to convert Microsoft smart quotes to HTML or XML
entities:

```
markup = b"<p>I just \x93love\x94 Microsoft Word\x92s smart quotes</p>"

UnicodeDammit(markup, ["windows-1252"], smart_quotes_to="html").unicode_markup
# '<p>I just &ldquo;love&rdquo; Microsoft Word&rsquo;s smart quotes</p>'

UnicodeDammit(markup, ["windows-1252"], smart_quotes_to="xml").unicode_markup
# '<p>I just &#x201C;love&#x201D; Microsoft Word&#x2019;s smart quotes</p>'
```

You can also convert Microsoft smart quotes to ASCII quotes:

```
UnicodeDammit(markup, ["windows-1252"], smart_quotes_to="ascii").unicode_markup
# '<p>I just "love" Microsoft Word\'s smart quotes</p>'
```

Hopefully you'll find this feature useful, but Beautiful Soup doesn't
use it. Beautiful Soup prefers the default behavior, which is to
convert Microsoft smart quotes to Unicode characters along with
everything else:

```
UnicodeDammit(markup, ["windows-1252"]).unicode_markup
# '<p>I just “love” Microsoft Word’s smart quotes</p>'
```

### Inconsistent encodings

Sometimes a document is mostly in UTF-8, but contains Windows-1252
characters such as (again) Microsoft smart quotes. This can happen
when a website includes data from multiple sources. You can use
`UnicodeDammit.detwingle()` to turn such a document into pure
UTF-8. Here's a simple example:

```
snowmen = (u"\N{SNOWMAN}" * 3)
quote = (u"\N{LEFT DOUBLE QUOTATION MARK}I like snowmen!\N{RIGHT DOUBLE QUOTATION MARK}")
doc = snowmen.encode("utf8") + quote.encode("windows_1252")
```

This document is a mess. The snowmen are in UTF-8 and the quotes are
in Windows-1252. You can display the snowmen or the quotes, but not
both:

```
print(doc)
# ☃☃☃�I like snowmen!�

print(doc.decode("windows-1252"))
# â˜ƒâ˜ƒâ˜ƒ“I like snowmen!”
```

Decoding the document as UTF-8 raises a `UnicodeDecodeError`, and
decoding it as Windows-1252 gives you gibberish. Fortunately,
`UnicodeDammit.detwingle()` will convert the string to pure UTF-8,
allowing you to decode it to Unicode and display the snowmen and quote
marks simultaneously:

```
new_doc = UnicodeDammit.detwingle(doc)
print(new_doc.decode("utf8"))
# ☃☃☃“I like snowmen!”
```

`UnicodeDammit.detwingle()` only knows how to handle Windows-1252
embedded in UTF-8 (or vice versa, I suppose), but this is the most
common case.

Note that you must know to call `UnicodeDammit.detwingle()` on your
data before passing it into `BeautifulSoup` or the `UnicodeDammit`
constructor. Beautiful Soup assumes that a document has a single
encoding, whatever it might be. If you pass it a document that
contains both UTF-8 and Windows-1252, it's likely to think the whole
document is Windows-1252, and the document will come out looking like
`â˜ƒâ˜ƒâ˜ƒ“I like snowmen!”`.

`UnicodeDammit.detwingle()` is new in Beautiful Soup 4.1.0.

# Line numbers

The `html.parser` and `html5lib` parsers can keep track of where in
the original document each [`Tag`](#Tag "Tag") was found. You can access this
information as `Tag.sourceline` (line number) and `Tag.sourcepos`
(position of the start tag within a line):

Note that the two parsers mean slightly different things by
`sourcepos`. For html.parser, `sourcepos` points to the first character of the
opening tag:

```
markup = '<p class="1"\n>Paragraph 1</p>\n    <p class="2">Paragraph 2</p>'
print(markup)
# Line 1: <p class="1"
# Line 2: >Paragraph 1</p>
# Line 3:     <p class="2">Paragraph 2</p>

soup = BeautifulSoup(markup, 'html.parser')
for tag in soup.find_all('p'):
    print(repr((tag.sourceline, tag.sourcepos, tag.string)))
# (1, 0, 'Paragraph 1') # The < just before p class="1"
# (3, 4, 'Paragraph 2') # The < just before p class="2"
```

For html5lib, `sourcepos` points to the *final* character of the
opening tag:

```
print(markup)
# Line 1: <p class="1"
# Line 2: >Paragraph 1</p>
# Line 3:     <p class="2">Paragraph 2</p>

soup = BeautifulSoup(markup, 'html5lib')
for tag in soup.find_all('p'):
    print(repr((tag.sourceline, tag.sourcepos, tag.string)))
# (2, 0, 'Paragraph 1') # The > just before Paragraph 1
# (3, 16, 'Paragraph 2') # The > just before Paragraph 2
```

You can shut off this feature by passing `store_line_numbers=False`
into the `BeautifulSoup` constructor:

```
markup = "<p\n>Paragraph 1</p>\n    <p>Paragraph 2</p>"
soup = BeautifulSoup(markup, 'html.parser', store_line_numbers=False)
print(soup.p.sourceline)
# None
```

*This feature is new in 4.8.1, and the parsers based on lxml don't
support it.*

# Comparing objects for equality

Beautiful Soup says that two [`NavigableString`](#NavigableString "NavigableString") or [`Tag`](#Tag "Tag") objects
are equal when they represent the same HTML or XML markup, even if their
attributes are in a different order or they live in different parts of the
object tree. In this example, the two <b> tags are treated as equal, because
they both look like "<b>pizza</b>":

```
markup = "<p>I want <b>pizza</b> and more <b>pizza</b>!</p>"
soup = BeautifulSoup(markup, 'html.parser')
first_b, second_b = soup.find_all('b')
print(first_b == second_b)
# True

print(first_b.previous_element == second_b.previous_element)
# False
```

If you want to see whether two variables refer to exactly the same
object, use *is*:

```
print(first_b is second_b)
# False
```

# Copying Beautiful Soup objects

You can use `copy.copy()` to create a copy of any [`Tag`](#Tag "Tag") or
[`NavigableString`](#NavigableString "NavigableString"):

```
import copy
p_copy = copy.copy(soup.p)
print(p_copy)
# <p>I want <b>pizza</b> and more <b>pizza</b>!</p>
```

The copy is considered equal to the original, since it represents the
same markup as the original, but it's not the same object:

```
print(soup.p == p_copy)
# True

print(soup.p is p_copy)
# False
```

The only real difference is that the copy is completely detached from
the original Beautiful Soup object tree, just as if `extract()` had
been called on it. This is because two different [`Tag`](#Tag "Tag")
objects can't occupy the same space at the same time.

> ```
> print(p_copy.parent)
> # None
> ```

You can use `Tag.copy_self()` to create a copy of a
[`Tag`](#Tag "Tag") without copying its contents.

> ```
> original = BeautifulSoup('<a id="a_tag" class="link">the <i>link</i></a>', 'html.parser')
> print(original.a)
> # <a class="link" id="a_tag">the <i>link</a>
> print(original.a.copy_self())
> # <a class="link" id="a_tag"></a>
> ```

*(Tag.copy\_self() is introduced in Beautiful Soup 4.13.0.)*

# Advanced parser customization

Beautiful Soup offers a number of ways to customize how the parser
treats incoming HTML and XML. This section covers the most commonly
used customization techniques.

## Parsing only part of a document

Let's say you want to use Beautiful Soup to look at a document's <a>
tags. It's a waste of time and memory to parse the entire document and
then go over it again looking for <a> tags. It would be much faster to
ignore everything that wasn't an <a> tag in the first place. The
[`SoupStrainer`](#SoupStrainer "SoupStrainer") class allows you to choose which parts of an incoming
document are parsed. You just create a [`SoupStrainer`](#SoupStrainer "SoupStrainer") and pass it in
to the `BeautifulSoup` constructor as the `parse_only` argument.

(Note that *this feature won't work if you're using the html5lib parser*.
If you use html5lib, the whole document will be parsed, no
matter what. This is because html5lib constantly rearranges the parse
tree as it works, and if some part of the document didn't actually
make it into the parse tree, it'll crash. To avoid confusion, in the
examples below I'll be forcing Beautiful Soup to use Python's
built-in parser.)

*class*SoupStrainer

The [`SoupStrainer`](#SoupStrainer "SoupStrainer") class takes the same arguments as a typical
method from [Searching the tree](#searching-the-tree): [name](#name), [attrs](#attrs), [string](#id11), and [\*\*kwargs](#kwargs). Here are
three [`SoupStrainer`](#SoupStrainer "SoupStrainer") objects:

```
from bs4 import SoupStrainer

only_a_tags = SoupStrainer("a")

only_tags_with_id_link2 = SoupStrainer(id="link2")

def is_short_string(string):
    return string is not None and len(string) < 10

only_short_strings = SoupStrainer(string=is_short_string)
```

I'm going to bring back the "three sisters" document one more time,
and we'll see what the document looks like when it's parsed with these
three [`SoupStrainer`](#SoupStrainer "SoupStrainer") objects:

```
html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

print(BeautifulSoup(html_doc, "html.parser", parse_only=only_a_tags).prettify())
# <a class="sister" href="http://example.com/elsie" id="link1">
#  Elsie
# </a>
# <a class="sister" href="http://example.com/lacie" id="link2">
#  Lacie
# </a>
# <a class="sister" href="http://example.com/tillie" id="link3">
#  Tillie
# </a>

print(BeautifulSoup(html_doc, "html.parser", parse_only=only_tags_with_id_link2).prettify())
# <a class="sister" href="http://example.com/lacie" id="link2">
#  Lacie
# </a>

print(BeautifulSoup(html_doc, "html.parser", parse_only=only_short_strings).prettify())
# Elsie
# ,
# Lacie
# and
# Tillie
# ...
#
```

When selectively parsing a document, the behavior of [`SoupStrainer`](#SoupStrainer "SoupStrainer") is as follows:

* When the name and attributes for a potential tag matches the
  [`SoupStrainer`](#SoupStrainer "SoupStrainer"), the tag is parsed. All of its
  children are automatically parsed, without the
  [`SoupStrainer`](#SoupStrainer "SoupStrainer") being consulted.
* When the name and attributes for a potential tag do not match, the tag is
  not parsed. But its children will be compared against the
  [`SoupStrainer`](#SoupStrainer "SoupStrainer") and may end up being parsed.
* The tag names and attribute values passed in to the
  [`SoupStrainer`](#SoupStrainer "SoupStrainer") are the same ones that would be passed into
  the [`Tag`](#Tag "Tag") constructor. These values will be in a less
  processed form here than in other parts of Beautiful Soup. In particular,
  attribute values are always passed in as Unicode strings, even if (as with
  the [`class`](https://docs.python.org/3/glossary.html#term-class "(in Python v3.14)") attribute in HTML) that value would become a list after parsing.

## Customizing multi-valued attributes

In an HTML document, an attribute like `class` is given a list of
values, and an attribute like `id` is given a single value, because
the HTML specification treats those attributes differently:

```
markup = '<a class="cls1 cls2" id="id1 id2">'
soup = BeautifulSoup(markup, 'html.parser')
soup.a['class']
# ['cls1', 'cls2']
soup.a['id']
# 'id1 id2'
```

You can turn this off by passing in
`multi_valued_attributes=None`. Than all attributes will be given a
single value:

```
soup = BeautifulSoup(markup, 'html.parser', multi_valued_attributes=None)
soup.a['class']
# 'cls1 cls2'
soup.a['id']
# 'id1 id2'
```

You can customize this behavior quite a bit by passing in a
dictionary for `multi_valued_attributes`. If you need this, look at
`HTMLTreeBuilder.DEFAULT_CDATA_LIST_ATTRIBUTES` to see the
configuration Beautiful Soup uses by default, which is based on the
HTML specification.

*(This is a new feature in Beautiful Soup 4.8.0.)*

## Handling duplicate attributes

When using the `html.parser` parser, you can use the
`on_duplicate_attribute` constructor argument to customize what
Beautiful Soup does when it encounters a tag that defines the same
attribute more than once:

```
markup = '<a href="http://url1/" href="http://url2/">'
```

The default behavior is to use the last value found for the tag:

```
soup = BeautifulSoup(markup, 'html.parser')
soup.a['href']
# http://url2/

soup = BeautifulSoup(markup, 'html.parser', on_duplicate_attribute='replace')
soup.a['href']
# http://url2/
```

With `on_duplicate_attribute='ignore'` you can tell Beautiful Soup
to use the *first* value found and ignore the rest:

```
soup = BeautifulSoup(markup, 'html.parser', on_duplicate_attribute='ignore')
soup.a['href']
# http://url1/
```

(lxml and html5lib always do it this way; their behavior can't be
configured from within Beautiful Soup.)

If you need more control, you can pass in a function that's called on each
duplicate value:

```
def accumulate(attributes_so_far, key, value):
    if not isinstance(attributes_so_far[key], list):
        attributes_so_far[key] = [attributes_so_far[key]]
    attributes_so_far[key].append(value)

soup = BeautifulSoup(markup, 'html.parser', on_duplicate_attribute=accumulate)
soup.a['href']
# ["http://url1/", "http://url2/"]
```

*(This is a new feature in Beautiful Soup 4.9.1.)*

## Instantiating custom subclasses

When a parser tells Beautiful Soup about a tag or a string, Beautiful
Soup will instantiate a [`Tag`](#Tag "Tag") or [`NavigableString`](#NavigableString "NavigableString") object to
contain that information. Instead of that default behavior, you can
tell Beautiful Soup to instantiate *subclasses* of [`Tag`](#Tag "Tag") or
[`NavigableString`](#NavigableString "NavigableString"), subclasses you define with custom behavior:

```
from bs4 import Tag, NavigableString
class MyTag(Tag):
    pass

class MyString(NavigableString):
    pass

markup = "<div>some text</div>"
soup = BeautifulSoup(markup, 'html.parser')
isinstance(soup.div, MyTag)
# False
isinstance(soup.div.string, MyString)
# False

my_classes = { Tag: MyTag, NavigableString: MyString }
soup = BeautifulSoup(markup, 'html.parser', element_classes=my_classes)
isinstance(soup.div, MyTag)
# True
isinstance(soup.div.string, MyString)
# True
```

This can be useful when incorporating Beautiful Soup into a test
framework.

*(This is a new feature in Beautiful Soup 4.8.1.)*

# Troubleshooting

## `diagnose()`

If you're having trouble understanding what Beautiful Soup does to a
document, pass the document into the `diagnose()` function. (This function is new in
Beautiful Soup 4.2.0.) Beautiful Soup will print out a report showing
you how different parsers handle the document, and tell you if you're
missing a parser that Beautiful Soup could be using:

```
from bs4.diagnose import diagnose
with open("bad.html") as fp:
    data = fp.read()

diagnose(data)

# Diagnostic running on Beautiful Soup 4.2.0
# Python version 2.7.3 (default, Aug  1 2012, 05:16:07)
# I noticed that html5lib is not installed. Installing it may help.
# Found lxml version 2.3.2.0
#
# Trying to parse your data with html.parser
# Here's what html.parser did with the document:
# ...
```

Just looking at the output of diagnose() might show you how to solve the
problem. Even if not, you can paste the output of `diagnose()` when
asking for help.

## Errors when parsing a document

There are two different kinds of parse errors. There are crashes,
where you feed a document to Beautiful Soup and it raises an
exception (usually an `HTMLParser.HTMLParseError`). And there is
unexpected behavior, where a Beautiful Soup parse tree looks a lot
different than the document used to create it.

These problems are almost never problems with Beautiful Soup itself.
This is not because Beautiful Soup is an amazingly well-written piece
of software. It's because Beautiful Soup doesn't include any parsing
code. Instead, it relies on external parsers. If one parser isn't
working on a certain document, the best solution is to try a different
parser. See [Installing a parser](#installing-a-parser) for details and a parser
comparison. If this doesn't help, you might need to inspect the
document tree found inside the `BeautifulSoup` object, to see where
the markup you're looking for actually ended up.

## Version mismatch problems

* `SyntaxError: Invalid syntax` (on the line `ROOT_TAG_NAME =
  '[document]'`): Caused by running an old Python 2 version of
  Beautiful Soup under Python 3, without converting the code.
* `ImportError: No module named HTMLParser` - Caused by running an old
  Python 2 version of Beautiful Soup under Python 3.
* `ImportError: No module named html.parser` - Caused by running the
  Python 3 version of Beautiful Soup under Python 2.
* `ImportError: No module named BeautifulSoup` - Caused by running
  Beautiful Soup 3 code in an environment that doesn't have BS3
  installed. Or, by writing Beautiful Soup 4 code without knowing that
  the package name has changed to `bs4`.
* `ImportError: No module named bs4` - Caused by running Beautiful
  Soup 4 code in an environment that doesn't have BS4 installed.

## Parsing XML

By default, Beautiful Soup parses documents as HTML. To parse a
document as XML, pass in "xml" as the second argument to the
`BeautifulSoup` constructor:

```
soup = BeautifulSoup(markup, "xml")
```

You'll need to [have lxml installed](#parser-installation).

## Other parser problems

* If your script works on one computer but not another, or in one
  virtual environment but not another, or outside the virtual
  environment but not inside, it's probably because the two
  environments have different parser libraries available. For example,
  you may have developed the script on a computer that has lxml
  installed, and then tried to run it on a computer that only has
  html5lib installed. See [Differences between parsers](#differences-between-parsers) for why this
  matters, and fix the problem by mentioning a specific parser library
  in the `BeautifulSoup` constructor.
* Because [HTML tags and attributes are case-insensitive](http://www.w3.org/TR/html5/syntax.html#syntax), all three HTML
  parsers convert tag and attribute names to lowercase. That is, the
  markup <TAG></TAG> is converted to <tag></tag>. If you want to
  preserve mixed-case or uppercase tags and attributes, you'll need to
  [parse the document as XML.](#parsing-xml)

## Miscellaneous

* `UnicodeEncodeError: 'charmap' codec can't encode character
  '\xfoo' in position bar` (or just about any other
  `UnicodeEncodeError`) - This problem shows up in two main
  situations. First, when you try to print a Unicode character that
  your console doesn't know how to display. (See [this page on the
  Python wiki](http://wiki.python.org/moin/PrintFails) for help.)
  Second, when you're writing to a file and you pass in a Unicode
  character that's not supported by your default encoding. In this
  case, the simplest solution is to explicitly encode the Unicode
  string into UTF-8 with `u.encode("utf8")`.
* `KeyError: [attr]` - Caused by accessing `tag['attr']` when the
  tag in question doesn't define the `attr` attribute. The most
  common errors are `KeyError: 'href'` and `KeyError: 'class'`.
  Use `tag.get('attr')` if you're not sure `attr` is
  defined, just as you would with a Python dictionary.
* `AttributeError: 'ResultSet' object has no attribute 'foo'` - This
  usually happens because you expected `find_all()` to return a
  single tag or string. But `find_all()` returns a *list* of tags
  and strings—a `ResultSet` object. You need to iterate over the
  list and look at the `.foo` of each one. Or, if you really only
  want one result, you need to use `find()` instead of
  `find_all()`.
* `AttributeError: 'NoneType' object has no attribute 'foo'` - This
  usually happens because you called `find()` and then tried to
  access the `.foo` attribute of the result. But in your case,
  `find()` didn't find anything, so it returned `None`, instead of
  returning a tag or a string. You need to figure out why your
  `find()` call isn't returning anything.
* `AttributeError: 'NavigableString' object has no attribute
  'foo'` - This usually happens because you're treating a string as
  though it were a tag. You may be iterating over a list, expecting
  that it contains nothing but tags, when it actually contains both tags and
  strings.

## Improving Performance

Beautiful Soup will never be as fast as the parsers it sits on top
of. If response time is critical, if you're paying for computer time
by the hour, or if there's any other reason why computer time is more
valuable than programmer time, you should forget about Beautiful Soup
and work directly atop [lxml](http://lxml.de/).

That said, there are things you can do to speed up Beautiful Soup. If
you're not using lxml as the underlying parser, my advice is to
[start](#parser-installation). Beautiful Soup parses documents
significantly faster using lxml than using html.parser or html5lib.

You can speed up encoding detection significantly by installing the
[cchardet](http://pypi.python.org/pypi/cchardet/) library.

[Parsing only part of a document](#parsing-only-part-of-a-document) won't save you much time parsing
the document, but it can save a lot of memory, and it'll make
*searching* the document much faster.

# Translating this documentation

New translations of the Beautiful Soup documentation are greatly
appreciated. Translations should be licensed under the MIT license,
just like Beautiful Soup and its English documentation are.

There are two ways of getting your translation into the main code base
and onto the Beautiful Soup website:

1. Create a branch of the Beautiful Soup repository, add your
   translation, and propose a merge with the main branch, the same
   as you would do with a proposed change to the source code.
2. Send a message to the Beautiful Soup discussion group with a link to
   your translation, or attach your translation to the message.

Use the Chinese or Brazilian Portuguese translations as your model. In
particular, please translate the source file `doc/index.rst`,
rather than the HTML version of the documentation. This makes it
possible to publish the documentation in a variety of formats, not
just HTML.

# Beautiful Soup 3

Beautiful Soup 3 is the previous release series, and is no longer
supported. Development of Beautiful Soup 3 stopped in 2012, and the
package was completely discontinued in 2021. There's no reason to
install it unless you're trying to get very old software to work, but
it's published through PyPi as `BeautifulSoup`:

`$ pip install BeautifulSoup`

You can also download [a tarball of the final release, 3.2.2](https://www.crummy.com/software/BeautifulSoup/download/3.x/BeautifulSoup-3.2.2.tar.gz).

If you ran `pip install beautifulsoup` or `pip install
BeautifulSoup`, but your code doesn't work, you installed Beautiful
Soup 3 by mistake. You need to run `pip install beautifulsoup4`.

[The documentation for Beautiful Soup 3 is archived online](http://www.crummy.com/software/BeautifulSoup/bs3/documentation.html).

## Porting code to BS4

Most code written against Beautiful Soup 3 will work against Beautiful
Soup 4 with one simple change. All you should have to do is change the
package name from `BeautifulSoup` to `bs4`. So this:

```
from BeautifulSoup import BeautifulSoup
```

becomes this:

```
from bs4 import BeautifulSoup
```

* If you get the `ImportError` "No module named BeautifulSoup", your
  problem is that you're trying to run Beautiful Soup 3 code, but you
  only have Beautiful Soup 4 installed.
* If you get the `ImportError` "No module named bs4", your problem
  is that you're trying to run Beautiful Soup 4 code, but you only
  have Beautiful Soup 3 installed.

Although BS4 is mostly backward-compatible with BS3, most of its
methods have been deprecated and given new names for [PEP 8 compliance](http://www.python.org/dev/peps/pep-0008/). There are numerous other
renames and changes, and a few of them break backward compatibility.

Here's what you'll need to know to convert your BS3 code and habits to BS4:

### You need a parser

Beautiful Soup 3 used Python's `SGMLParser`, a module that was
deprecated and removed in Python 3.0. Beautiful Soup 4 uses
`html.parser` by default, but you can plug in lxml or html5lib and
use that instead. See [Installing a parser](#installing-a-parser) for a comparison.

Since `html.parser` is not the same parser as `SGMLParser`, you
may find that Beautiful Soup 4 gives you a different parse tree than
Beautiful Soup 3 for the same markup. If you swap out `html.parser`
for lxml or html5lib, you may find that the parse tree changes yet
again. If this happens, you'll need to update your scraping code to
process the new tree.

### Property names

I renamed three attributes to avoid using words that have special
meaning to Python. Unlike my changes to method names (which you'll see
in the form of deprecation warnings), these changes *did not
preserve backwards compatibility.* If you used these attributes in
BS3, your code will break in BS4 until you change them.

* `UnicodeDammit.unicode` -> `UnicodeDammit.unicode_markup`
* `Tag.next` -> `Tag.next_element`
* `Tag.previous` -> `Tag.previous_element`

### Generators

Some of the generators used to yield `None` after they were done, and
then stop. That was a bug. Now the generators just stop.

### XML

There is no longer a `BeautifulStoneSoup` class for parsing XML. To
parse XML you pass in "xml" as the second argument to the
`BeautifulSoup` constructor. For the same reason, the
`BeautifulSoup` constructor no longer recognizes the `isHTML`
argument.

Beautiful Soup's handling of empty-element XML tags has been
improved. Previously when you parsed XML you had to explicitly say
which tags were considered empty-element tags. The `selfClosingTags`
argument to the constructor is no longer recognized. Instead,
Beautiful Soup considers any empty tag to be an empty-element tag. If
you add a child to an empty-element tag, it stops being an
empty-element tag.

### Entities

An incoming HTML or XML entity is always converted into the
corresponding Unicode character. Beautiful Soup 3 had a number of
overlapping ways of dealing with entities, which have been
removed. The `BeautifulSoup` constructor no longer recognizes the
`smartQuotesTo` or `convertEntities` arguments. ([Unicode,
Dammit](#unicode-dammit) still has `smart_quotes_to`, but its default is now to turn
smart quotes into Unicode.) The constants `HTML_ENTITIES`,
`XML_ENTITIES`, and `XHTML_ENTITIES` have been removed, since they
configure a feature (transforming some but not all entities into
Unicode characters) that no longer exists.

If you want to turn Unicode characters back into HTML entities on
output, rather than turning them into UTF-8 characters, you need to
use an [output formatter](#output-formatters).

### Miscellaneous

[Tag.string](#string) now operates recursively. If tag A
contains a single tag B and nothing else, then A.string is the same as
B.string. (Previously, it was None.)

[Multi-valued attributes](#multi-valued-attributes) like `class` have lists of strings as
their values, not simple strings. This may affect the way you search by CSS
class.

[`Tag`](#Tag "Tag") objects now implement the `__hash__` method, such that two
[`Tag`](#Tag "Tag") objects are considered equal if they generate the same
markup. This may change your script's behavior if you put [`Tag`](#Tag "Tag")
objects into a dictionary or set.

If you pass one of the `find*` methods both [string](#id11) *and*
a tag-specific argument like [name](#name), Beautiful Soup will
search for tags that match your tag-specific criteria and whose
[Tag.string](#string) matches your [string](#id11)
value. It will *not* find the strings themselves. Previously,
Beautiful Soup ignored the tag-specific arguments and looked for
strings.

The `BeautifulSoup` constructor no longer recognizes the
`markupMassage` argument. It's now the parser's responsibility to
handle markup correctly.

The rarely-used alternate parser classes like
`ICantBelieveItsBeautifulSoup` and `BeautifulSOAP` have been
removed. It's now the parser's decision how to handle ambiguous
markup.

The `prettify()` method now returns a Unicode string, not a bytestring.

---

## Bibliography

1. [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)