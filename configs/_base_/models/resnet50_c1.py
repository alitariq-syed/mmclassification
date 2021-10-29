# model settings
model = dict(
    type='ImageClassifier',
    backbone=dict(
        type='ResNet',
        depth=50,
        num_stages=4,
        out_indices=(3, ),
        style='pytorch'),
    neck=dict(type='GlobalAveragePooling'),
    head=dict(
        type='MultiLabelLinearClsHead',
        num_classes=3,
        in_channels=2048,
        loss=#[
        	dict(type='CrossEntropyLoss', loss_weight=1.0, use_sigmoid=True),
        #	dict(type='LabelSmoothLoss',
        #    loss_weight=1.0,
        #    label_smooth_val=0.1,
        #    num_classes=3,mode='classy_vision')
            #],
        #topk=(1, 5),
    ),
    
train_cfg=dict(
        augments=[
        	dict(type='BatchMixup', alpha=0.2, num_classes=3,prob=.5),
              	dict(type='BatchCutMix', alpha=1.0, num_classes=3, prob=.5),
                      ]),

)

