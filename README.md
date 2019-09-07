# CricAnalysis [cricket video processing with python 3.7]

Goal of this project is to capture image when ball hits the bat

How to : <br>
1 - OpenCV (real-time computer vision library) <br>
2 - Remove background by masking<br>
3 - Use colours to detect objects <br>
4 - Draw a contour around the identified color & size <br>
5 - Check where these 2 objects are colliding <br>
6 - Save that frame as image <br>
<br>
Factors affecting detection of object:<br>
- multiple objects of same color present in the video [same area size is another problem]<br>
- no proper lighting to detect the object. [Need to update HSV values real-time for this]<br>
- distance tracked can be 3ft. [Assumption based on certain findings]