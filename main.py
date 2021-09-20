import threading
from muzmo import Muzmo

nabor = ['Баста']

for i in nabor:
    print(i)
    threading.Thread(target=Muzmo(5).download_with_name, args=(i,)).start()

Muzmo(3).download_top_all()
