# auto-deployer
Auto deploy files to remove hosts and run scripts

#How to run:

#Sample command and it's output:
```
python3 auto-deployer.py --hosts hosts.yml --command "rm test.sh" --command date --command "touch test.sh" --command "ls -lh test.sh" --command "chmod +x test.sh" --command "ls -lh test.sh"
```
ERROR: timed out connecting to host 10.0.0.1 through SSH
ERROR: timed out connecting to host 10.0.0.2 through SSH
command "rm test.sh" ran on test3

output of command "date" on test3:
Tue May 26 19:12:48 +0430 2020

command "touch test.sh" ran on test3

output of command "ls -lh test.sh" on test3:
-rw-rw-r-- 1 dev dev 0 May 26 19:12 test.sh

command "chmod +x test.sh" ran on test3

output of command "ls -lh test.sh" on test3:
-rwxrwxr-x 1 dev dev 0 May 26 19:12 test.sh
