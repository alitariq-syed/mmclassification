_base_ = [
    '../_base_/models/swin_transformer/tiny_224_TBX11K.py',
    '../_base_/datasets/Local_data_finetune_bs64_swin_224.py',
    '../_base_/schedules/TBX11K_bs1024_adamw_swin.py',
    '../_base_/default_runtime.py'
]
