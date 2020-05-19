all:
	echo "No default goal, use one of [build, install]"
	exit 0

build:
	# Build the web version using pandoc
	mkdir -p build
	./vars2yaml markdown resume.yml build/resume.yml
	pandoc build/resume.yml -o build/resume.md --template=resume.md
	# Build the pdf version using latex (pandoc)
	mkdir -p build
	./vars2yaml tex resume.yml build/resume.yml
	pandoc build/resume.yml -o build/resume.tex --template=resume.tex
	pandoc build/resume.yml -o build/resume.pdf --template=resume.tex --pdf-engine=xelatex
	pdftoppm build/resume.pdf build/resume -r 30 -f 1 -singlefile -jpeg -jpegopt quality=90

install:
	cp build/resume.pdf resume-alexandre-dubreuil-pdf/resume-alexandre-dubreuil.pdf
	cp build/resume.jpg resume-alexandre-dubreuil-pdf/resume-alexandre-dubreuil.jpg
	cp build/resume.md resume-alexandre-dubreuil-web/README.md

.PHONY: build install

