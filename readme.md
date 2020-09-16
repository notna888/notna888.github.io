# notna888.github.io
Putting my personal page up here on github.

## It's main spot is here.
[anton.savill.id.au](https://anton.savill.id.au)

## The backup is here on github
[notna888.github.io](https://notna888.github.io)

### This is just commands for me for pushing to github
ghp-import output
git push git@github.com:notna888/notna888.github.io.git gh-pages:master --force

### pull the plugins
This is how I last got it to work at least...

git submodule init
git submodule update
cd plugins
git submodule add -f https://github.com/mindcruzer/pelican-encrypt-content.git encrypt-content
