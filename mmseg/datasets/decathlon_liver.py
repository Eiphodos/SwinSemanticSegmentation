from .builder import DATASETS
from .custom import CustomDataset


@DATASETS.register_module()
class DecathlonLiverDataset(CustomDataset):
    """Decathlon Liver dataset.

    In segmentation map annotation for Decathlon Liver, 0 stands for background.
    ``reduce_zero_label`` is fixed to False.
    The ``img_suffix`` is fixed to '.png' and ``seg_map_suffix`` is fixed to
    '.png'.
    """
    CLASSES = ('background', 'liver', 'cancer')

    PALETTE = [[100, 200, 100], [20, 230, 230], [200, 50, 50]]

    def __init__(self, **kwargs):
        super(DecathlonLiverDataset, self).__init__(
            img_suffix='.png',
            seg_map_suffix='.png',
            reduce_zero_label=False,
            **kwargs)
