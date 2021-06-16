# Using preconfig
You can see how `preconfig` works with the small example:

```
python preconfig.py small_example.txt.tpl
```

See the comments in the file to see what it does. It will create a file `small_exampleXXXX.txt` for every combination of  parameters in the file. You can check that it works, in bash:

```
cat *.txt|grep parameter2| sort | uniq
cat *.txt|grep parameter1| sort | uniq
```

If you wanted several copies for each set of parameters (for example when you run simulations)

```
python preconfig.py N small_example.txt.tpl
```
Then check `example_scan`