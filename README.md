# discord.py-gettext-demo

This project is a demonstration of how to set up gettext localization
(at a beginner level) and integrate it into discord.py v2.0!

Check out the [tutorial] if you want to build this from scratch.
If you just want to test out the example, install this repository,
write a [config.toml] in your current working directory, start the bot,
then use the "@mention sync" command.

```sh
python -m pip install git+https://github.com/thegamecracks/discord.py-gettext-demo
python -m dpygt
```

## Requirements

- Python 3.11+
- `gettext` and its associated utilities, particularly `msgfmt`
  - Not sure how to get this? See the [tutorial]

[tutorial]: /docs/TUTORIAL.md
[config.toml]: /config_default.toml
