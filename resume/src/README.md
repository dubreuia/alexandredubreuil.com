# Resume source

<span class="icon icon-github">**[Source Code](https://github.com/dubreuia/alexandredubreuil.com/tree/master/resume/src)**</span>

Using [pandoc](https://pandoc.org) to generate a web version and a latex version from a common source file.

## Installation instruction

You'll need `pandoc`, `texlive-full` (you might be able to use a smaller latex packaging) and `pdftoppm` to convert to png for the thumbnail.

```bash
sudo apt install pandoc texlive-full pdftoppm
```

## Usage

```bash
# For the web version, this command generates build/resume.md
make md

# For the latex version, this command generates build/resume.pdf and build/resume.jpg (thumbnail)
make tex
```

## Files

The file `resume.yml` contains the resume content in yaml which is used by pandoc to replace the values in `resume.md` for the web version and `resume.tex` for the latex version. The latex version has it's style sheet `resume.sty` to split formatting from structure.

There's a preprocessor script `vars2yaml` that replaces `$command{stuff}` content with proper content enabling language agnostic formatting. For example `$strong{stuff}` gets replaced by `**stuff**` in markdown and `\textbf{stuff}` in latex.

