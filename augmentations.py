"""
Registry of Albumentations augmentations with parameter metadata for the UI.
Compatible with albumentations >= 1.3, < 2.0
"""

import albumentations as A

# Each entry: (param_name, type, default, min, max, step)
# type is one of: "int", "float", "bool", "select"
# For "select": (param_name, "select", default, [options])

AUGMENTATION_REGISTRY = {
    # ── Geometric ──
    "HorizontalFlip": {
        "class": A.HorizontalFlip,
        "category": "Geometric",
        "params": [],
    },
    "VerticalFlip": {
        "class": A.VerticalFlip,
        "category": "Geometric",
        "params": [],
    },
    "Rotate": {
        "class": A.Rotate,
        "category": "Geometric",
        "params": [
            ("limit", "int", 45, 0, 180, 1),
        ],
    },
    "Affine": {
        "class": A.Affine,
        "category": "Geometric",
        "params": [
            ("scale_min", "float", 0.8, 0.1, 2.0, 0.05),
            ("scale_max", "float", 1.2, 0.1, 2.0, 0.05),
            ("rotate_min", "int", -45, -180, 180, 1),
            ("rotate_max", "int", 45, -180, 180, 1),
            ("shear_min", "int", -10, -45, 45, 1),
            ("shear_max", "int", 10, -45, 45, 1),
        ],
    },
    "Perspective": {
        "class": A.Perspective,
        "category": "Geometric",
        "params": [
            ("scale_min", "float", 0.05, 0.0, 0.2, 0.01),
            ("scale_max", "float", 0.1, 0.0, 0.5, 0.01),
        ],
    },
    "ElasticTransform": {
        "class": A.ElasticTransform,
        "category": "Geometric",
        "params": [
            ("alpha", "float", 1.0, 0.0, 5.0, 0.1),
            ("sigma", "float", 50.0, 1.0, 100.0, 1.0),
        ],
    },
    "GridDistortion": {
        "class": A.GridDistortion,
        "category": "Geometric",
        "params": [
            ("num_steps", "int", 5, 1, 10, 1),
            ("distort_limit", "float", 0.3, 0.0, 1.0, 0.05),
        ],
    },
    "OpticalDistortion": {
        "class": A.OpticalDistortion,
        "category": "Geometric",
        "params": [
            ("distort_limit", "float", 0.05, 0.0, 1.0, 0.05),
            ("shift_limit", "float", 0.05, 0.0, 1.0, 0.05),
        ],
    },
    # ── Color / Pixel ──
    "RandomBrightnessContrast": {
        "class": A.RandomBrightnessContrast,
        "category": "Color",
        "params": [
            ("brightness_limit", "float", 0.2, 0.0, 1.0, 0.05),
            ("contrast_limit", "float", 0.2, 0.0, 1.0, 0.05),
        ],
    },
    "HueSaturationValue": {
        "class": A.HueSaturationValue,
        "category": "Color",
        "params": [
            ("hue_shift_limit", "int", 20, 0, 180, 1),
            ("sat_shift_limit", "int", 30, 0, 255, 1),
            ("val_shift_limit", "int", 20, 0, 255, 1),
        ],
    },
    "RGBShift": {
        "class": A.RGBShift,
        "category": "Color",
        "params": [
            ("r_shift_limit", "int", 20, 0, 255, 1),
            ("g_shift_limit", "int", 20, 0, 255, 1),
            ("b_shift_limit", "int", 20, 0, 255, 1),
        ],
    },
    "CLAHE": {
        "class": A.CLAHE,
        "category": "Color",
        "params": [
            ("clip_limit", "float", 4.0, 1.0, 16.0, 0.5),
        ],
    },
    "ChannelShuffle": {
        "class": A.ChannelShuffle,
        "category": "Color",
        "params": [],
    },
    "RandomGamma": {
        "class": A.RandomGamma,
        "category": "Color",
        "params": [
            ("gamma_limit_low", "int", 80, 0, 200, 1),
            ("gamma_limit_high", "int", 120, 80, 300, 1),
        ],
    },
    "ColorJitter": {
        "class": A.ColorJitter,
        "category": "Color",
        "params": [
            ("brightness", "float", 0.2, 0.0, 1.0, 0.05),
            ("contrast", "float", 0.2, 0.0, 1.0, 0.05),
            ("saturation", "float", 0.2, 0.0, 1.0, 0.05),
            ("hue", "float", 0.2, 0.0, 0.5, 0.05),
        ],
    },
    "ToGray": {
        "class": A.ToGray,
        "category": "Color",
        "params": [],
    },
    # ── Blur / Noise ──
    "GaussianBlur": {
        "class": A.GaussianBlur,
        "category": "Blur & Noise",
        "params": [
            ("blur_limit", "int", 7, 3, 31, 2),
        ],
    },
    "GaussNoise": {
        "class": A.GaussNoise,
        "category": "Blur & Noise",
        # v1.x uses var_limit (variance range in [0, 255^2] scale but normalised to [0,1])
        "params": [
            ("var_limit_min", "float", 0.001, 0.0, 0.1, 0.001),
            ("var_limit_max", "float", 0.01, 0.0, 0.2, 0.001),
        ],
    },
    "MedianBlur": {
        "class": A.MedianBlur,
        "category": "Blur & Noise",
        "params": [
            ("blur_limit", "int", 7, 3, 31, 2),
        ],
    },
    "MotionBlur": {
        "class": A.MotionBlur,
        "category": "Blur & Noise",
        "params": [
            ("blur_limit", "int", 7, 3, 31, 2),
        ],
    },
    # ── Enhancement ──
    "Sharpen": {
        "class": A.Sharpen,
        "category": "Enhancement",
        "params": [
            ("alpha_min", "float", 0.2, 0.0, 1.0, 0.05),
            ("alpha_max", "float", 0.5, 0.0, 1.0, 0.05),
            ("lightness_min", "float", 0.5, 0.0, 1.0, 0.05),
            ("lightness_max", "float", 1.0, 0.0, 2.0, 0.05),
        ],
    },
    "Emboss": {
        "class": A.Emboss,
        "category": "Enhancement",
        "params": [
            ("alpha_min", "float", 0.2, 0.0, 1.0, 0.05),
            ("alpha_max", "float", 0.5, 0.0, 1.0, 0.05),
            ("strength_min", "float", 0.2, 0.0, 1.0, 0.05),
            ("strength_max", "float", 0.7, 0.0, 2.0, 0.05),
        ],
    },
    # ── Dropout ──
    "CoarseDropout": {
        "class": A.CoarseDropout,
        "category": "Dropout",
        # v1.x API: max_holes, min_holes, max_height, min_height, max_width, min_width
        "params": [
            ("min_holes", "int", 1, 1, 30, 1),
            ("max_holes", "int", 8, 1, 50, 1),
            ("min_height", "int", 8, 1, 128, 1),
            ("max_height", "int", 32, 1, 256, 1),
            ("min_width", "int", 8, 1, 128, 1),
            ("max_width", "int", 32, 1, 256, 1),
        ],
    },
}


def _build_kwargs(name: str, param_values: dict) -> dict:
    """
    Convert flat UI param values into the kwargs expected by the albumentations class.
    Handles special range-based parameters.
    """
    kwargs = {}

    if name == "Affine":
        kwargs["scale"] = (param_values.get("scale_min", 0.8), param_values.get("scale_max", 1.2))
        kwargs["rotate"] = (param_values.get("rotate_min", -45), param_values.get("rotate_max", 45))
        kwargs["shear"] = (param_values.get("shear_min", -10), param_values.get("shear_max", 10))
    elif name == "Perspective":
        kwargs["scale"] = (param_values.get("scale_min", 0.05), param_values.get("scale_max", 0.1))
    elif name == "Rotate":
        kwargs["limit"] = param_values.get("limit", 45)
    elif name == "RandomGamma":
        kwargs["gamma_limit"] = (
            param_values.get("gamma_limit_low", 80),
            param_values.get("gamma_limit_high", 120),
        )
    elif name == "Sharpen":
        kwargs["alpha"] = (param_values.get("alpha_min", 0.2), param_values.get("alpha_max", 0.5))
        kwargs["lightness"] = (param_values.get("lightness_min", 0.5), param_values.get("lightness_max", 1.0))
    elif name == "Emboss":
        kwargs["alpha"] = (param_values.get("alpha_min", 0.2), param_values.get("alpha_max", 0.5))
        kwargs["strength"] = (param_values.get("strength_min", 0.2), param_values.get("strength_max", 0.7))
    elif name == "GaussianBlur":
        blur_limit = int(param_values.get("blur_limit", 7))
        blur_limit = max(3, blur_limit)
        if blur_limit % 2 == 0:
            blur_limit += 1
        # Keep minimum blur kernel > 0 to avoid albumentations warning.
        kwargs["blur_limit"] = (3, blur_limit)
        kwargs["sigma_limit"] = (0.1, 2.0)
    elif name == "GaussNoise":
        # v1.x: var_limit accepts (min, max) tuple; values are in [0, 255^2] but
        # albumentations internally multiplies by 255^2 when using float images,
        # so we pass a 0-255 scale tuple directly.
        var_min = round(param_values.get("var_limit_min", 0.001) * 255 * 255)
        var_max = round(param_values.get("var_limit_max", 0.01) * 255 * 255)
        kwargs["var_limit"] = (max(0, var_min), max(1, var_max))
    elif name == "CoarseDropout":
        # v1.x positional kwargs
        kwargs["max_holes"] = param_values.get("max_holes", 8)
        kwargs["min_holes"] = param_values.get("min_holes", 1)
        kwargs["max_height"] = param_values.get("max_height", 32)
        kwargs["min_height"] = param_values.get("min_height", 8)
        kwargs["max_width"] = param_values.get("max_width", 32)
        kwargs["min_width"] = param_values.get("min_width", 8)
    else:
        # For simple transforms, pass params directly
        entry = AUGMENTATION_REGISTRY[name]
        for p in entry["params"]:
            pname = p[0]
            if pname in param_values:
                kwargs[pname] = param_values[pname]

    return kwargs


def build_pipeline(selected: dict) -> A.Compose:
    """
    Build an Albumentations Compose pipeline from the selected augmentations.

    selected: {aug_name: {"params": {param_name: value}, "p": float}}
    """
    transforms = []
    for name, config in selected.items():
        entry = AUGMENTATION_REGISTRY[name]
        cls = entry["class"]
        kwargs = _build_kwargs(name, config.get("params", {}))
        kwargs["p"] = config.get("p", 1.0)
        transforms.append(cls(**kwargs))

    return A.Compose(transforms)

