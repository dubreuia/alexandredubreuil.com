all:
	echo "No default goal, use one of [markdown, tex]"
	exit 1

markdown:
	mkdir -p build; \
	./vars2yaml markdown resume.yml build/resume.yml; \
	pandoc build/resume.yml -o build/resume.md --template=resume.md;

tex:
	mkdir -p build; \
	./vars2yaml tex resume.yml build/resume.yml; \
	pandoc build/resume.yml -o build/resume.tex --template=resume.tex; \
	pandoc build/resume.yml -o build/resume.pdf --template=resume.tex --pdf-engine=xelatex; \
	pdftoppm build/resume.pdf build/resume -r 30 -f 1 -singlefile -jpeg -jpegopt quality=90

install:
	cp build/resume.$(target) ../$(target)/resume-alexandre-dubreuil.$(target)
	cp build/resume.jpg ../$(target)/resume-alexandre-dubreuil.jpg

.PHONY: markdown tex

