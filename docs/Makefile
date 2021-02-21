# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
# SPHINXOPTS    ?= -w warnings.log
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile html-with-todo html-without-todo all

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

html-with-todo:
	$(SPHINXBUILD) -M html . $(BUILDDIR)/html-with-todo -D todo_include_todos=1 -w warnings-with-todo.log $(SPHINXOPTS) $(O)
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html-with-todo."

html-without-todo:
	$(SPHINXBUILD) -M html . $(BUILDDIR)/html-without-todo -D todo_include_todos=0 -w warnings-without-todo.log $(SPHINXOPTS) $(O)
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html-without-todo."

all: clean html-with-todo html-without-todo
