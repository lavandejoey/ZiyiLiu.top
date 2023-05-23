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

    - `css`: Contains CSS files, including `font-awesome.css`, `font-awesome.css.map`, `font-awesome.min.css`, and `JoshuaZiyiLiu.css`.

    - `fonts`: Includes various font files, including `FontAwesome.otf`, `fontawesome-webfont.eot`, `fontawesome-webfont.svg`, `fontawesome-webfont.ttf`, `fontawesome-webfont.woff`, `fontawesome-webfont.woff2`, and font files for HarmonyOS_Sans fonts.

    - `img`: Contains image files used by the application, such as `badge.svg`, `favicon.ico`, and `logo-pic.png`.

    - `js`: Contains JavaScript files required by the application, including Bootstrap-related scripts and `JoshuaZiyiLiu.js`.

    - `scss`: Contains SCSS files, including `JoshuaZiyiLiu.css`, `JoshuaZiyiLiu.css.map`, and `JoshuaZiyiLiu.scss`.

- `templates`: This directory contains HTML templates used by the application. It includes the following files:

    - `base.html`: The base HTML template used as the layout for other pages.

    - `contact.html`: The HTML template for the contact page.

    - `cv.html`: The HTML template for the curriculum vitae page.

    - `index.html`: The HTML template for the homepage.

    - `portfolio.html`: The HTML template for the portfolio page.

    - `svg`: This subdirectory contains the `rustysentry.svg` file used for SVG graphics.

- `views`: This directory contains the views and routing logic implemented in `main.py`. It includes an `__init__.py` file and `main.py`.

