# discord.py-i18n-demo

This project is a demonstration of how to set up gettext localization
(at a beginner level) and integrate it into discord.py v2.0!

Check out the [onboarding] if you want to learn how the package works.
If you just want to test out the package then install this repository,
create a [config.toml] file in your current working directory,
start the bot, then use the "@mention sync" command.

```sh
python -m pip install git+https://github.com/thegamecracks/discord.py-i18n-demo
python -m dpygt
```

## Requirements

- Python 3.11+
- `gettext` and its associated utilities, particularly `msgfmt`
  - Not sure how to get this? See the [tutorial]

[onboarding]: /docs/onboarding.md
[config.toml]: /src/dpygt/config_default.toml
