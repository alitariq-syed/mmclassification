# #
# #1. Convert model from MMSegmentation to TorchServe
# python mmsegmentation/tools/torchserve/mmseg2torchserve.py mmsegmentation/configs/pspnet/pspnet_r50-d8_512x1024_40k_cityscapes.py pspnet_r50-d8_512x1024_80k_cityscapes_20200606_112131-2376f12b.pth --output-folder mmserve_models --model-name pspnet

# #2. Build mmseg-serve docker image
# docker build -t mmseg-serve:latest mmsegmentation/docker/serve/

# #3  Run mmseg-serve
# docker run --rm --cpus 8 --gpus device=0 -p8080:8080 -p8081:8081 -p8082:8082 --mount type=bind,source=mmserve_models,target=/home/model-server/model-store mmseg-serve:latest

# #4. Test deployment
# curl -O https://raw.githubusercontent.com/open-mmlab/mmsegmentation/master/resources/3dogs.jpg
# curl http://127.0.0.1:8080/predictions/${MODEL_NAME} -T 3dogs.jpg -o 3dogs_mask.png