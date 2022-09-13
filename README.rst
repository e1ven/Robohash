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
    with open("path/to/new/file.png", "wb") as f:
        rh.img.save(f, format="png")

Robosets
--------

RoboHash comes with five image sets, named "set1", "set2", "set3", "set4" and "set5".
Specify which set you want in the ``assemble()`` method. Alternatively,
specify the string "any", and RoboHash will pick an image set for you,
based on the provided hash.


License
-------

The Python Code is available under the MIT/Expat license. See the
``LICENSE.txt`` file for the full text of this license. Copyright (c)
2011.

Feel free to embed the Robohash images, host your own instance of Robohash, 
or integrate them into your own project.
If you do, please just mention where they came from :) 
Example wording might be "Robots lovingly delivered by Robohash.org" or similar. 

The "set1" artwork (and robohash backgrounds) were created by Zikri Kader. 
They are available under CC-BY-3.0 or CC-BY-4.0 license.

The "set2" artwork was created by Hrvoje Novakovic. 
They are available under CC-BY-3.0 license.

The "set3" artwork was created by Julian Peter Arias.
They are available under CC-BY-3.0 license.

The Cats/"set4" were created by David Revoy, used under CC-BY-4.0
https://www.peppercarrot.com/en/article391/cat-avatar-generator

The avatars used in "set5" were created by Pablo Stanley, for https://avataaars.com/  
They are "Free for personal and commercial use. 😇"




Disclaimer
----------

OK, I'll admit I'm a crappy programmer. Compounding this, I wrote this
code initially to be internal-only. It's ugly, and could be a LOT nicer.

Sorry about that.

.. _RoboHash.org: https://robohash.org/
