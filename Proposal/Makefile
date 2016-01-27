default: show

TEX = proposal

#%.aux %.log %.dvi: %.tex
#	latex $<

pdf: alltex
	dvipdf $(TEX).dvi

alltex:
	latex $(TEX).tex
	bibtex $(TEX).aux
	latex $(TEX).tex
	latex $(TEX).tex

clean:
	rm $(TEX).aux
	rm $(TEX).log
	rm $(TEX).dvi
	rm $(TEX).pdf
	rm $(TEX).bbl
	rm $(TEX).blg

show: pdf
	evince $(TEX).pdf
