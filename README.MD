# Сервис рассылок

___
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
	![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
## Перед запуском программы необходимо:

> Настроить почту yandex.ru, [по инструкции](https://clck.ru/3BLEsg)

### Для запуска программы необходимо:

- В корне проекта создать файл .env и заполнить его согласно настройкам,указаным в .env.sample
- В терминале интерпретатора Python ввести команду

```ini
https://github.com/400ton/mailing-service.git
```

- Создать виртуальное окружение:

```ini
python3 -m venv venv
```

- Активировать виртуальное окружение:

```ini
source venv/Scripts/activate
```

- Установить зависимости командой:

```ini
pip install -r requirements.txt
```

- В терминале перейти в корень проекта и выполнить команду и перейти по доменному адресу:

```ini
python manage.py runserver
```

- Для доступа в админ-панель django к адресу локального сервера дописать /admin.
  В предложенной форме ввести имя пользователя: Admin, пароль: 0000
- Команда для заполнения базы данных из файла json используйте команду

```ini
python manage.py fill
```

- Для остановки локального сервера используйте Сtrl+С в терминале