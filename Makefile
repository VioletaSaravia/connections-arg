count-difs:
	awk '/# [0-9].*/ {print $$2}' "conecciones.txt" | sort | uniq -c

count-words:
	grep -v "[# ].*" "conecciones.txt" | sort | uniq | wc -l

count-cats:
	grep "#.*" "conecciones.txt" | wc -l

words:
	grep -v "[# ].*" "conecciones.txt" | sort | uniq

cats:
	grep "#.*" "conecciones.txt"

setup:
	. .venv/bin/activate

view: setup
	python graph.py
