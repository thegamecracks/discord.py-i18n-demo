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
    - [Creating a .mo (Machine Object) compiled localization](#creating-a-mo-machine-object-compiled-localization)
    - [Updating .po/.pot files after generation](#updating-popot-files-after-generation)

## Program Description

- [ ] Summarize the project architecture

### gettext

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

- [ ] Explain what a .po does
- [ ] Explain how to create a .po

### Creating a .mo (Machine Object) compiled localization

- [ ] Explain how .mo files are used
- [ ] Explain how to create a .mo
- [ ] Explain the project's own utilities for .mo generation

### Updating .po/.pot files after generation

- [ ] Explain how to merge .po/.pot changes
