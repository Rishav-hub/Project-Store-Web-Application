# Project Title

This is a FastAPI based web application that is used to store all your projects.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Make sure you have the following prerequisites installed:
- MySQL [Windows](https://dev.mysql.com/downloads/windows/installer/8.0.html)


### Installing

#### 1. Environment setup.
```commandline
conda create --prefix ./env python=3.7 -y
conda activate ./env
```

#### 2. Install Requirements
```commandline
pip install -r requirements.txt
```

#### 3. Run the setup
```commandline
pip install -e .
```
#### 4. Execute this file to generate key for Database

```commandline
python generateKey.py 
```
- After executing this command you will get a secret.key file, now copy the 
secret key and save it into your environment variable as DATABASE_KEY and run this file again to encrypt

- Also add the SECRET_KEY and ALGORITHM to be used to your environment variables

#### 5. Run Application
windows
```commandline
python app.py 
```
## Docker  Integration 

1. Build Image 
```
docker build -t Image_name .
```
2. Create and run container
```
docker run -p 8000:8080 Image_name
```
3. Stop running container
```
docker stop container_ID
```
4. start container 
```
docker start container_ID
```

## Interface

Login page
![Login](https://user-images.githubusercontent.com/57321948/163331626-d6c9b97b-f3ee-4780-a43a-2acedadde2c6.JPG)

Register Page
![Register](project_store_presentation_layer/img/register.JPG)

Home Page
![home1](https://user-images.githubusercontent.com/57321948/163331708-89a54491-6c7e-426a-8d62-2b446b3f1603.JPG)
![home2](https://user-images.githubusercontent.com/57321948/163331716-b8ec4d6b-2862-4df5-b0c6-50a9c929d796.JPG)

View App Page
![view_app](https://user-images.githubusercontent.com/57321948/163331760-3a17d529-94d8-4497-8cf4-4b71378140e5.JPG)

Add App Page
![add_app](https://user-images.githubusercontent.com/57321948/163331787-fa64e0bf-d26b-4131-8536-bc1b35f1cca8.JPG)


## Built With

* [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
* [MySQL](https://dev.mysql.com/downloads/windows/) - Database

## Authors

* **iNeuron Private Limited** - *Initial work* - [iNeuron-Pvt-Ltd](https://github.com/iNeuron-Pvt-Ltd)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


