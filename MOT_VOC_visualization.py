import argparse
import cv2
import os

from src.utils_dataset import mot2voc_get_metadata
from src.utils import concat_root_path, ColorGenerator


def parse_args():
    parser = argparse.ArgumentParser(description='Generate the list of the files contained in a set of folders (for DL datasets).')
    parser.add_argument('--voc_path', dest='voc_path',
                        help='Dataset path where the VOC files will be stored.',
                        default=DATA_DIR_VOC, type=str)

    args = parser.parse_args()
    return args


def voc_visualize(data_dir_voc_seq):
    # Paths
    seq_path_voc = os.path.join(data_dir_voc_seq, 'img1')
    gt_path_voc = os.path.join(data_dir_voc_seq, 'gt')
    seq_id = os.path.basename(data_dir_voc_seq)

    # List img and XML files
    xml_list = os.listdir(gt_path_voc)
    xml_list.sort()
    img_list = [os.path.splitext(img_name)[0] + '.jpg' for img_name in xml_list]  # To maintain the order
    img_list_path = concat_root_path(seq_path_voc, img_list)
    xml_list_path = concat_root_path(gt_path_voc, xml_list)

    color_generator = ColorGenerator()

    for img_file, xml_file in zip(img_list_path, xml_list_path):
        img_info, obj_struct_list = mot2voc_get_metadata(xml_file)
        img = cv2.imread(img_file)

        for obj_struct in obj_struct_list:
            if obj_struct.label in labels_to_visualize:
                top_left = (obj_struct.bbox[0], obj_struct.bbox[1])
                bot_right = (obj_struct.bbox[0] + obj_struct.bbox[2], obj_struct.bbox[1] + obj_struct.bbox[3])
                color = tuple(color_generator.colors[int(obj_struct.obj_id)])
                color = tuple(map(int, color))  # From int64 to int
                cv2.rectangle(img, top_left, bot_right, color, 2)
                text_pos_x = bot_right[0] - 5
                text_pos_y = bot_right[1] - 5
                text_pos = (text_pos_x, text_pos_y)
                cv2.putText(img, obj_struct.label, text_pos, cv2.FONT_ITALIC, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('img', img)
        cv2.waitKey(10)


def main():
    args = parse_args()
    voc_visualize(args.voc_path)


if __name__ == '__main__':
    DATA_DIR_VOC = '/mnt/7C1A87F757CA1344/datasets/MOT17/MOT17_voc/train/MOT17-04'
    # DATA_DIR_VOC = '/work/agirbau/MOT/MOT17/MOT17_voc/train/MOT17-02'
    labels_to_visualize = ['1']
    # labels: ('__background__', 'pedestrian', 'person_on_vehicle', 'car', 'bicycle', 'motorbike',
    #                  'non_motorized_vehicle', 'static_person', 'distractor', 'occluder',
    #                  'occluder_on_the_ground', 'occluder_full', 'reflection')
    # labels: ('__background__', '1', '2', '3', '4', '5',
    #                  '6', '7', '8', '9',
    #                  '10', '11', '12')
    main()
