import xml.etree.ElementTree as ET
import csv
from os import listdir
from os.path import isfile, join

def read_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()

    return root


def get_ojects(xml_file_path, images_dirpath):
    root = read_xml(xml_file_path)
    cows = list()

    filename = root.find('filename').text

    for cow in root.findall('object'):

        # Get bounding box
        bbox = cow.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        xmax = int(bbox.find('xmax').text)
        ymin = int(bbox.find('ymin').text)
        ymax = int(bbox.find('ymax').text)

        # Store into the cow collection
        cows.append({'xmin': xmin, 'xmax': xmax, 'ymin': ymin, 'ymax': ymax, 'filename': join('images/', filename)})

    return cows


def arrange_annotations_file(annotation_dirpath, images_dirpath):
    files = [join(annotation_dirpath, i) for i in listdir(annotation_dirpath) if isfile(join(annotation_dirpath, i))]
    cows = []

    for file in files:
        boundaries = get_ojects(file, images_dirpath)
        for boundary in boundaries:
            cows.append(boundary)

    with open('annotations.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for cow in cows:
            print(cow)
            for i in cow:
                cow[i] = str(cow[i])
            filewriter.writerow([cow['filename'], cow['xmin'], cow['ymin'], cow['xmax'], cow['ymax'], 'cow'])


arrange_annotations_file('./Dataset/FriesianCattle2017/annotations', './Dataset/FriesianCattle2017/images')
