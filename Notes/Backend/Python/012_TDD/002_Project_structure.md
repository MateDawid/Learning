# Project structure

```
├── sum
│   ├── __init__.py
│   └── another_sum.py
└── tests
    ├── __init__.py
    ├── conftest.py
    ├── pytest.ini
    └── test_sum
        ├── __init__.py
        └── test_another_sum.py
```

Keeping your tests together in single package allows you to:

- Reuse pytest configuration across all tests
- Reuse fixtures across all tests
- Simplify the running of tests