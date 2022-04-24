Code for doing needlet analysis on EoR. 

- needlet_funcs: contains all the heavy-lifting functions
- scripts: contains mainly plotting scripts
- boxes: contains all 21cmfast output boxes in binary. not committing the dir cause its big, committing a zipped file instead.

In order to run, you need to do

```
python -m pip install -e needlet_funcs
```

which lets the scripts inside needlet_funcs be called from anywhere.