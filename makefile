all:
	echo "No default goal, use one of [theme]"
	exit 1

theme:
	mkdir -p _layouts
	cp theme/cayman/_layouts/default.html _layouts/default.html

.PHONY: theme

