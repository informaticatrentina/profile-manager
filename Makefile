# Silly Makefile for extract, update and compile messages
i18n:
	pybabel extract -F babel.cfg -o messages.pot .
	pybabel update -i messages.pot -d ProfileManager/translations
	pybabel compile -d ProfileManager/translations
	rm messages.pot
