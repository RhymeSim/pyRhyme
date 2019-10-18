# PyRhyme Scrips

## `rhyme_slice`
This script is using `VisItAPI` to plot a pseducolor+slice plot.

To learn more about the script, run

```shell
$ rhyme_slice --help
```

One can use the inline commands to alter the plot. The list of inline commands
will be shown after the script is executed.

To test if the script is working properly, run the following command:

```shell
$ rhyme_slice /path/to/rhyme/output.chombo.h5 --var rho --scaling log \
--min 1e-4 --max 1e5 --colortable RdYlBu --invert --axis x --percent 60 \
--commands 'sl50, cn0, cp5, ck, cj, tt1.23, pslinear, pvu'
```
