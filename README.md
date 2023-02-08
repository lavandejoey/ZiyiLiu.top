# Welcome to my website @ [lzyatshcn.top](https://www.lzyatshcn.top/)

## About

### source code structure
```text
├── LICENSE
├── README.md
├── __init__.py
├── instance 特定于应用程序特定实例的配置文件，例如数据库 URI 或密钥。
│        └── config.py
├── mainApp 应用程序mainApp的主要代码
│        ├── __init__.py 使用应用程序工厂模式创建 Flask 应用程序对象。它设置数据库和其他配置选项。
│        ├── models.py 定义将在应用程序中使用的数据库模型。
│        ├── routes.py 定义应用程序的端点和路由。
│        ├── static
│        │       ├── css
│        │       ├── image
│        │       ├── js
│        │       └── scss
│        └── templates 应用程序将用于呈现页面的 HTML 模板。
├── requirements.txt 运行应用程序所需的包。
└── run.py 用于运行应用程序。它设置FLASK_APP和FLASK_ENV环境变量，然后运行flask run。
```

### colour set

| clf           | example                                                                                                                                        |
|:--------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| bg            | <span style="color:#F7F0EA"><b>text</b></span>, <span style="color:#FDF8F2"><b>text</b></span>, <span style="color:#E8E1DB"><b>text</b></span> |
| bg-active     | <span style="color:#FADFB0"><b>text</b></span>                                                                                                 |
| bg-inactive   | <span style="color:#FCF7F1"><b>text</b></span>                                                                                                 |
| icon-active   | <span style="color:#75581F"><b>text</b></span>                                                                                                 |
| icon-inactive | <span style="color:#706A5E"><b>text</b></span>, <span style="color:#B3AA9B"><b>text</b></span>                                                 |
| font          | <span style="color:#241D17"><b>text</b></span>                                                                                                 |
| font-b        | <span style="color:#73331B"><b>text</b></span>                                                                                                 |

## How to help

## Contact me

## License
