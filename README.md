# kindle-goodreads-sync
Python project to facilitate syncing books and reading progress from Amazon's Kindle cloud reader and a Goodreads account

## Installing PhantomJS ##

You need at least PhantomJS 1.8.1.  There are *no other external
dependencies* (you don't need Qt, or a running X server, etc.)

### Mac ###

* *Homebrew*: `brew install phantomjs`
* *MacPorts*: `sudo port install phantomjs`
* *Manual install*: [Download this](https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-macosx.zip)

### Linux ###

* Download the [32 bit](https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-i686.tar.bz2)
or [64 bit](https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2)
binary.
* Extract the tarball and copy `bin/phantomjs` into your `PATH`

### Windows ###
* Download the [precompiled binary](https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip)
for Windows
