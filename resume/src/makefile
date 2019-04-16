all:
	echo "No default goal, use one of [md, tex]"
	exit 1

md:
	mkdir -p build; \
	./vars2yaml md resume.yml build/resume.yml; \
	pandoc build/resume.yml -o build/resume.md --template=resume.md;

tex:
	mkdir -p build; \
	./vars2yaml tex resume.yml build/resume.yml; \
	pandoc build/resume.yml -o build/resume.tex --template=resume.tex; \
	pandoc build/resume.yml -o build/resume.pdf --template=resume.tex --pdf-engine=xelatex; \
	pdftoppm build/resume.pdf build/resume -r 30 -f 1 -singlefile -jpeg -jpegopt quality=90

.PHONY: md tex

