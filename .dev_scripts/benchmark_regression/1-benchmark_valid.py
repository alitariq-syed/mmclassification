import logging
import re
from argparse import ArgumentParser
from pathlib import Path
from time import time
from typing import OrderedDict

import numpy as np
import torch
from mmcv import Config
from mmcv.parallel import collate, scatter
from rich.console import Console
from rich.table import Table

from mmcls.apis import init_model
from mmcls.core.visualization.image import imshow_infos
from mmcls.datasets.imagenet import ImageNet
from mmcls.datasets.pipelines import Compose
from mmcls.utils import get_root_logger

console = Console()
MMCLS_ROOT = Path(__file__).absolute().parents[2]

CIFAR10_CLASSES = [
    'airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse',
    'ship', 'truck'
]

CIFAR100_CLASSES = [
    'apple', 'aquarium_fish', 'baby', 'bear', 'beaver', 'bed', 'bee', 'beetle',
    'bicycle', 'bottle', 'bowl', 'boy', 'bridge', 'bus', 'butterfly', 'camel',
    'can', 'castle', 'caterpillar', 'cattle', 'chair', 'chimpanzee', 'clock',
    'cloud', 'cockroach', 'couch', 'crab', 'crocodile', 'cup', 'dinosaur',
    'dolphin', 'elephant', 'flatfish', 'forest', 'fox', 'girl', 'hamster',
    'house', 'kangaroo', 'keyboard', 'lamp', 'lawn_mower', 'leopard', 'lion',
    'lizard', 'lobster', 'man', 'maple_tree', 'motorcycle', 'mountain',
    'mouse', 'mushroom', 'oak_tree', 'orange', 'orchid', 'otter', 'palm_tree',
    'pear', 'pickup_truck', 'pine_tree', 'plain', 'plate', 'poppy',
    'porcupine', 'possum', 'rabbit', 'raccoon', 'ray', 'road', 'rocket',
    'rose', 'sea', 'seal', 'shark', 'shrew', 'skunk', 'skyscraper', 'snail',
    'snake', 'spider', 'squirrel', 'streetcar', 'sunflower', 'sweet_pepper',
    'table', 'tank', 'telephone', 'television', 'tiger', 'tractor', 'train',
    'trout', 'tulip', 'turtle', 'wardrobe', 'whale', 'willow_tree', 'wolf',
    'woman', 'worm'
]

classes_map = {
    'ImageNet-1k': ImageNet.CLASSES,
    'CIFAR-10': CIFAR10_CLASSES,
    'CIFAR-100': CIFAR100_CLASSES
}


def parse_args():
    parser = ArgumentParser(description='Valid all models in model-index.yml')
    parser.add_argument(
        '--checkpoint-root',
        help='Checkpoint file root path. If set, load checkpoint before test.')
    parser.add_argument('--img', default='demo/demo.JPEG', help='Image file')
    parser.add_argument('--models', nargs='+', help='models name to inference')
    parser.add_argument('--show', action='store_true', help='show results')
    parser.add_argument(
        '--wait-time',
        type=float,
        default=1,
        help='the interval of show (s), 0 is block')
    parser.add_argument(
        '--inference-time',
        action='store_true',
        help='Test inference time by run 10 times for each model.')
    parser.add_argument(
        '--device', default='cuda:0', help='Device used for inference')
    args = parser.parse_args()
    return args


def inference(config_file, checkpoint, classes, args):
    cfg = Config.fromfile(config_file)

    model = init_model(cfg, checkpoint, device=args.device)
    model.CLASSES = classes

    # build the data pipeline
    if cfg.data.test.pipeline[0]['type'] != 'LoadImageFromFile':
        cfg.data.test.pipeline.insert(0, dict(type='LoadImageFromFile'))
    if cfg.data.test.type in ['CIFAR10', 'CIFAR100']:
        # The image shape of CIFAR is (32, 32, 3)
        cfg.data.test.pipeline.insert(1, dict(type='Resize', size=32))

    data = dict(img_info=dict(filename=args.img), img_prefix=None)

    test_pipeline = Compose(cfg.data.test.pipeline)
    data = test_pipeline(data)
    resolution = tuple(data['img'].shape[1:])
    data = collate([data], samples_per_gpu=1)
    if next(model.parameters()).is_cuda:
        # scatter to specified GPU
        data = scatter(data, [args.device])[0]

    # forward the model
    result = {'resolution': resolution}
    with torch.no_grad():
        if args.inference_time:
            time_record = []
            for _ in range(10):
                start = time()
                scores = model(return_loss=False, **data)
                time_record.append((time() - start) * 1000)
            result['time_mean'] = np.mean(time_record[1:-1])
            result['time_std'] = np.std(time_record[1:-1])
        else:
            scores = model(return_loss=False, **data)

        pred_score = np.max(scores, axis=1)[0]
        pred_label = np.argmax(scores, axis=1)[0]
        result['pred_label'] = pred_label
        result['pred_score'] = float(pred_score)
    result['pred_class'] = model.CLASSES[result['pred_label']]

    result['model'] = config_file.stem

    return result


def show_summary(summary_data):
    table = Table(title='Validation Benchmark Regression Summary')
    table.add_column('Model')
    table.add_column('Validation')
    table.add_column('Resolution (h, w)')
    table.add_column('Inference Time (std) (ms/im)')

    for model_name, summary in summary_data.items():
        row = [model_name]
        valid = summary['valid']
        color = 'green' if valid == 'PASS' else 'red'
        row.append(f'[{color}]{valid}[/{color}]')
        if valid == 'PASS':
            row.append(str(summary['resolution']))
            if 'time_mean' in summary:
                time_mean = f"{summary['time_mean']:.2f}"
                time_std = f"{summary['time_std']:.2f}"
                row.append(f'{time_mean}\t({time_std})'.expandtabs(8))
        table.add_row(*row)

    console.print(table)


# Sample test whether the inference code is correct
def main(args):
    model_index_file = MMCLS_ROOT / 'model-index.yml'
    model_index = Config.fromfile(model_index_file)
    models = OrderedDict()
    for file in model_index.Import:
        metafile = Config.fromfile(MMCLS_ROOT / file)
        models.update({model.Name: model for model in metafile.Models})

    logger = get_root_logger(
        log_file='benchmark_test_image.log', log_level=logging.INFO)

    if args.models:
        patterns = [re.compile(pattern) for pattern in args.models]
        filter_models = {}
        for k, v in models.items():
            if any([re.match(pattern, k) for pattern in patterns]):
                filter_models[k] = v
        if len(filter_models) == 0:
            print('No model found, please specify models in:')
            print('\n'.join(models.keys()))
            return
        models = filter_models

    summary_data = {}
    for model_name, model_info in models.items():

        config = Path(model_info.Config)
        assert config.exists(), f'{model_name}: {config} not found.'

        logger.info(f'Processing: {model_name}')

        http_prefix = 'https://download.openmmlab.com/mmclassification/'
        dataset = model_info.Results[0]['Dataset']
        if args.checkpoint_root is not None:
            root = Path(args.checkpoint_root)
            checkpoint = root / model_info.Weights[len(http_prefix):]
        else:
            checkpoint = None

        try:
            # build the model from a config file and a checkpoint file
            result = inference(MMCLS_ROOT / config, str(checkpoint),
                               classes_map[dataset], args)
            result['valid'] = 'PASS'
        except Exception as e:
            logger.error(f'"{config}" : {repr(e)}')
            result = {'valid': 'FAIL'}

        summary_data[model_name] = result
        # show the results
        if args.show:
            imshow_infos(args.img, result, wait_time=args.wait_time)

    show_summary(summary_data)


if __name__ == '__main__':
    args = parse_args()
    main(args)
