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
  - [Glossary](#glossary)

## Project Summary

This project is written as a Python package, intended to be installed
into a Python environment before execution. It uses the built-in
[Python gettext module](https://docs.python.org/3/library/gettext.html)
to perform translations, and [discord.py](https://discordpy.readthedocs.io/)
to log into Discord with a bot account.

### gettext

gettext refers to a set of utilities written as part of the GNU Project
designed to help programs support internationalization (abbreviated as i18n,
meaning a program can adapt to different locales without an architectural re-design)
and localization (abbreviated as L18n, referring to the process of adding
translations for one or more locales).

On Linux, gettext is usually available through your package manager.

On Windows, gettext utilites can be provided by the [Git for Windows](https://git-scm.com/download/)
distribution, either by:

1. using the gettext utilities within [Git Bash](https://www.atlassian.com/git/tutorials/git-bash),
   or;
2. enabling the "Use Git and optional Unix tools from the Command Prompt"
   option during installation to have access to them in the regular Windows
   terminals.

You can read more about gettext on the [GNU website](https://www.gnu.org/software/gettext/).

### Python

[Python](https://www.python.org/) is a general-purpose, dynamically typed language
with a syntax designed to be easier for humans to read.
You can learn more about Python in their [official documentation](https://docs.python.org/).
This project uses Python [3.11](https://docs.python.org/3/whatsnew/3.11.html)
which was released on October 2022 and is being maintained until October 2027.

- [ ] Summarize Python packages
- [ ] Explain how to set up a virtual environment

### discord.py

discord.py is a Python library that wraps the Discord API and Gateway,
allowing succinct programs that can interact with the Discord social platform.
discord.py's [official documentation](https://discordpy.readthedocs.io/)
and [GitHub repository](https://github.com/Rapptz/discord.py)
are the most up-to-date places to learn how the library works.

To run this project, you must have a bot account created, joined on a server,
and the bot token added to a [config.toml](/src/dpygt/config_default.toml)
file in your current directory.
See step 1 in the
[official Getting Started guide](https://discord.com/developers/docs/getting-started#step-1-creating-an-app)
to complete this. No privileged gateway intents are required, but you are free
to enable them.

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

Before translations in PO files can be used, they must be compiled into MO files,
which are portable (as in cross-platform) binary formats designed for optimized
lookups of translations.

To create a MO file from a PO file, you can use `msgfmt -o <domain>.mo <domain>.po`.
Some GUI editors may do this for you, but otherwise it has to be done for each PO file
which can get tedious. As such, this project provides two utilites for this:

- [utils/build_mo.py](/utils/build_mo.py):
  This is a very simple Python script that invokes msgfmt on all PO files
  found within the src/ directory. It is intended to be run with the project
  root being the current working directory.

- [setup.py](/setup.py):
  This is used by the setuptools build system and implements a subcommand
  which replaces all PO files with MO equivalents when building the package
  (editable installs excepted).
  In other words, the [sdist] will only contain PO files, and the [wheel]
  will only contain the MO files.

[sdist]: https://packaging.python.org/en/latest/flow/#build-artifacts
[wheel]: https://packaging.python.org/en/latest/flow/#build-artifacts

This project prefers that MO files are not included in version control because
they increase the repository size and can lead to inconsistent translations
with their respective PO files.

### Updating .po/.pot files after generation

- [ ] Explain how to merge .po/.pot changes

## Glossary

1. Domain

   In gettext, a domain uniquely identifies a set of translations for a program.
   MO files should be named with their domain as it is required for
   [locating](https://www.gnu.org/software/gettext/manual/gettext.html#Locating-Message-Catalog-Files)
   those files in their locale category (`<localedir>/<locale>/<category>/<domain>.mo`).
