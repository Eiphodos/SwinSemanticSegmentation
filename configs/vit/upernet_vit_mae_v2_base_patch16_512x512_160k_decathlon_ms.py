_base_ = [
    '../_base_/models/upernet_vit_mae_v2.py', '../_base_/datasets/decathlon_liver.py',
    '../_base_/default_runtime.py', '../_base_/schedules/schedule_160k.py'
]

crop_size = (512, 512)

model = dict(
    backbone=dict(
        img_size=512,
        embed_dim=768,
        depth=12,
        num_heads=12,
        patch_size=16,
        in_chans=1,
        num_classes=1000,
        use_abs_pos_emb=True,
        use_rel_pos_bias=True
    ),
    decode_head=dict(
        in_channels=[768, 768, 768, 768],
        num_classes=3,
        channels=768
    ),
    auxiliary_head=dict(
        in_channels=768,
        num_classes=3
    ),
    test_cfg = dict(mode='slide', crop_size=crop_size, stride=(341, 341))
)

# AdamW optimizer, no weight decay for position embedding & layer norm in backbone
#optimizer = dict(_delete_=True, type='AdamW', lr=0.00006, betas=(0.9, 0.999), weight_decay=0.01,
#                 paramwise_cfg=dict(custom_keys={'absolute_pos_embed': dict(decay_mult=0.),
#                                                 'relative_position_bias_table': dict(decay_mult=0.),
#                                                 'norm': dict(decay_mult=0.)}))

optimizer = dict(_delete_=True, type='AdamW', lr=7e-4, betas=(0.9, 0.999), weight_decay=0.05,
                 constructor='LayerDecayOptimizerConstructor',
                 paramwise_cfg=dict(num_layers=12, layer_decay_rate=0.65))

lr_config = dict(_delete_=True, policy='poly',
                 warmup='linear',
                 warmup_iters=1500,
                 warmup_ratio=1e-6,
                 power=1.0, min_lr=0.0, by_epoch=False)


img_norm_cfg = dict(
    mean=[0], std=[255], to_rgb=False)
crop_size = (512, 512)

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', reduce_zero_label=False),
    dict(type='Resize', img_scale=(2048, 512), ratio_range=(0.5, 2.0)),
    dict(type='RandomCrop', crop_size=crop_size, cat_max_ratio=0.75),
    dict(type='RandomFlip', prob=0.5),
    dict(type='PhotoMetricDistortion'),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='Pad', size=crop_size, pad_val=0, seg_pad_val=255),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_semantic_seg']),
]

test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(2048, 512),
        #img_ratios=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75],
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img']),
        ])
]
# By default, models are trained on 8 GPUs with 2 images per GPU
data = dict(
    samples_per_gpu=8,
    workers_per_gpu=8,
    train=dict(pipeline=train_pipeline),
    val=dict(pipeline=test_pipeline),
    test=dict(pipeline=test_pipeline))