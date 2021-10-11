# sleepy-driver
Due to the large number of accidents caused by the driver falling asleep while driving, we proposed a solution to solve this problem. The camera records the driver for the entire drive, and when it detects that the driver is asleep, it will sound a beep and a human voice telling it to wake up to wake the driver.

We used the OPEN CV library to process the image and identify whether the driver closed his eyes.

Using PYQT, we created the windows of the system.

We stored the information about the warnings that the driver received in the FIREBASE database so that the information would be saved for the driver from any device from which he entered.

![4](https://user-images.githubusercontent.com/45630158/136717342-2e705c2c-fb70-41c1-894a-16a6c3e50cc8.png)
