import time
max_time = int(input('Enter the amount of seconds you want to run this: '))
start_time = time.time()  # remember when we started
while (time.time() - start_time) < max_time:
    for i in range(1,10):
        print(i)
        