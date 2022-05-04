
import os
import random
from isort import file
from matplotlib.image import imread
from PIL import Image
import numpy as np
from base64 import b64encode
from io import BytesIO


# pour langestion de l'API custum vision

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid

def open_waste_slot():

    """
        open the machine so that
        a user can enter the machine
    :return:
    """

    send_command_to_machine("open_waste_slot")
    return True


def close_waste_slot():
    """
    close the waste box for user safety
    :return:
    """

    send_command_to_machine("close_waste_slot")
    return True


def process_waste(waste_type):

    """
    move the good slot and shredd the waste
    :return:
    """

    move_container(waste_type)
    was_sucessful = shred_waste()

    return was_sucessful


def move_container(waste_type):

    BOTTLE_BOX = 0
    GLASS_BOX = 1
    command_name = "move_container"

    if waste_type == "bottle":
        send_command_to_machine(command_name, BOTTLE_BOX)
    elif waste_type == "glass":
        send_command_to_machine(command_name, GLASS_BOX)

    return True


def send_command_to_machine(command_name, value=None):

    """
    simulate command sending to rasberry pi
    do nothing to work even if the machine is not connected

    :param command_name:
    :param value:
    :return:
    """
    return True



def shred_waste():

    send_command_to_machine("shred_waste")

    return True


def take_trash_picture():

    """
        function simulating the picture taking
        inside the machine. 

        Call this function to ask the machine to 
        take picture of the trash

        return : np array of the picture
    """

    send_command_to_machine("take_picture")

    # global paths # recherche immédiatement les elements dont on a besoin
    # global img
    paths = os.listdir('/Users/enyonadjanor/IA-P2-Euskadi-Enyon/Projets/Projet P8 - Triof/triof/camera')
    path = random.choice(paths)
    path_return = path

    return (imread(os.path.join("/Users/enyonadjanor/IA-P2-Euskadi-Enyon/Projets/Projet P8 - Triof/triof/camera", path)),path_return)

picture, path_return = take_trash_picture()
PIL_image = Image.fromarray(np.uint8(picture)).convert('RGB')
data = BytesIO()
PIL_image.save(data, "JPEG")
data64 = b64encode(data.getvalue())
PIL_image = u'data:img/jpeg;base64,'+data64.decode('utf-8')

def predictions(img):

    ENDPOINT = "https://cgcustomvision-prediction.cognitiveservices.azure.com/"
    prediction_key = "33463958a6a048f48c49653b457e0853"
    project_id = "ef16960a-94fe-468f-a42b-3e8ea8fc1483"
    published_name = "Iteration1"
    prediction_resource_id = "/subscriptions/9b9c4a7a-4f40-4fc2-ab99-0bbe0c4064bd/resourceGroups/IA_Christian/providers/Microsoft.CognitiveServices/accounts/CGCustomVision-Prediction"
    file_location = "/Users/enyonadjanor/IA-P2-Euskadi-Enyon/Projets/Projet P8 - Triof/triof/camera/"


    prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
    print(prediction_credentials)
    predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)
   

    with open(os.path.join (file_location ,img), "rb") as image_contents:
        results = predictor.classify_image(
            image_data=image_contents.read(),
            project_id=project_id,
            published_name=published_name)
       
        tag_image = " ",
        proba_predict =  0
            

        for prediction in results.predictions:
            if prediction.probability > proba_predict:
                tag_image = prediction.tag_name
                proba_predict = prediction.probability
        # result = tag_image  + ":{0: .2f}%".format(proba_predict*100)

    return tag_image, proba_predict


from keras.models import load_model
from keras import preprocessing

def clean_or_dirty(img):
    #load the saved model
    classifier = load_model("/Users/enyonadjanor/IA-P2-Euskadi-Enyon/Projets/Projet P8 - Triof/triof/model_tl")
    path = "/Users/enyonadjanor/IA-P2-Euskadi-Enyon/Projets/Projet P8 - Triof/triof/camera"
    #prediction
    image_address = os.path.join (path, img)
    img = preprocessing.image.load_img(image_address,target_size=(64,64))
    img = np.asarray(img)
    img = np.expand_dims(img, axis=0)

    # make prediction

    #making prediction for output 

    output = classifier.predict(img)[0][0]

    print(output)

    #returning prediction
    res = ""
    if output <= 0.5:
        res = 'Item is clean'
    else:
        res = 'Item is dirty'
    return res