# model settings
model = dict(
    type='ImageClassifier',
    backbone=dict(
        type='SwinTransformer', arch='tiny', img_size=224, drop_path_rate=0.2),
    neck=dict(type='GlobalAveragePooling'),
    head=dict(
        #type='LinearClsHead',
        type='MultiLabelLinearClsHead',
        num_classes=3,
        in_channels=768,
        init_cfg=None,  # suppress the default init_cfg of LinearClsHead.
        loss=dict(
            type='LabelSmoothLoss', label_smooth_val=0.1, mode='multi_label'),
            #type='CrossEntropyLoss', loss_weight=1.0, use_sigmoid=True),
        #cal_acc=False
        ),
    init_cfg=[
        dict(type='TruncNormal', layer='Linear', std=0.02, bias=0.),
        dict(type='Constant', layer='LayerNorm', val=1., bias=0.)
    ],
    train_cfg=dict(augments=[
        dict(type='BatchMixup', alpha=0.2, num_classes=3, prob=0.5),
        dict(type='BatchCutMix', alpha=1.0, num_classes=3, prob=0.5)
    ]))
