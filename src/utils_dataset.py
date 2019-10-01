import copy
import os
import xml.etree.ElementTree as ET


# Variables
XML_EXT = '.xml'
ENCODE_METHOD = 'utf-8'


class ObjectStruct:
    def __init__(self):
        self.frame_id = None
        self.obj_id = None
        self.bbox = None  # left, top, width, height
        self.confidence = None
        self.label = None
        self.visibility = None

    def reset(self):
        self.__init__()

    def set_params(self, frame_id, obj_id, bbox, confidence, label, visibility):
        self.frame_id = frame_id
        self.obj_id = obj_id
        self.bbox = bbox  # left, top, width, height
        self.confidence = confidence
        self.label = label
        self.visibility = visibility


def indent(elem, level=0):
    # Taken from https://norwied.wordpress.com/2013/08/27/307/
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def mot2voc_set_metadata(meta_file, seq_path=None, seq_id=None, img_info=None, obj_struct=None):
    # Generate a file containing and ordering the metadata per frame
    flag_new_file = True
    if os.path.isfile(meta_file):
        flag_new_file = False
        tree = ET.parse(meta_file)
        root = tree.getroot()
    else:
        root = ET.Element('annotation')

        # Sequence information
        seq = ET.SubElement(root, 'seq')
        seq.text = seq_id
        seq_p = ET.SubElement(root, 'path')
        seq_p.text = seq_path

        # Camera frame information
        frame_size = ET.SubElement(root, 'size')
        height = ET.SubElement(frame_size, 'height')
        height.text = str(img_info[0])
        width = ET.SubElement(frame_size, 'width')
        width.text = str(img_info[1])
        depth = ET.SubElement(frame_size, 'depth')
        depth.text = str(img_info[2])

        frame_num = ET.SubElement(root, 'frame')
        frame_num.text = str(obj_struct.frame_id)

    # Object information
    object_info = ET.SubElement(root, 'object')
    obj_id = ET.SubElement(object_info, 'obj_id')
    obj_id.text = obj_struct.obj_id
    # Bbox
    bbox = ET.SubElement(object_info, 'bndbox')
    xleft = ET.SubElement(bbox, 'xleft')
    xleft.text = str(obj_struct.bbox[0])
    ytop = ET.SubElement(bbox, 'ytop')
    ytop.text = str(obj_struct.bbox[1])
    width = ET.SubElement(bbox, 'width')
    width.text = str(obj_struct.bbox[2])
    height = ET.SubElement(bbox, 'height')
    height.text = str(obj_struct.bbox[3])
    # Other information
    confidence = ET.SubElement(object_info, 'confidence')
    confidence.text = str(obj_struct.confidence)
    label = ET.SubElement(object_info, 'label')
    label.text = str(obj_struct.label)
    visibility = ET.SubElement(object_info, 'visibility')
    visibility.text = str(obj_struct.visibility)

    indent(root)
    if flag_new_file:
        tree = ET.ElementTree(root)

    tree.write(meta_file, xml_declaration=True, encoding='utf-8', method="xml")


def mot2voc_get_metadata(meta_file):
    # Generated a file containing and ordering the metadata per frame
    if not os.path.isfile(meta_file):
        return

    # Initialize object struct
    obj_struct_list = []

    # Parse element tree
    tree = ET.parse(meta_file)
    root = tree.getroot()

    # Sequence information
    seq = root.find('seq').text
    img_info = [[] for _ in range(3)]
    bbox = [[] for _ in range(4)]
    img_info_obj = root.find('size')
    img_info[0] = int(img_info_obj.find('width').text)
    img_info[1] = int(img_info_obj.find('height').text)
    img_info[2] = int(img_info_obj.find('depth').text)
    frame_id = root.find('frame').text

    obj_struct = ObjectStruct()

    for obj in root.iter('object'):
        # Object information
        obj_id = obj.find('obj_id').text
        confidence = float(obj.find('confidence').text)
        label = obj.find('label').text
        visibility = float(obj.find('visibility').text)

        # bbox
        obj_bbox = obj.find('bndbox')
        bbox[0] = int(obj_bbox.find('xleft').text)
        bbox[1] = int(obj_bbox.find('ytop').text)
        bbox[2] = int(obj_bbox.find('width').text)
        bbox[3] = int(obj_bbox.find('height').text)

        obj_struct.reset()
        obj_struct.set_params(frame_id, obj_id, bbox, confidence, label, visibility)
        obj_struct_list.append(copy.deepcopy(obj_struct))

    return img_info, obj_struct_list


def test_mot2voc_set_metadata():
    meta_file = 'tmp.xml'
    # seq_path = '/mnt/7C1A87F757CA1344/datasets/MOT17/MOT17Det/train'
    seq_path = '/imatge/agirbau/work/MOT/MOT17/MOT17Det/train'
    seq_id = 'MOT17-02'
    img_info = (1920, 1080, 3)

    obj_struct = ObjectStruct()
    obj_struct.set_params('1', '1', [912, 484, 97, 109], 0, 7, 1)
    mot2voc_set_metadata(meta_file, seq_path, seq_id, img_info, obj_struct)


def test_mot2voc_get_metadata():
    voc_xml_file = '/mnt/7C1A87F757CA1344/datasets/MOT17/MOT17_voc_test/000001.xml'
    mot2voc_get_metadata(voc_xml_file)


if __name__ == '__main__':
    # test_mot2voc_set_metadata()
    test_mot2voc_get_metadata()
