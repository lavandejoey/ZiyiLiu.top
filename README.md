# JoshuaZiyiLiu.com

This repository contains the source code and files for [www.JoshuaZiyiLiu.com](https://www.JoshuaZiyiLiu.com), a personal website developed by Joshua Ziyi Liu. The website showcases Joshua's portfolio, provides contact information, and includes a CV (Curriculum Vitae).

## Directory Structure

The repository's directory structure is as follows:

```
.
├── LICENSE
├── MainApplication
│   ├── forms
│   ├── __init__.py
│   ├── static
│   │   ├── css
│   │   ├── fonts
│   │   ├── img
│   │   ├── js
│   │   ├── package.json
│   │   ├── package-lock.json
│   │   └── scss
│   ├── templates
│   └── views
├── README.md
├── requirements.txt
└── run.py
```

MainApplication: Contains the main application files.

- `forms`: This directory contains form-related files used by the application. Currently, it includes `email.py` which handles email forms.

- `static`: This directory contains static files such as CSS stylesheets, fonts, images, and JavaScript files used by the application. It has the following subdirectories:

- `templates`: This directory contains HTML templates used by the application. It includes the following files:

- `views`: This directory contains the views and routing logic implemented in `main.py`. It includes an `__init__.py` file and `main.py`.
