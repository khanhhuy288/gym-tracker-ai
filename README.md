# AI Gym Tracker
AI Gym Tracker is an app for counting reps of different exercises such as bicep 
curl, lateral raise, and overhead press, etc. with a webcam.  

The app is built using OpenCV for controlling the webcam, MediaPipe for pose 
estimation and Streamlit for building the web app.
## Installation
Clone the repository.
```
git clone <repo>
cd <repo>
```
Create a new virtual environment (called `gym_tracker_ai` in the example).
```
pip install virtualenv 
virtualenv gym_tracker_ai
```
Enter the virtual environment.
```
source gym_tracker_ai/bin/activate
```
Install the requirements in the current environment. 
```
pip install -r requirements.txt
```

## Usage
Run the Streamlit app in the browser.
```
streamlit run rep_count_app.py
```

Stay in front of the webcam so that all the involving joints of an exercise are visible. The app can currently detect in total 3 different exercises, which are:
* Bicep curl 

![Bicep curl](http://newlife.com.cy/wp-content/uploads/2019/11/23211301-Dumbbell-Standing-Inner-Biceps-Curl-version-2_Upper-Arms_360.gif)

* Overhead press

![Overhead press](https://modusx.de/wp-content/uploads/2021/04/military-press-weiter-griff.gif)
* Lateral raise

![Lateral raise](http://newlife.com.cy/wp-content/uploads/2019/11/22341301-Dumbbell-Standing-Lateral-Raise-female_Shoulders_360.gif)

## Contact
Huy Tran - khanhhuy288@gmail.com

Project Link: [https://github.com/khanhhuy288/gym_tracker_ai](https://github.com/khanhhuy288/gym_tracker_ai)

