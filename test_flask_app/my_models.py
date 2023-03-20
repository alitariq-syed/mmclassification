from mmseg.apis import init_segmentor, inference_segmentor, show_result_pyplot
from mmseg.core.evaluation import get_palette


def initialize_mmseg_model():
    try:
        config_file = 'mmsegmentation/configs/pspnet/pspnet_r50-d8_512x1024_40k_cityscapes.py'
        checkpoint_file = 'pspnet_r50-d8_512x1024_80k_cityscapes_20200606_112131-2376f12b.pth'

        # build the model from a config file and a checkpoint file
        print("---------loading mmseg model...")
        model = init_segmentor(config_file, checkpoint_file, device='cuda:0')
        print("---------mmseg model loaded!")
        return model
    except Exception as e:
        print ("---------error in loading mmseg model: ", e)

def infer_mmseg_model(model, img):
    result = inference_segmentor(model, img)
    return result