# Empty Meat Detection

The main idea is to develop a tool that is capable of detecting when a product, inside the meat cubicle, has been exhausted and launch an alert to the store employees to recharge the product stock.

The approach that has been used has been the identification of colors for empty spaces. For this strategy to make sense, the trays where the meat part is located should be changed to a specific color, in this case we will use green, but we can configure any color to be recognized. The green color has been chosen because it is the one that provides the most contrast.

For this strategy we have used the OpenCV library to help us with object and area recognition. What the system does is recognize the areas within a range of colors in BGR and look for the contours of each match. For each match we carry out a validation and thus determine if it is only noise or an empty space.

For filtering green objects that aren't inside the meat fridge we will discard the following features:
* Points within ABC triangle
* Points within DEF triangle
* Points at the right of C
* Points with lower are than 300

![Filtering points ](localstore/1606609738/frame2.jpg)

To be coherent with the image sizes and avoid recognition problems, all points are calculated using a ponderation of the image shapes starting on the base that we know about the fridge coordinates from the 1920x1080 images.

## Start project 🚀

_These instructions will allow you to get a copy of the project running on your local machine for development and testing purposes._

See **Deployment** to know how to deploy the project.


### Pre-requirements 📋

```
click==7.1.2
Flask==1.1.2
Flask-HTTPAuth==4.2.0
itsdangerous==1.1.0
Jinja2==2.11.2
MarkupSafe==1.1.1
numpy==1.19.4
opencv-contrib-python-headless==4.4.0.46
opencv-python-headless==4.4.0.46
Werkzeug==1.0.1
```

### Installation 🔧

```
$ https://github.com/Rochii/EmptyMeatDetection.git
$ pip install -r requirements.txt
```

## Run tests ⚙️

**You must configure your own directory paths within the classes/scripts/module.py file.** 
_To run the Flask server in local run:_
```
$ python app.py
```

_Now we have to post the request and await for response. We can use Postman tool, curl, ..._

```
curl -H "Accept: application/json" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer 2b7ef86ff94561072baa6b86323de061" \
     -X POST \
     -d '{"frame" : {base64img}' \
     http://localhost:5000/detect
```

### After tests 🔩
#### Original image:
![Original Image](images/tests/green_noise2.jpg)

#### Response image received from the response (base64 decoded for showing)
![Tracted Image](localstore/1606613721/frame.jpg)

and the response json (without the base64 explicitly):
```
{
    "attributes": {
        "base64image": "{base64_img}",
        "empty_holes": 9
    },
    "code": "200",
    "id": "1606618859",
    "status": "Success"
}
```

## Deployment 📦

_To deploy the project it's **HIGHLY RECOMENDABLE** to use _Nginx_ as a web server and _Gunicorn_ to run the python Flask application._

## Build with 🛠️

* [Python3.8](https://www.python.org/downloads/release/python-386/) - Python language
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Python framework
* [OpenCV](https://opencv.org/) - Computer Vision Library

## Authors ✒️

* **Roger Truchero Visa** - [Rochii](https://github.com/Rochii)