# sleepy-driver
Due to the large number of accidents caused by the driver falling asleep during the trip, we proposed a solution in order to solve this problem.
RECORD webcam the driver for the entire trip and when it detects that the driver is asleep it will sound a beep and a human voice telling him to wake up in order to wake the driver

We used the OPEN CV library to process the image and identify whether the driver closes his eyes.
Using PYQT we created the windows of the system
We stored the information about the warnings that the driver received in the FIREBASE database so that the information would be saved for the driver from any device from which he entered.
