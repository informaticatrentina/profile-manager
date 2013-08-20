# Silly Makefile for extract, update and compile messages
i18n:
	pybabel extract -F babel.cfg -o messages.pot .
	pybabel update -i messages.pot -d ProfileManager/translations
	pybabel compile -d ProfileManager/translations
	rm messages.pot

init-en:
	pybabel extract -F babel.cfg -o messages.pot .
	pybabel init -d ProfileManager/translations -l en -i messages.pot
	rm messages.pot
