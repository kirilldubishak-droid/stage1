# Эмулятор оболочки — Вариант 7, Этап 4

## Что сделано

- Этапы 1–3 (GUI, конфиг, VFS)
- Настоящие команды **ls** и **cd**
- Команды **wc** и **find**
- Стартовый скрипт `scripts/test_all.sh`

## Запуск

```
python src\emulator.py --config configs\config.toml
python src\emulator.py --vfs vfs_data\deep.csv --script scripts\test_all.sh
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
| exit | выход |

## Примеры

```
$ ls
d  bin
d  etc
d  home
$ cd /home/user
Путь: /home/user
$ wc hello.txt
  1  2  11  hello.txt
$ find / -name note.txt
/home/user/docs/note.txt
```
