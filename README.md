# lightmixer
This is light mixing software written in Python 3.5 mainly used to control DMX lights via UDP. It is still very experimental, so be warned if you try to use it.

The mixer outputs UDP packages to clients subscribed to universes containing one byte of data per channel.

At the moment it can handle dimming 20000 channels simultaneously on a 2.4ghz i7 processor core while keeping above 40fps. This should be more than enough for most use, but I intend to make it more efficient for use on a raspberry pi later.