# Эмулятор оболочки — Вариант 7, Этап 3

## Что сделано

- Всё из этапа 2 (CLI + TOML + скрипт)
- VFS из CSV **в памяти**
- Файлы: minimal, medium, deep (≥3 уровня)
- Ошибки: файл не найден, неверный формат
- Заголовок окна = имя VFS
- ls/cd пока заглушки (логика — этап 4)

## Запуск

```
python src\emulator.py --vfs vfs_data\minimal.csv
python src\emulator.py --vfs vfs_data\deep.csv
python src\emulator.py --config configs\config.toml
python tests\test_vfs.py
```
