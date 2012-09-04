The FontFuzzer is created to fuzz the TrueType Font (TTF) into different sizes which enables the generation of test cases to determine the size of font in triggering the vulnerability. The overall process of the fuzzer starts with automating detect the 'FontName' and install the crafted font in Windows system. It will then display the font in a different size, uninstall the font file and repeat the process if no vulnerability is found.

Extra python packages needed: 1. pywin32-216.win32-py2.7

1.numpy-1.7.0b1-win32-superpack-python2.7
2.fonttools-2.3
3.comtypes-0.6.2.win32
Usage:

C:\github>python fontfuzzer.py fonts\unifont.ttf

GNU Unifont 0

GNU Unifont 10
