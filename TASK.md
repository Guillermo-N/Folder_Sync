# Task

Implement a program that synchronizes two folders: source and replica. The program should maintain a full, identical copy of source folder at replica folder. Solve the test task by writing a program in one of these programming languages:

<br>
<center>
Python ✅ <br>
C/C++ <br>
C# <br>
</center>
<br>

1. Synchronization must be one-way: after the synchronization content of the replica folder should be modified to exactly match content of the source folder;

2. Synchronization should be performed periodically.

3. File creation/copying/removal operations should be logged to a file and to the console output;

4. Folder paths, synchronization interval and log file path should be provided using the command line arguments;

5. It is undesirable to use third-party libraries that implement folder synchronization;

6. It is allowed (and recommended) to use external libraries implementing other well-known algorithms. For example, there is no point in implementing yet another function that calculates MD5 if you need it for the task – it is perfectly acceptable to use a third-party (or built-in) library.