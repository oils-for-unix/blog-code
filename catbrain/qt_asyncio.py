import asyncio
import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
import qasync

async def my_coroutine():
    print("Starting coroutine")
    await asyncio.sleep(1)
    print("Coroutine finished")

def button_clicked():
    asyncio.ensure_future(my_coroutine())

app = QApplication(sys.argv)
loop = qasync.QEventLoop(app)
asyncio.set_event_loop(loop)

# Create a simple GUI
window = QWidget()
layout = QVBoxLayout()
button = QPushButton("Run Coroutine")
button.clicked.connect(button_clicked)
layout.addWidget(button)
window.setLayout(layout)
window.show()

# Run the event loop
with loop:
    loop.run_forever()
