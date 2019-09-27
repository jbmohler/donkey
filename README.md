# donkey

This project aspires to be an analog sudoku solver containing a sudoku solving
engine, an image recognition component picking sudoku puzzles out of image
files, and a web server receiving photo files and returning solutions.  It's
merely a toy for me to convince myself I can do this end-to-end.

In the testvision folder there is a fledgling sudoku square connector.  It
hopefully detects a critical mass of lines to be able to rotate the sudoku
square to be oriented with lines parallel to the respective image sides.

```bash
# be in a virtual env
cd testvision
pip install -r requirements.txt
python intersections.py <image-file>
```
