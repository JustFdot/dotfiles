# My personal collection of dotfiles

## Usage

I didn't figure out how to configure xstow per package, so by now installing might be a little tricky

```sh
git clone https://github.com/justfdot/dotfiles.git ~/dotfiles
cd ~/dotfiles
# For system-wide configs
xstow -ap system -t /
# For home-living configs
xstow home
```
