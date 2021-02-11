# JupyterLazyLoader

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square)

I often have a ton of standard imports which slow down startup time. As a matter of style, I usually import all of these at once at the start of the notebook. This allows me to quickly see all relevant imports and not move imports around as needed. But this is wasteful as I don't usually need all of them to be loaded immediatly. Therefore it would be ideal if the modules where lazy loaded. 

To my surprise the only "solution" to this is [this project](https://github.com/8080labs/pyforest) which I dislike for a few reasons:
 - There's a lot of modules it can implicitely import for you, but you need to know which ones these are or configure extra modules yourself
 - When you import a module, it automatically edits a jupyter cell. This is horrible for version control and seems like a bad idea overall.
 - The way it installs is quite invasive (it auto enables itself by default) and it's hard to uninstall fully.
 
 So here's an alternative that is much simpler (less than 50 loc) and works like so:
 
 ```python 
%%lazyimport

from functools import (
    partial, 
    lru_cache
)

from collections import defaultdict, OrderedDict, deque
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
```

This will create placeholders instead of actually importing the module, and as soon as you interact with the module or use it in ay way, it will be dynamically imported. Simple! An added side effect is that if you don't end up using one of the packages it won't get imported!

To use it, you'll need to either load the extension:

```python
%load_ext lazyimport
```

or place it in jupyter's startup directory which you can find by running the following: 

```python
get_ipython().profile_dir.startup_dir
```

> _**Note:**_ This does not work with wildcard imports such as `from sklearn import *`. This is due to python's import dynamics, and besides, wildcard imports are usually a bad idea.

_*Remark:*_ Yes, this extensions actually adds the modules to `builtins` instead of to `__main__`'s globals. This is simply because globals aren't shared between modules so the lazy importer cannot access them. Let me know if you know a more elegant solution!
