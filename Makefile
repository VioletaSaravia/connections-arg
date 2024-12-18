count-difs:
	awk '/# [0-9].*/ {print $$2}' "backend/conecciones.txt" | sort | uniq -c

count-words:
	grep -v "[# ].*" "backend/conecciones.txt" | sort | uniq | wc -l

count-cats:
	grep "#.*" "backend/conecciones.txt" | wc -l

words:
	grep -v "[# ].*" "backend/conecciones.txt" | sort | uniq

cats:
	grep "#.*" "backend/conecciones.txt"

setup:
	. backend/.venv/bin/activate

view: setup
	python backend/graph.py
