ps aux | grep launch.py | awk '{print $2}' | xargs kill -9
