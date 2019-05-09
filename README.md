# Dotbot yay Plugin

For use with [dotbot](https://github.com/anishathalye/dotbot),
this plugin allows one to easily install or upgrade a list of yaourt packages.

This plugin is a port of [dotbot-yaourt](https://github.com/niklas-heer/dotbot-yaourt) for use with `yay`. Basically the same thing with a `:%s/yaourt/yay` command ran, plus a couple other changes in this readme.

[dotbot-yaourt](https://github.com/niklas-heer/dotbot-yaourt) was itself heavily inspired by the [apt-get](https://github.com/rubenvereecken/dotbot-apt-get) plugin.

## Usage

It's easiest to track this plugin in your dotfiles repo:

```bash
git submodule add https://github.com/oxson/dotbot-yay
```

The original author also recommends having your yay list in a separate file
since dotbot will need root privileges in order to use the plugin.
Using the plugin should look something like this:

```bash
./install -p dotbot-yay/yay.py -c packages.conf.yaml
```

I found that I needed to do this for reasons unknown (should theoretically be the same thing):
```bash
dotbot/bin/dotbot -p dotbot-yay/yay.py -c packages.conf.yaml
```

Example for `packages.conf.yaml`:

```yaml
- yay:
  - vim
  - zsh
  - tldr
```
