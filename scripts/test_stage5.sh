# Тест этапа 5: mkdir, rm + прошлые команды
# Комментарии на #

pwd
ls

# создать папку и файл через mkdir
mkdir /tmp
mkdir /tmp/work
ls /tmp

cd /tmp/work
pwd
mkdir nested
ls

# ошибки mkdir
mkdir /tmp/work
mkdir /no/parent/here

# rm
cd /
rm /tmp/work/nested
ls /tmp/work
rm /tmp/work
rm /tmp
ls /

# ошибка rm
rm /no/such
rm /home

# прошлые команды
ls /home
wc /home/user/hello.txt
find / -name hello.txt
foobar

exit
