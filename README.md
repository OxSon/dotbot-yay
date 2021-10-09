# Dotbot yay Plugin

For use with [dotbot](https://github.com/anishathalye/dotbot),
this plugin allows one to easily install or upgrade a list of yay packages.

This plugin is a port of [dotbot-yaourt](https://github.com/niklas-heer/dotbot-yaourt) for use with `yay`. Basically the same thing with a `:%s/yaourt/yay` command ran, plus a couple other relevant changes.

[dotbot-yaourt](https://github.com/niklas-heer/dotbot-yaourt) was itself heavily inspired by the [apt-get](https://github.com/rubenvereecken/dotbot-apt-get) plugin.

## Usage

It's easiest to track this plugin in your dotfiles repo:

```bash
git submodule add https://github.com/oxson/dotbot-yay
```

The original author also recommends having your yay list in a separate file
since dotbot will need root privileges in order to use the plugin.

If you use the default install script provided by [dotbot](https://github.com/anishathalye/dotbot), using the plugin will look like this:

```bash
./dotbot/bin/dotbot -p dotbot-yay/yay.py -c packages.conf.yaml
```

Using the `install` script provided by this repo, using the plugin will look like this:
```bash
./install packages
```

Example for `packages.conf.yaml`:

```yaml
- yay:
  - vim
  - zsh
  - tldr
```
