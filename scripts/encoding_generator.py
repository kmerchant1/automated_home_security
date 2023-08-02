import cv2
import face_recognition
import pickle
import os


#importing the images of verified people
img_path = '../verified_images'
path_list = [f for f in os.listdir(img_path) if not f.startswith('.')]

img_list = []
id_list = []
for img in path_list:
    img_list.append(cv2.imread(os.path.join(img_path,img)))
    id_list.append(os.path.splitext(img)[0])


#generate encodings for each image in our verified_images folder
def generate_encodings(img_list):
    '''
    Takes in a list of images and generates encodings (using face_recognition) for each image in the list
    
    Args:
        img_list --> list of image paths
    Returns:
        encode_list --> list of encodings for each of the images
    
    '''
    encode_list = []
    for img in img_list:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoding = face_recognition.face_encodings(img)[0]
        encode_list.append(encoding)
    
    return encode_list

print('Starting Encoding...')
verified_encodings = generate_encodings(img_list)
verified_encodings_with_id = [verified_encodings, id_list]
print('Encoding Complete')

#save known encodings and id's to a file for importing later
verified_file = open('../resources/verified_file.p', 'wb')
pickle.dump(verified_encodings_with_id, verified_file)
verified_file.close()
print('verified file saved')