import argparse
import csv
import multiprocessing as mp
import os

from PIL import Image
from src.utils import check_and_create, concat_root_path, Timer
from src.utils_dataset import mot2voc_set_metadata, ObjectStruct


def parse_args():
    parser = argparse.ArgumentParser(description='Generate the list of the files contained in a set of folders (for DL datasets).')
    parser.add_argument('--mot_path', dest='mot_path',
                        help='Dataset path where the MOT files will be read.',
                        default=DATA_DIR_MOT, type=str)
    parser.add_argument('--voc_path', dest='voc_path',
                        help='Dataset path where the VOC files will be stored.',
                        default=DATA_DIR_VOC, type=str)

    args = parser.parse_args()
    return args


def mot_to_voc(data_dir_mot_seq, data_dir_voc_seq):
    # Paths
    seq_path_mot = os.path.join(data_dir_mot_seq, 'img1')
    seq_path_voc = os.path.join(data_dir_voc_seq, 'img1')
    gt_path_mot = os.path.join(data_dir_mot_seq, 'gt')
    gt_file_mot = os.path.join(gt_path_mot, 'gt.txt')
    gt_path_voc = os.path.join(data_dir_voc_seq, 'gt')
    seq_id = os.path.basename(data_dir_mot_seq)

    # Flag to check if there's a ground truth file
    flag_gt = os.path.isfile(gt_file_mot)

    # Generate unexisting paths
    check_and_create(data_dir_voc_seq)
    check_and_create(seq_path_voc)
    if flag_gt:
        check_and_create(gt_path_voc)

    # Generate softlinks to MOT dataset
    frames_mot = os.listdir(seq_path_mot)
    frames_mot_path = concat_root_path(seq_path_mot, frames_mot)
    frames_voc_path = concat_root_path(seq_path_voc, frames_mot)
    for f_m, f_v in zip(frames_mot_path, frames_voc_path):
        if not os.path.exists(f_v):
            os.symlink(f_m, f_v)
        else:
            print('Assuming files are generated for ' + seq_id + '. If not, delete ' + data_dir_voc_seq + ' and run the script again.')
            return

    # If there's no ground truth file finish here (only generate the softlinks).
    if not flag_gt:
        return

    # Get img info from the first image
    img_0 = Image.open(os.path.join(seq_path_mot, '000001.jpg'))
    img_w, img_h = img_0.size
    img_c = len(img_0.getbands())  # ['R', 'G', 'B']

    print("Generating metadata for: " + seq_id)

    # Initialize object
    obj_struct = ObjectStruct()

    with open(gt_file_mot, 'r') as r_gt_mot:
        reader = csv.reader(r_gt_mot)
        for row in reader:
            # Link frame with frame file and xml
            frame_id = int(row[0])
            frame_id_name = '{:06d}'.format(frame_id)
            frame_id_name_xml = frame_id_name + '.xml'

            meta_file = os.path.join(gt_path_voc, frame_id_name_xml)

            # Bbox info
            obj_id = row[1]
            bbox = row[2:6]  # left, top, width, height
            confidence = row[6]
            label = row[7]
            visibility = row[8]
            obj_struct.set_params(frame_id, obj_id, bbox, confidence, label, visibility)

            # Generate XML
            mot2voc_set_metadata(meta_file, seq_path=seq_path_voc, seq_id=seq_id,
                                 img_info=(img_w, img_h, img_c), obj_struct=obj_struct)

            obj_struct.reset()


def main():
    args = parse_args()
    # For each folder generate an XML per frame --> open and close depending on the frame (txt is ordered by object, not by frame).
    mot_train = os.path.join(args.mot_path, 'train')
    mot_test = os.path.join(args.mot_path, 'test')
    voc_train = os.path.join(args.voc_path, 'train')
    voc_test = os.path.join(args.voc_path, 'test')

    # Check and create path for VOC-like dataset
    check_and_create(args.voc_path)
    check_and_create(voc_train)
    check_and_create(voc_test)

    # Pairs of sequences (mot-like and voc-like)
    mot_train_seqs = os.listdir(mot_train)
    mot_train_seqs_path = concat_root_path(mot_train, mot_train_seqs)
    voc_train_seqs_path = concat_root_path(voc_train, mot_train_seqs)
    mot_voc_train_pairs = [p for p in zip(mot_train_seqs_path, voc_train_seqs_path)]

    mot_test_seqs = os.listdir(mot_test)
    mot_test_seqs_path = concat_root_path(mot_test, mot_test_seqs)
    voc_test_seqs_path = concat_root_path(voc_test, mot_test_seqs)
    mot_voc_test_pairs = [p for p in zip(mot_test_seqs_path, voc_test_seqs_path)]

    with mp.Pool(processes=6) as p, Timer('timer_mot_to_voc'):
        p.starmap(mot_to_voc, mot_voc_train_pairs)
        p.starmap(mot_to_voc, mot_voc_test_pairs)


if __name__ == '__main__':
    DATA_DIR_MOT = '/mnt/7C1A87F757CA1344/datasets/MOT17/MOT17Det'
    DATA_DIR_VOC = '/mnt/7C1A87F757CA1344/datasets/MOT17/MOT17_voc'
    # DATA_DIR_MOT = '/imatge/agirbau/work/MOT/MOT17/MOT17Det'
    # DATA_DIR_VOC = '/imatge/agirbau/work/MOT/MOT17/MOT17_voc'
    main()
