setlocal ENABLEDELAYEDEXPANSION

cd %CD% 
copy /b *.txt temp1.txt

findstr /V "+---------+---------------+----------+" temp1.txt > temp2.txt

set word=|
set str="   ETHER"
call set str=%%str:chair=%word%%%
echo %str%
