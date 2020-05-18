# Resume

## Resume Portable Format (PDF)

<span class="icon icon-link">**[PDF version](pdf)**</span>

## Resume HTML (web)

<span class="icon icon-website">**[Web version](web)**</span>

## Source

<span class="icon icon-github">**[Source Code](https://github.com/dubreuia/alexandredubreuil.com/tree/master/resume)**</span>

Using [pandoc](https://pandoc.org) to generate a web version and a latex version from a common source file.

### Installation instruction

You'll need `pandoc`, `texlive-full` (you might be able to use a smaller latex packaging) and `pdftoppm` to convert to png for the thumbnail.

```bash
sudo apt install pandoc texlive-full pdftoppm
```

### Usage

```bash
# Buils the files in the "build" folder, for the pdf,
# png preview and md files
make markdown

# Copies the files from the "build" folder to the target folders,
# to the "pdf" and "web" folders
make install
```

### Files

The file `resume.yml` contains the resume content in yaml which is used by pandoc to replace the values in `resume.md` for the web version and `resume.tex` for the latex version. The latex version has it's style sheet `resume.sty` to split formatting from structure.

There's a preprocessor script `vars2yaml` that replaces `$command{stuff}` content with proper content enabling language agnostic formatting. For example `$strong{stuff}` gets replaced by `**stuff**` in markdown and `\textbf{stuff}` in latex.

