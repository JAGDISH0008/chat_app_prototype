import time
import random
channels = {"org1":[],"org2":[],"org3":[],"org4":[],"org5":[]}
channels["org1"].append(1)
channels["org1"].append(2)

# for k in channels["org1"]:
#     if 1 in channels["org1"]:
#         print(k)
while True:
    print(random.choice(list(channels)))
    print(channels[random.choice(list(channels))])
    time.sleep(4)
