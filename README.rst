RoboHash
========

The source code for `RoboHash.org`_.

It basically copy/pastes various robot pictures together, using bits
from the SHA hash. It's not perfect, and not entirely secure, but it
gives a good gut-check to "Hey, this SHA is wrong."

Install
-------

Just the library:

.. code:: bash

    $ pip install robohash

Or if you also want the web frontend:

.. code:: bash

    $ pip install robohash[web]

Usage
-----

.. code:: python

    from robohash import Robohash

    hash = "whatever-hash-you-want"
    rh = Robohash(hash)
    rh.assemble(roboset='any')
    with open("path/to/new/file.png", "w") as f:
        rh.img.save(f, format="png")

Robosets
--------

RoboHash comes with three image sets, named "set1", "set2", and "set3".
Specify which set you want in the ``assemble()`` method. Alternatively,
specify the string "any", and RoboHash will pick an image set for you,
based on the provided hash.

The "set1" artwork was created by Zikri Kader. The "set2" artwork was
created by Hrvoje Novakovic. The "set3" artwork was created by Julian
Peter Arias.
The Cats/"set4" were created by David Revoy, used under CC-BY-4.0
https://www.peppercarrot.com/en/article391/cat-avatar-generator


License
-------

The Python Code is available under the MIT/Expat license. See the
``LICENSE.txt`` file for the full text of this license. Copyright (c)
2011, Colin Davis.

The RoboHash images are available under the CC-BY-3.0 license.

Disclaimer
----------

OK, I'll admit I'm a crappy programmer. Compounding this, I wrote this
code initially to be internal-only. It's ugly, and could be a LOT nicer.

Sorry about that.

.. _RoboHash.org: https://robohash.org/
