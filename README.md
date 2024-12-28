# Automatic Layout Check

Automatic Layout Check is a web service that allows users to check the correctness of HTML and CSS markup
against a predefined template.


## Развертывание окружения
Для развертывания окружения и дальнейшей разработки необходимо выполнить следующие шаги:
1. **Создать виртуальное окружение**
   - _В PyCharm_:
       - **Settings -> Python Interpreter -> Add Interpreter -> Add Local Interpreter -> Poetry Environment**
       - Выбираем **Poetry Environment**
       - В **base interpreter** выбираем **python 3.11** (устанавливаем если нет)
       - Ставим галочку **Install packages from pyproject.toml**
       - Нажимаем на **OK**

   - _Либо развернуть окружение через терминал_
        - Создать виртуальное окружение с названием _venv_:
       ``` bash
       python -m venv venv
       ```
        - Активировать виртуальное окружение
          - для macOS и Linux:
             ``` bash
             source venv/bin/activate
             ```
          - для Windows:
             ``` bash
             venv\Scripts\activate
             ```
2. **Установить poetry**
``` bash
pip install poetry
```

3. **Выполнить установку зависимостей**
``` bash
poetry install
```

4. **Выполнить установку драйвера chromium**
```bash
playwright install chromium
```
