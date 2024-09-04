# [ZiyiLiu.top Site](https://github.com/lavandejoey/ZiyiLiu.top)

[//]: # (Badges)
[![stars](https://img.shields.io/github/stars/lavandejoey/ZiyiLiu.top.svg)]()
[![license](https://img.shields.io/github/license/lavandejoey/ZiyiLiu.top.svg)]()
[![Python](https://img.shields.io/badge/python-3.10.13-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Flask](https://img.shields.io/badge/flask-2.3.2-blue.svg)](https://flask.palletsprojects.com/en/1.1.x/)
[![Mysql](https://img.shields.io/badge/mysql-8.0.34-blue.svg)](https://dev.mysql.com/downloads/mysql/)

This repository contains the source code and files for [www.ZiyiLiu.top](https://www.ZiyiLiu.top), a
personal website developed by Ziyi Liu. The website showcases Ziyi's portfolio, provides contact information,
and includes a CV (Curriculum Vitae).

## Directory Structure

The repository's directory structure is as follows:

```
.
├── LICENSE
├── MainApplication
│   ├── __init__.py
│   ├── apis
│   ├── forms
│   ├── static
│   │   ├── css
│   │   ├── fonts
│   │   ├── img
│   │   ├── js
│   │   ├── package.json
│   │   ├── package-lock.json
│   │   └── scss
│   ├── templates
│   ├── translations
│   └── views
├── README.md
├── requirements.txt
└── run.py
```

MainApplication: Contains the main application files.

- `__init__.py`: This file initializes the application and contains the application factory.

- `apis`: This directory contains API-related files used by the application. Currently.

- `forms`: This directory contains form-related files used by the application. Currently.

- `static`: This directory contains static files such as CSS stylesheets, fonts, images, and JavaScript files used by
  the application. It has the following subdirectories:

- `templates`: This directory contains HTML templates used by the application. It includes the following files:

- `translations`: This directory contains translation files used by the application.

- `views`: This directory contains the views and routing logic implemented in `main.py`. It includes an `__init__.py`
  file and `main.py`.

## Update History

- [2023-11-02] Build API blueprint for **_authentication_** and **_user_**; add **_user_** model. Driven by JWT.
- [2023-10-13] Add a new blueprint for **_authentication_**, added login/signup/logout pages; connected to **_MySql_** database
- [2023-10-12] **_Internationalization_** (i18n) support (EN-UK, ZH-CN, YUE-HK, FR-FR)
- [2023-02-12] Signin/up pages
- [2023-02-10] Dependencies update
- [2023-02-09] Create .travis.yml for Travis CI

## License

This project is licenced under the Apache Licence 2.0 - see the [LICENCE](LICENCE) file for details.
