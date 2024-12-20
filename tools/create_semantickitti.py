import argparse
from os import path as osp
from pathlib import Path

import mmengine

total_num = {
    0: 4541,
    1: 1101,
    2: 4661,
    3: 801,
    4: 271,
    5: 2761,
    6: 1101,
    7: 1101,
    8: 4071,
    9: 1591,
    10: 1201,
}
fold_split = {
    'train': [ 1, 2, 3, 4, 5, 6, 7,8 ],
    'val': [9],
    'trainval': [ 1, 2, 3, 4, 5, 6, 7, 8, 9, ],
    'test': [10],
}
split_list = ['train', 'valid', 'trainval', 'test']


def get_semantickitti_info(split: str) -> dict:
    data_infos = dict()
    data_infos['metainfo'] = dict(dataset='SemanticKITTI')
    data_list = []
    for i_folder in fold_split[split]:
        for j in range(total_num[i_folder]):
            data_list.append({
                'lidar_points': {
                    'lidar_path':
                    osp.join('sequences',
                             str(i_folder).zfill(2), 'velodyne',
                             str(j).zfill(6) + '.bin'),
                    'num_pts_feats':
                    4
                },
                'pts_semantic_mask_path':
                osp.join('sequences',
                         str(i_folder).zfill(2), 'labels',
                         str(j).zfill(6) + '.label'),
                'sample_idx':
                str(i_folder).zfill(2) + str(j).zfill(6)
            })
    data_infos.update(dict(data_list=data_list))
    return data_infos


def create_semantickitti_info_file(pkl_prefix: str, save_path: str) -> None:
    print('Generate info.')
    save_path = Path(save_path)

    semantickitti_infos_train = get_semantickitti_info(split='train')
    filename = save_path / f'{pkl_prefix}_infos_train.pkl'
    print(f'SemanticKITTI info train file is saved to {filename}')
    mmengine.dump(semantickitti_infos_train, filename)

    semantickitti_infos_val = get_semantickitti_info(split='val')
    filename = save_path / f'{pkl_prefix}_infos_val.pkl'
    print(f'SemanticKITTI info val file is saved to {filename}')
    mmengine.dump(semantickitti_infos_val, filename)

    semantickitti_infos_trainval = get_semantickitti_info(split='trainval')
    filename = save_path / f'{pkl_prefix}_infos_trainval.pkl'
    print(f'SemanticKITTI info trainval file is saved to {filename}')
    mmengine.dump(semantickitti_infos_trainval, filename)

    semantickitti_infos_test = get_semantickitti_info(split='test')
    filename = save_path / f'{pkl_prefix}_infos_test.pkl'
    print(f'SemanticKITTI info test file is saved to {filename}')
    mmengine.dump(semantickitti_infos_test, filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data converter arg parser')
    parser.add_argument(
        '--out-dir',
        type=str,
        default='./data/semantickitti',
        required=False,
        help='output path of pkl')
    parser.add_argument('--extra-tag', type=str, default='semantickitti')
    args = parser.parse_args()
    create_semantickitti_info_file(args.extra_tag, args.out_dir)
