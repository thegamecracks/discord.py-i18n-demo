# discord.py-i18n-demo

This project demonstrates how to set up gettext localization and integrate it
into discord.py v2.0.

Check out the [onboarding] if you want to learn how gettext and the package works.
If you just want to test out the package, then:

1. Install this repository

   ```sh
   python -m pip install git+https://github.com/thegamecracks/discord.py-i18n-demo
   ```

2. Create a [config.toml] file with your bot token

   ```toml
   [bot]
   token = "Bot token from https://discord.com/developers/applications"
   ```

3. Start the bot

   ```sh
   python -m dpygt
   ```

4. Use the "<@mention> sync" text command to register application commands

## Requirements

- Python 3.11 or greater
- `gettext` and its associated utilities, particularly `msgfmt`
  - Not sure how to get this? See the [onboarding](/docs/en/onboarding.md#gettext)

## Contributing

Want to add translations? [Fork this repository], create a new branch,
commit your changes there, then make a pull request. You may want to
read the [onboarding] to learn how localizations are done, or look at
how [existing localizations](/src/dpygt/locales/) are written.

[onboarding]: /docs/en/onboarding.md
[config.toml]: /src/dpygt/config_default.toml
[Fork this repository]: https://docs.github.com/en/get-started/quickstart/contributing-to-projects
