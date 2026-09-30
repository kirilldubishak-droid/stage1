# Эмулятор оболочки — Вариант 7, Этап 1

Минимальный GUI-прототип (tkinter).

## Что сделано

- Окно с заголовком `Эмулятор - default_vfs`
- Парсер с раскрытием `$HOME`, `$USER`
- Заглушки `ls`, `cd`
- Команда `exit`
- Сообщения об ошибках

## Запуск

```
python src/emulator.py
```

Windows: `run.bat`  
Linux/Mac: `./run.sh`

## Тесты

```
python tests/test_parser.py
```

## Примеры

```
$ ls
ls: аргументы = []

$ cd /tmp
cd: аргументы = ['/tmp']

$ foobar
Ошибка: нет команды 'foobar'

$ exit
```
