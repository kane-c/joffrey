import os
import glob


__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + '/*.py')]
from Phrangman import Phrangman
for module in __all__:
    __import__(module, locals(), globals())
