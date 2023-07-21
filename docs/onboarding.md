# Onboarding

Wondering how this project works? This document explains the technologies,
common patterns, and workflows involved in developing it.

- [Onboarding](#onboarding)
  - [Program Description](#program-description)
    - [gettext](#gettext)
    - [Python](#python)
    - [discord.py](#discordpy)
  - [gettext workflow](#gettext-workflow)
    - [Creating a .pot (Portable Object Template) file from a project](#creating-a-pot-portable-object-template-file-from-a-project)
    - [Creating a .po (Portable Object) localization](#creating-a-po-portable-object-localization)
    - [Organizing PO files for gettext](#organizing-po-files-for-gettext)
    - [Creating a .mo (Machine Object) compiled localization](#creating-a-mo-machine-object-compiled-localization)
    - [Updating .po/.pot files after generation](#updating-popot-files-after-generation)

## Program Description

- [ ] Summarize the project architecture

### gettext

On Windows, gettext utilites can be provided by the [Git for Windows](https://git-scm.com/download/)
distribution, either by:

1. using the gettext utilities within Git Bash, or;
2. enabling the "Use Git and optional Unix tools from the Command Prompt"
   option during installation to have access to them in the regular Windows
   terminals.

On Linux, gettext is usually available through your package manager.

You can read more about gettext on the [GNU website](https://www.gnu.org/software/gettext/).

- [ ] Summarize gettext
- [ ] Explain how to install gettext

### Python

[Python](https://www.python.org/) is a general-purpose, dynamically typed language
with a syntax designed to be easier for humans to read.
You can learn more about Python in their [official documentation](https://docs.python.org/).
This project uses Python [3.11](https://docs.python.org/3/whatsnew/3.11.html)
which was released on October 2022 and is being maintained until October 2027.

- [ ] Summarize Python packages
- [ ] Explain how to set up a virtual environment

### discord.py

discord.py's [official documentation](https://discordpy.readthedocs.io/)
and [GitHub repository](https://github.com/Rapptz/discord.py)
are the most up-to-date places to learn how the library works.

- [ ] Summarize discord.py

## gettext workflow

### Creating a .pot (Portable Object Template) file from a project

To create the .pot, start by `cd`ing into `src/dpygt/` and then running
`xgettext **/*.py`. xgettext will scan the given Python files and generate
a resulting `messages.po` file. You can then rename this with the .pot file
extension and "dpygt" domain (resulting in `dpygt.pot`), then edit the comment
header.

Make sure you also change the `Content-Type` charset to `utf-8` since the
[Python gettext](https://docs.python.org/3/library/gettext.html) module
will later rely on it to determine the translation file's encoding.

Additional resources:
- [`*` glob syntax](https://en.wikipedia.org/wiki/Glob_(programming))
- [GNU xgettext manual](https://www.gnu.org/software/gettext/manual/gettext.html#Making-the-PO-Template-File)

- [ ] Explain how source code translatable text is identified

### Creating a .po (Portable Object) localization

Assuming you are still in the `src/dpygt/` directory from the previous section,
you can run `msginit -i dpygt.pot -l <locale>` to generate a new PO file,
where `<locale>` defines the language code and an optional country code in
the form LL_CC, for example `en_US`.

> Note
>
> For this project we are limited to the locales supported by Discord,
> which can be found [in their documentation](https://discord.com/developers/docs/reference#locales).

Afterwards a `<locale>.po` file will be generated in your current directory.
You should open that file and adjust any metadata as necessary (such as `Last-Translator`)
before you start writing translations for messages.

The PO format is explained in the [GNU manual](https://www.gnu.org/software/gettext/manual/gettext.html#The-Format-of-PO-Files).
However, there are also graphical interfaces for editing PO files like
[Lokalize](https://userbase.kde.org/Lokalize),
[Poedit](https://poedit.net/),
and [Virtaal](https://virtaal.translatehouse.org/)
which help with maintaining consistent/correct syntax of the file format.

Additional references:
- [-l/--locale option format](https://www.gnu.org/software/gettext/manual/gettext.html#index-_002dl_002c-msginit-option)
- [ISO 639-1 language codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
- [ISO 3166-1 alpha-2 country codes](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
- [PO Editors](https://www.gnu.org/software/trans-coord/manual/web-trans/html_node/PO-Editors.html)

- [ ] Explain what a .po does

### Organizing PO files for gettext

The [Python gettext module](https://docs.python.org/3/library/gettext.html#gettext.bindtextdomain)
generally requires an explicit path to the directory containing the localizations.
For this project, that has been set to [src/dpygt/locales/](/src/dpygt/locales/).
Within this directory, localizations are further categorized into
`<language>/<category>/<domain>.po`, where `<language>` is the locale code,
`<category>` is the locale category (always LC_MESSAGES for gettext),
and `<domain>` is the domain name. For example, a PO file for a Japanese
localization of this project should be defined as `locales/ja/LC_MESSAGES/dpygt.po`.

### Creating a .mo (Machine Object) compiled localization

- [ ] Explain how .mo files are used
- [ ] Explain how to create a .mo
- [ ] Explain the project's own utilities for .mo generation

### Updating .po/.pot files after generation

- [ ] Explain how to merge .po/.pot changes
