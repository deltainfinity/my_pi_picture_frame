# my_pi_picture_frame
*Under Development!*

This project will use Python to display photos stored in cloud sources on a photo frame constructed using a Raspberry Pi. The project is currently under active development. The test code for keeping a local copy of the contents of an application folder on DropBox has been completed. This was done primarily so that I coulod learn the DropBox API without having to deal with the overhead of object creation. Next up I will be converting the procedural test code into a class for use in the final software for the photo frame.

I have created a class that authenticates the application with DropBox. Currently this requires the user to copy and paste the authorization code from a web browser into the program. Borrowing from the method used by the creators of pyDrive I plan on instantiating a headless web server to receive the authorization code from the program, thus eliminating the need for the user to copy and paste the code. I will implement this functionality once a minimum viable product has been produced for the DropBox source.

I will be creating code to synchronize a Google Drive folder in the same way the DropBox code uses. I will be using pyDrive for this, because why reinvent the wheel? The Google Drive source will be the second source implemented.

The initial idea for the read_me for the completed program is found below:

Displays photo slideshows from various online resources using a Raspberry Pi. The display code is written in Python. The program supports displaying photos stored on Google Drive and Dropbox at this time. More sources to come.
