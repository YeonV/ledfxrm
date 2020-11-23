@echo off
title yzledfx
MODE CON COLS=30 LINES=3
E:

set root=E:\Users\Blade\anaconda3

call %root%\Scripts\activate.bat led

call cd dev

call ledfx -v
