FontFuzzer
==========

The FontFuzzer is created to fuzz the TrueType Font (TTF) into different sizes which enables the generation of test cases to determine the size of font in triggering the vulnerability. The overall process of the fuzzer starts with automating detect the 'FontName' and install the crafted font in Windows system. It will then display the font in a different size, uninstall the font file and repeat the process if no vulnerability is found.

Extra python packages needed:
1. pywin32-216.win32-py2.7
2. numpy-1.7.0b1-win32-superpack-python2.7
3. fonttools-2.3
4. comtypes-0.6.2.win32

Usage:
C:\github>dir
 Volume in drive C has no label.
 Volume Serial Number is B0DD-C53C

 Directory of C:\github

09/02/2012  12:08 PM    <DIR>          .
09/02/2012  12:08 PM    <DIR>          ..
09/02/2012  12:08 PM             6,723 fontfuzzer.py
09/02/2012  12:09 PM    <DIR>          fonts
               1 File(s)          6,723 bytes
               3 Dir(s)  32,938,553,344 bytes free

C:\github>python fontfuzzer.py fonts\unifont.ttf
GNU Unifont
0
GNU Unifont
10
GNU Unifont
20
GNU Unifont