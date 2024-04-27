import sys
from pathlib import Path

from PIL import Image

from utils_ootd import get_mask_location

PROJECT_ROOT = Path(__file__).absolute().parents[1].absolute()
sys.path.insert(0, str(PROJECT_ROOT))

from preprocess.openpose.run_openpose import OpenPose
from preprocess.humanparsing.run_parsing import Parsing
from ootd.inference_ootd_hd import OOTDiffusionHD

openpose_model = OpenPose(0)
parsing_model = Parsing(0)
model = OOTDiffusionHD(0)

model_type = 'hd'
image_scale = 1.0
n_steps = 1
n_samples = 5
seed = -1

category_dict = ['upperbody', 'lowerbody', 'dress']
category_dict_utils = {
    'upperbody': 'upper_body',
    'lowerbody': 'lower_body',
    'dress': 'dresses'
}


def try_on_cloth(model_path: str, cloth_path: str, category: str):
    cloth_img = Image.open(cloth_path).resize((768, 1024))
    model_img = Image.open(model_path).resize((768, 1024))
    keypoints = openpose_model(model_img.resize((384, 512)))
    model_parse, _ = parsing_model(model_img.resize((384, 512)))

    mask, mask_gray = get_mask_location(model_type, category_dict_utils.get(category), model_parse, keypoints)
    mask = mask.resize((768, 1024), Image.NEAREST)
    mask_gray = mask_gray.resize((768, 1024), Image.NEAREST)

    masked_vton_img = Image.composite(mask_gray, model_img, mask)

    images = model(
        model_type=model_type,
        category=category,
        image_garm=cloth_img,
        image_vton=masked_vton_img,
        mask=mask,
        image_ori=model_img,
        num_samples=n_samples,
        num_steps=n_steps,
        image_scale=image_scale,
        seed=seed,
    )

    return images[0]
