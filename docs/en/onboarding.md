# Onboarding

Wondering how this project works? This document explains the technologies,
common patterns, and workflows involved in developing it.

- [Onboarding](#onboarding)
  - [Project Summary](#project-summary)
    - [gettext](#gettext)
    - [Python](#python)
    - [discord.py](#discordpy)
  - [gettext workflow](#gettext-workflow)
    - [Creating a .pot (Portable Object Template) file from a project](#creating-a-pot-portable-object-template-file-from-a-project)
    - [Creating a .po (Portable Object) localization](#creating-a-po-portable-object-localization)
    - [Organizing PO files for gettext](#organizing-po-files-for-gettext)
    - [Creating a .mo (Machine Object) compiled localization](#creating-a-mo-machine-object-compiled-localization)
    - [Updating .po/.pot files after generation](#updating-popot-files-after-generation)
    - [Adding extracted comments to provide context](#adding-extracted-comments-to-provide-context)
  - [Glossary](#glossary)

## Project Summary

This project is written as a Python package, intended to be installed
into a Python environment before execution. It uses the built-in
[Python gettext module](https://docs.python.org/3/library/gettext.html)
to perform translations, and [discord.py](#discordpy)
to login and register application commands on Discord.

### gettext

[gettext](https://en.wikipedia.org/wiki/Gettext) refers to a set of utilities
written as part of the GNU Project, designed to help programs support
[internationalization/i18n] and [localization/L10n].
Translations are written by hand, often with the help of someone else,
and can be changed at runtime without the need to re-compile a program.
The gettext file formats are language-agnostic so anyone can help translate
your program without having any programming knowledge.

On Linux, gettext is usually available through your package manager.

On Windows, gettext utilities can be provided by the [Git for Windows](https://git-scm.com/download/)
distribution, either by:

1. using the gettext utilities within [Git Bash](https://www.atlassian.com/git/tutorials/git-bash),
   or;
2. enabling the "Use Git and optional Unix tools from the Command Prompt"
   option during installation to have access to them in the regular Windows
   terminals.

> [!NOTE]
>
> For Windows users, you may notice some warnings when running gettext programs
> mentioning that there are files missing in `/usr/share`:
>
> ```sh
> sh: /usr/share/gettext/projects/team-address: No such file or directory
> msginit: /usr/share/gettext/projects/team-address subprocess failed
> msginit: /usr/share/gettext/projects/team-address subprocess failed with exit code 127
> ```
>
> This is not critical to gettext's operation, but you may choose to fix this
> by installing the [Git for Windows SDK](https://gitforwindows.org/)
> and then running `pacman -S gettext-devel` to install the rest of its files
> (see also [Package Management](https://www.msys2.org/docs/package-management/)).

You can read more about gettext on the [GNU website](https://www.gnu.org/software/gettext/).

### Python

[Python](https://www.python.org/) is a general-purpose, dynamically typed language
with a syntax designed to be easier for humans to read.
You can learn more about Python in their [official documentation](https://docs.python.org/).
This project uses Python [3.11](https://docs.python.org/3/whatsnew/3.11.html)
which was released on October 2022 and is being maintained until October 2027.

Since there are dependencies and MO file compilations involved, this project
is set up as a package to make these steps automatic with one install command.
Python packages
(or more specifically [distribution packages](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package))
are there to help share code across users while automating any necessary setup,
such as compiling C extensions and installing other package dependencies.

When you install packages with Python, they go to a common location known
as your `site-packages`. Python will look through this directory to find
your packages so you can [import](https://docs.python.org/3/tutorial/modules.html)
them from anywhere in your scripts.
Ideally however, you should create a virtual environment for every project
so your packages are isolated to that project, preventing dependencies
from conflicting with each other and having an overall mess in your global
`site-packages`.
You can learn more about this in [one of the PyPA guides](https://packaging.python.org/en/latest/tutorials/installing-packages/).

### discord.py

discord.py is a Python library that wraps the Discord API and Gateway,
allowing succinct programs that can interact with the Discord social platform.
discord.py's [official documentation](https://discordpy.readthedocs.io/)
and [GitHub repository](https://github.com/Rapptz/discord.py)
are the most up-to-date resources to learn how the library works.

To run this project, you must have a bot account created, joined on a server,
and the bot token added to a [config.toml](/src/dpygt/config_default.toml)
file in your current directory.
See step 1 in the [official Getting Started guide](https://discord.com/developers/docs/getting-started#step-1-creating-an-app)
to complete this.
No privileged gateway intents are required, but you are free to enable them.

## gettext workflow

### Creating a .pot (Portable Object Template) file from a project

A POT file contains all the strings in the source code that have been marked
as translatable, along with some common metadata like the project version
and copyright. It by itself does not handle translation, but it can be
used to create PO files which contain translations for a single [locale].

The `xgettext` utility is used to scan your source code files to extract
strings. This is done by looking for keywords, typically a function name
like `gettext`, followed by a set of parentheses with arguments, one or
more of which contain strings:

```py
from gettext import gettext as _

def main():
    translatable_string = _("Hello world!")
    print(translatable_string)
```

A default set of keywords are defined for several programming languages
as listed [in the manual](https://www.gnu.org/software/gettext/manual/gettext.html#index-_002dk_002c-xgettext-option).
For Python, `xgettext` checks for `*gettext()` functions and the additional
`_()` shorthand which programmers can alias to any function they want,
usually `gettext()`.
In the case of discord.py, `discord.app_commands.locale_str` marks strings
that can be localized when synchronizing application commands with Discord,
so this project often aliases it to `_`.
You can also define your own keywords using the
[`-k/--keyword`](https://www.gnu.org/software/gettext/manual/gettext.html#index-_002dk_002c-xgettext-option)
option if you prefer having multiple shorthands available.

To create the .pot, start by running `xgettext src/dpygt/**/*.py`. xgettext
will scan the given Python files and generate a resulting `messages.po` file.
You can then rename it to the `dpygt` [domain] + `.pot` extension,
edit the title/copyright header, and place it at `src/dpygt/dpygt.pot`.

Make sure you also change the `Content-Type` charset to `UTF-8` since the
[Python gettext module](https://docs.python.org/3/library/gettext.html)
will later rely on it to determine the translation file's encoding.

Additional resources:
- [`*` glob syntax](https://en.wikipedia.org/wiki/Glob_(programming))
- [GNU xgettext](https://www.gnu.org/software/gettext/manual/gettext.html#Making-the-PO-Template-File)

### Creating a .po (Portable Object) localization

To begin writing translations for a particular [locale], you should run
`msginit -i src/dpygt/dpygt.pot -l <locale>` to generate a new PO file
from the template, resulting in `<locale>.po`.
`<locale>` should define the language code + optional country code
in the form LL_CC, for example `en_US`.
Adjust the PO file's metadata like `Last-Translator` as necessary before you
start writing translations for messages.

> [!NOTE]
> For this project we are limited to the
> [locales supported by Discord](https://discord.com/developers/docs/reference#locales).

The PO format is explained in the [GNU manual](https://www.gnu.org/software/gettext/manual/gettext.html#The-Format-of-PO-Files)
and it is important to understand when editing it by hand.
However, there are also graphical interfaces for editing PO files like
[Lokalize](https://userbase.kde.org/Lokalize),
[Poedit](https://poedit.net/),
and [Virtaal](https://virtaal.translatehouse.org/)
which help you ensure your changes use valid and conventional syntax.

Additional resources:
- [-l/--locale option format](https://www.gnu.org/software/gettext/manual/gettext.html#index-_002dl_002c-msginit-option)
- [ISO 639-1 language codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
- [ISO 3166-1 alpha-2 country codes](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
- [PO Editors](https://www.gnu.org/software/trans-coord/manual/web-trans/html_node/PO-Editors.html)

### Organizing PO files for gettext

The [Python gettext module](https://docs.python.org/3/library/gettext.html#gettext.bindtextdomain)
requires us to define a directory containing the localizations.
For this project, that has been set to [src/dpygt/locales/](/src/dpygt/locales/).
Within this directory, localizations are further categorized into
`<language>/<category>/<domain>.po`, where `<language>` is the [locale] code,
`<category>` is the locale category (always LC_MESSAGES for gettext),
and `<domain>` is the [domain] name. For example, a Japanese localization
of this project should be defined as `locales/ja/LC_MESSAGES/dpygt.po`.

In reality, this file structure is intended for MO files, not PO files.
However for convenience, this project expects all PO files to reside in
the same directories as their MO file outputs.

### Creating a .mo (Machine Object) compiled localization

Before translations in PO files can be used, they must be compiled into MO files,
which are cross-platform binary formats designed for optimized lookups of translations.

To create a MO file from a PO file, you can use `msgfmt -o <domain>.mo <domain>.po`.
Some GUI editors may do this for you, but otherwise it has to be done for each PO file
which can get tedious. As such, this project provides two utilities for this:

- [utils/build_mo.py](/utils/build_mo.py):
  This is a very simple Python script that invokes msgfmt on all PO files
  found within the src/ directory.
  It is intended to be executed from the project root.

- [setup.py](/setup.py):
  This is used by the [setuptools](https://setuptools.pypa.io/) build system
  and implements a subcommand which replaces all PO files with MO equivalents
  when building the package (editable installs excepted).
  In other words the [sdist] only includes the PO files, but once the [wheel]
  is built from it, only MO files will be present.

[sdist]: https://packaging.python.org/en/latest/flow/#build-artifacts
[wheel]: https://packaging.python.org/en/latest/flow/#build-artifacts

It is debatable whether MO files should be part of the repository
or only exist as build artifacts.
This project prefers that MO files are not included in version control because
they increase the repository size and can lead to inconsistent translations
with their respective PO files.
This however means that users installing from source cannot compile PO files
if they are missing the `msgfmt` utility.

### Updating .po/.pot files after generation

As the source code changes, strings may be added or removed, and source file
references will become obsolete. To help maintain PO/POT files, the `msgmerge`
utility can be used to merge two PO files, such as one freshly generated from
`xgettext`. For example to update `current.po` in-place with `new.pot`, you
can run `msgmerge current.po new.pot -o current.po`.

For strings that have changed, `msgmerge` attempts to match them to their
previous revision and if successful, marks them as
[fuzzy](https://www.gnu.org/software/gettext/manual/gettext.html#index-fuzzy-flag):

```po
#: src/dpygt/cogs/random.py:18
#, fuzzy
msgid "roll-dice"
msgstr "lancer"
```

When compiling MO files, fuzzy entries are omitted unless the
[`-f/--use-fuzzy`](https://www.gnu.org/software/gettext/manual/gettext.html#index-_002df_002c-msgfmt-option)
is specified. Translators should review fuzzy strings and update
their translations if necessary before deleting the fuzzy flag.

When a string no longer appears in the source code, `msgmerge` will mark
their localizations as obsolete with `#~` and may be discarded by translators.

Similar to `msgfmt`, GUI editors may provide a utility command for merging
PO files, but otherwise `msgmerge` has to be ran on each PO/POT file, making
it tedious to use. Instead, the [utils/merge_po.py](/utils/merge_po.py) script
can be used to generate a PO file from source and merge them to all existing
PO/POT files.

Additional resources:
- [GNU msgmerge](https://www.gnu.org/software/gettext/manual/gettext.html#msgmerge-Invocation)

### Adding extracted comments to provide context

Translators find it easier to provide an appropriate localization when
they know the context of each message being translated. As such, adding
comments beside messages is a helpful practice. However, you might assume
that you should add a regular comment beside an entry for this:

```po
# This is a command name
#: src/dpygt/cogs/random.py:18
msgid "roll"
msgstr ""
```

A `#` comment not at the top of the file is considered a "translator comment",
meaning it is only for the translator(s) writing the localization. `msgmerge`
does not share these comments between other localizations and will only try to
preserve them in their current file. If you want to provide comments across all
of your PO files, you should use "extracted comments" instead, denoted with `#.`:

```po
#. This is a command name
#: src/dpygt/cogs/random.py:18
msgid "roll"
msgstr ""
```

However, extracted comments should not be written by hand as they are intended
to be generated only by `xgettext`, and will be overwritten by `msgmerge`.
When running `xgettext`, you can use the
[`-c/--add-comments`](https://www.gnu.org/software/gettext/manual/gettext.html#index-_002dc_002c-xgettext-option)
flag to tell it to scan for comments that precede translatable strings:

```py
# main.py
@app_commands.command(
    # This is a command name
    # And another line...
    name=_("my-command"),
)
async def my_command(interaction):
    ...
```

With the above Python code, running `xgettext --add-comments main.py` results in:

```po
#. This is a command name
#. And another line...
#: main.py:5
msgid "my-command"
msgstr ""
```

Additional resources:

- [The Format of PO Files](https://www.gnu.org/software/gettext/manual/gettext.html#The-Format-of-PO-Files)

## Glossary

1. <span id="domain">Domain</span>

   In gettext, a domain uniquely identifies a set of localizations for a program.
   MO files should be named with their domain as it is required for
   [locating](https://www.gnu.org/software/gettext/manual/gettext.html#Locating-Message-Catalog-Files)
   those files in their [locale] category (`<localedir>/<locale>/<category>/<domain>.mo`).

2. <span id="internationalization">Internationalization/i18n</span>

   As described by the [GNU manual](https://www.gnu.org/software/gettext/manual/gettext.html#I18n_002c-L10n_002c-and-Such),
   internationalization refers to a program's ability to adapt to different [locales]
   without an architectural re-design.

3. <span id="locale">Locale</span>

   As described by the [GNU manual](https://www.gnu.org/software/gettext/manual/gettext.html#I18n_002c-L10n_002c-and-Such),
   a locale defines the "cultural habits" associated with a language and/or country.
   Locales are used as identifiers for categorizing translations.

4. <span id="localization">Localization/L10n</span>

   As described by the [GNU manual](https://www.gnu.org/software/gettext/manual/gettext.html#I18n_002c-L10n_002c-and-Such),
   localization refers to the process of translating a program to one or more [locales].

[domain]: #domain
[internationalization/i18n]: #internationalization
[locale]: #locale
[locales]: #locale
[localization/L10n]: #localization
