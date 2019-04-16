all:
	echo "No default goal, use one of [theme resume-md resume-tex]"
	exit 1

theme:
	mkdir -p _layouts
	cp theme/cayman/_layouts/default.html _layouts/default.html

resume-md:
	cd resume/src; \
	  make md;
	mkdir -p resume/web
	cp resume/src/build/resume.md resume/web/README.md

resume-tex:
	cd resume/src; \
	  make tex;
	mkdir -p resume/pdf
	cp resume/src/build/resume.pdf resume/pdf/resume-alexandre-dubreuil.pdf
	cp resume/src/build/resume.jpg resume/pdf/resume-alexandre-dubreuil-thumbnail.jpg

.PHONY: theme resume-md resume-tex


