# Эмулятор оболочки — Вариант 7, Этап 2

## Что сделано

- Параметры CLI: `--vfs`, `--prompt`, `--script`, `--config`
- Конфиг TOML (файл имеет приоритет над CLI)
- Отладочный вывод параметров при запуске
- Стартовый скрипт с комментариями `#`
- Ошибки чтения конфига и скрипта
- Заглушки `ls`, `cd`, команда `exit`

## Запуск

```
python src\emulator.py --prompt "test$ "
python src\emulator.py --config configs\config.toml
python src\emulator.py --script scripts\test_stage2.sh
scripts\run_cli_config.bat
```

## Примеры

```
$ ls
ls: аргументы = []
$ cd /tmp
cd: аргументы = ['/tmp']
$ foobar
Ошибка: нет команды 'foobar'
```
