all:
	echo "No default goal, use one of [theme resume-md resume-tex]"
	exit 1

theme:
	mkdir -p _layouts
	cp theme/cayman/_layouts/default.html _layouts/default.html

resume-md:
	cd resume/src; \
	  echo "Building in resume/src/build"; \
	  mkdir -p build; \
	  ./vars2yaml md resume.yml build/resume.yml; \
	  pandoc build/resume.yml -o build/resume.md --template=resume.md;
	mkdir -p resume/web
	cp resume/src/build/resume.md resume/web/README.md

resume-tex:
	cd resume/src; \
	  echo "Building in resume/src/build"; \
	  mkdir -p build; \
	  ./vars2yaml tex resume.yml build/resume.yml; \
	  pandoc build/resume.yml -o build/resume.tex --template=resume.tex; \
	  pandoc build/resume.yml -o build/resume.pdf --template=resume.tex --pdf-engine=xelatex;
	mkdir -p resume/pdf
	cp resume/src/build/resume.pdf resume/pdf/resume-alexandre-dubreuil.pdf

.PHONY: theme


