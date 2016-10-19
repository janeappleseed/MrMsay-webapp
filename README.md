MrMsay
======

This repository contains the source code of
[mrmsay.herokuapp.com](https://mrmsay.herokuapp.com/), the web app for
[MrMsay](https://github.com/janeappleseed/MrMsay).

Dependencies
------------

- Python 3.3 or later.

Getting started
---------------

```sh
git clone https://github.com/janeappleseed/MrMsay-webapp mrmsay-webapp
cd mrmsay-webapp
pip3 install -r requirements.txt
export PYTHONPATH=$PWD/MrMsay/src:$PYTHONPATH
export GH_CREDENTIALS=<user>:<token>
./webapp.py
```

Virtualenv is highly recommended.

License
-------

Although MrMsay is under WTFPL, this repository is licensed under
[GPLv3](COPYING) due to [vendored cowsay](vendor/cowsay).
