pybabel extract -F babel.cfg -o messages.pot .
pybabel update -i messages.pot -d translations
#pybabel init -i messages.pot -d translations -l fr
#pybabel init -i messages.pot -d translations -l zh_Hans
#pybabel init -i messages.pot -d translations -l zh_Hant         Chinese (Traditional)
#pybabel init -i messages.pot -d translations -l yue
pybabel compile -d translations
