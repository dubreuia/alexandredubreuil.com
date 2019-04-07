all:
	echo 'Usage: make [tex, md]'

open:
	vim -O resume-en.yml resume.tex resume.sty

tex:
	mkdir -p out
	./vars2yaml tex resume-en.yml out/resume-en.yml
	pandoc out/resume-en.yml -o out/resume-en.tex --template=resume.tex
	pandoc out/resume-en.yml -o out/resume-en.pdf --template=resume.tex --pdf-engine=xelatex
	evince out/resume-en.pdf &

md:
	mkdir -p out
	./vars2yaml md resume-en.yml out/resume-en.yml
	pandoc out/resume-en.yml -o out/resume-en.md --template=resume.md

