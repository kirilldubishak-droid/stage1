# Стартовый скрипт — тест всех команд
# Комментарии на # поддерживаются

pwd
ls
cd /home
ls
cd user
pwd
ls

# wc и find
cd /
wc /home/user/hello.txt
find /home -name hello.txt
find / -name docs

# ошибки
wc /no/such/file
foobar

exit
