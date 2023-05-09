├── README.md <- The top-level README for developers using this project.
├── projects <- Each project contains code for a service and/or ETL
│ ├── project1
│ │ ├── Dockerfile
│ │ ├── pyproject.toml <- Each project has its own dependencies
│ │ ├── project1/ <- Project code (Python modules) go here
│ │ └── tests/
│ └── project2...
│
├── lib <- Each lib is a Python package that you can install using poetry
│ ├── lib1 ||
│ │ ├── pyproject.toml <- Each lib specifies its dependencies
│ │ ├── bipp/lib1/ <- All internal packages are in the bipp namespace
│ │ └── tests/
│ └── lib2...
│
└── tools
├── cookiecutter <- Cookiecutter templates
├── ci/ <- Common CI/CD infrastructure
└── other tools...
