# Эмулятор оболочки — Вариант 7, Этап 5

## Что сделано

- Этапы 1–4 (GUI, конфиг, VFS, ls/cd/wc/find)
- Команды **mkdir** и **rm** (изменения только в памяти)
- Стартовый скрипт `scripts/test_stage5.sh`

## Запуск

```
python src\emulator.py --config configs\config.toml
python src\emulator.py --vfs vfs_data\medium.csv --script scripts\test_stage5.sh
python tests\test_vfs.py
```

## Команды

| Команда | Описание |
|---------|----------|
| ls [path] | список файлов |
| cd [path] | смена директории |
| pwd | текущий путь |
| wc file | строки, слова, байты |
| find [path] -name name | поиск |
| mkdir path | создать директорию |
| rm path | удалить файл/пустую папку |
| exit | выход |

## Примеры

```
$ mkdir /tmp
создано: /tmp
$ ls /
d  bin
d  etc
d  home
d  tmp
$ rm /tmp
удалено: /tmp
```
