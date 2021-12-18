# dataset settings
dataset_base = 'Decathlon'
dataset_type = 'DecathlonLiverDataset'
data_root = 'data/Decathlon/3D/Task03_Liver'
img_norm_cfg = dict(
    mean=[0], std=[255], to_rgb=False)
crop_size = (224, 224)
pp_ct_window = True
ct_window = [-21, 189]
interpolate_voxel_spacing = False
voxel_spacing = 1.0
train_pipeline = [
    dict(type='LoadImageFromFile', color_type='grayscale'),
    dict(type='LoadAnnotations', reduce_zero_label=True),
    dict(type='Resize', img_scale=(768, 512), ratio_range=(0.75, 1.5)),
    dict(type='RandomCrop', crop_size=crop_size, cat_max_ratio=0.75),
    dict(type='RandomFlip', prob=0.2),
    #dict(type='RandomRotate', prob=0.1),
    #dict(type='PhotoMetricDistortion'),
    dict(type='Normalize', **img_norm_cfg),
    #dict(type='Pad', size=crop_size, pad_val=0, seg_pad_val=255),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_semantic_seg']),
]
test_pipeline = [
    dict(type='LoadImageFromFile', color_type='grayscale'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(224, 224),
        # img_ratios=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75],
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip', prob=0.),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img']),
        ])
]
data = dict(
    samples_per_gpu=32,
    workers_per_gpu=8,
    train=dict(
        type=dataset_type,
        data_root=data_root,
        img_dir='img_dir/train',
        ann_dir='ann_dir/train',
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        data_root=data_root,
        img_dir='img_dir/val',
        ann_dir='ann_dir/val',
        pipeline=test_pipeline))
