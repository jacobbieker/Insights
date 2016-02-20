readme.txt

The included files allow conversion of Hexoskin data to CSV so they can be analyzed or otherwise used in a more human-friendly fashion.

The Mac, Windows and Ubuntu files can be used by calling:

Windows
    C:\Path\to\windows\ConvertSourceFile.exe C:\Path\to\folder_to_convert

Mac
    ~/Path/to/mac/ConvertSourceFile ~/Path/to/folder_to_convert

Ubuntu
    ~/Path/to/ubuntu/ConvertSourceFile ~/Path/to/folder_to_convert


The code folder contains a version of the conversion script in Matlab/Octave format, in Python and in C, if you are interested in having a look at how to script works (The mac, windows and ubuntu codes are compiled from the c code included)

The Matlab/Octave script in the code folder can be used just as any other function. Just put it in your folder, and call
	convertSourceFile('/path/to/your/folder')

Finally, the Python script in the code folder works the same way. You can call
	python convertSourceFile.py path/to/your/folder

For more details on the downloaded data, refer to
http://support.hexoskin.com/customer/portal/articles/1633107-technical-description-of-data-channels