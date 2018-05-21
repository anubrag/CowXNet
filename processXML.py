import xml.etree.ElementTree as ET

def read_xml(xml_file):

    tree = ET.parse(xml_file)
    root = tree.getroot()

    return root

def get_ojects(root):

    cows = dict()

    for cow in root.findall('object'):
        # Get cow ID
        cow_id = cow.find('name').text

        # Get bounding box
        bbox = cow.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        xmax = int(bbox.find('xmax').text)
        ymin = int(bbox.find('ymin').text)
        ymax = int(bbox.find('ymax').text)

        # Store into the cow collection
        cows[cow_id] = {'xmin': xmin, 'xmax': xmax, 'ymin': ymin, 'ymax': ymax}

    return cows
