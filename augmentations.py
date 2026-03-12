"""
Registry of Albumentations augmentations with parameter metadata for the UI.
Compatible with albumentations >= 1.3, < 2.0
"""

import ast
import inspect

import albumentations as A

# Each entry: (param_name, type, default, min, max, step)
# type is one of: "int", "float", "bool", "select", "text", "literal"
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
    "RandomRotate90": {
        "class": A.RandomRotate90,
        "category": "Geometric",
        "params": [],
    },
    "ShiftScaleRotate": {
        "class": A.ShiftScaleRotate,
        "category": "Geometric",
        "params": [
            ("shift_limit", "float", 0.1, 0.0, 0.5, 0.01),
            ("scale_limit", "float", 0.1, 0.0, 0.5, 0.01),
            ("rotate_limit", "int", 30, 0, 180, 1),
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
    "ToSepia": {
        "class": A.ToSepia,
        "category": "Color",
        "params": [],
    },
    "Equalize": {
        "class": A.Equalize,
        "category": "Color",
        "params": [
            ("mode", "select", "cv", ["cv", "pil"]),
            ("by_channels", "bool", True),
        ],
    },
    "Solarize": {
        "class": A.Solarize,
        "category": "Color",
        "params": [
            ("threshold", "int", 128, 0, 255, 1),
        ],
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
    "ISONoise": {
        "class": A.ISONoise,
        "category": "Blur & Noise",
        "params": [
            ("color_shift_min", "float", 0.01, 0.0, 0.5, 0.01),
            ("color_shift_max", "float", 0.05, 0.0, 1.0, 0.01),
            ("intensity_min", "float", 0.1, 0.0, 0.5, 0.01),
            ("intensity_max", "float", 0.5, 0.0, 1.0, 0.01),
        ],
    },
    "MultiplicativeNoise": {
        "class": A.MultiplicativeNoise,
        "category": "Blur & Noise",
        "params": [
            ("multiplier_min", "float", 0.9, 0.0, 2.0, 0.01),
            ("multiplier_max", "float", 1.1, 0.0, 3.0, 0.01),
            ("per_channel", "bool", False),
            ("elementwise", "bool", False),
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
    "UnsharpMask": {
        "class": A.UnsharpMask,
        "category": "Enhancement",
        "params": [
            ("blur_limit", "int", 7, 3, 31, 2),
            ("sigma_limit_min", "float", 0.1, 0.0, 2.0, 0.05),
            ("sigma_limit_max", "float", 1.0, 0.0, 3.0, 0.05),
            ("alpha_min", "float", 0.2, 0.0, 1.0, 0.05),
            ("alpha_max", "float", 0.5, 0.0, 1.0, 0.05),
            ("threshold", "int", 10, 0, 255, 1),
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
    "PixelDropout": {
        "class": A.PixelDropout,
        "category": "Dropout",
        "params": [
            ("dropout_prob", "float", 0.01, 0.0, 1.0, 0.01),
            ("per_channel", "bool", False),
        ],
    },
}


def _has_default_constructor(cls: type) -> bool:
    """Return True when the transform can be instantiated without required custom args."""
    signature = inspect.signature(cls.__init__)
    for param in signature.parameters.values():
        if param.name in {"self", "always_apply", "p"}:
            continue
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue
        if param.default is inspect.Parameter.empty:
            return False
    return True


def _infer_numeric_bounds(default_value: float) -> tuple[float, float, float]:
    """Generate simple slider bounds for inferred numeric defaults."""
    magnitude = max(1.0, abs(float(default_value)))
    if default_value >= 0:
        min_v = 0.0
        max_v = max(1.0, magnitude * 3.0)
    else:
        min_v = -magnitude * 3.0
        max_v = magnitude * 3.0
    step = 0.01 if abs(default_value) < 1 else 0.1
    return min_v, max_v, step


def _infer_param_definition(param_name: str, default_value: object):
    """Infer a UI control definition from a constructor default value."""
    if isinstance(default_value, bool):
        return (param_name, "bool", default_value)
    if isinstance(default_value, int):
        max_v = max(10, abs(default_value) * 3)
        min_v = 0 if default_value >= 0 else -max_v
        return (param_name, "int", default_value, min_v, max_v, 1)
    if isinstance(default_value, float):
        min_v, max_v, step = _infer_numeric_bounds(default_value)
        return (param_name, "float", default_value, min_v, max_v, step)
    if isinstance(default_value, str):
        return (param_name, "text", default_value)
    if isinstance(default_value, (tuple, list, dict)) or default_value is None:
        return (param_name, "literal", repr(default_value))
    return None


def _auto_params_for_class(cls: type) -> list[tuple]:
    """Build UI params from class signature defaults for optional transforms."""
    params: list[tuple] = []
    signature = inspect.signature(cls.__init__)
    for param in signature.parameters.values():
        if param.name in {"self", "always_apply", "p"}:
            continue
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue
        if param.default is inspect.Parameter.empty:
            continue
        inferred = _infer_param_definition(param.name, param.default)
        if inferred is not None:
            params.append(inferred)
    return params


def _register_optional_augmentation(
    name: str,
    category: str,
    candidate_class_names: list[str],
) -> None:
    """Register optional transforms only when present and safely constructible."""
    if name in AUGMENTATION_REGISTRY:
        return

    cls = None
    for class_name in candidate_class_names:
        cls = getattr(A, class_name, None)
        if cls is not None:
            break

    if cls is None or not _has_default_constructor(cls):
        return

    AUGMENTATION_REGISTRY[name] = {
        "class": cls,
        "category": category,
        "params": _auto_params_for_class(cls),
    }


# Add requested transforms when available in the installed Albumentations version.
_OPTIONAL_REQUESTED_AUGMENTATIONS: list[tuple[str, str, list[str]]] = [
    ("AdditiveNoise", "Blur & Noise", ["AdditiveNoise"]),
    ("AdvancedBlur", "Blur & Noise", ["AdvancedBlur"]),
    ("AtmosphericFog", "Weather & Effects", ["AtmosphericFog", "RandomFog"]),
    ("AutoContrast", "Color", ["AutoContrast"]),
    ("Blur", "Blur & Noise", ["Blur"]),
    ("ChannelDropout", "Dropout", ["ChannelDropout"]),
    ("ChannelSwap", "Color", ["ChannelSwap", "ChannelShuffle"]),
    ("ChromaticAberration", "Color", ["ChromaticAberration"]),
    ("Defocus", "Blur & Noise", ["Defocus"]),
    ("Dithering", "Color", ["Dithering"]),
    ("Downscale", "Color", ["Downscale"]),
    ("FDA", "Color", ["FDA"]),
    ("FancyPCA", "Color", ["FancyPCA"]),
    ("FilmGrain", "Color", ["FilmGrain"]),
    ("FromFloat", "Color", ["FromFloat"]),
    ("GlassBlur", "Blur & Noise", ["GlassBlur"]),
    ("HEStain", "Color", ["HEStain"]),
    ("Halftone", "Color", ["Halftone"]),
    ("HistogramMatching", "Color", ["HistogramMatching"]),
    ("Illumination", "Color", ["Illumination"]),
    ("ImageCompression", "Color", ["ImageCompression"]),
    ("InvertImg", "Color", ["InvertImg"]),
    ("LensFlare", "Weather & Effects", ["LensFlare", "RandomSunFlare"]),
    ("Normalize", "Color", ["Normalize"]),
    ("PhotoMetricDistort", "Color", ["PhotoMetricDistort"]),
    ("PixelDistributionAdaptation", "Color", ["PixelDistributionAdaptation"]),
    ("PlanckianJitter", "Color", ["PlanckianJitter"]),
    ("PlasmaBrightnessContrast", "Color", ["PlasmaBrightnessContrast"]),
    ("PlasmaShadow", "Weather & Effects", ["PlasmaShadow"]),
    ("Posterize", "Color", ["Posterize"]),
    ("RandomFog", "Weather & Effects", ["RandomFog"]),
    ("RandomGravel", "Weather & Effects", ["RandomGravel"]),
    ("RandomRain", "Weather & Effects", ["RandomRain"]),
    ("RandomShadow", "Weather & Effects", ["RandomShadow"]),
    ("RandomSnow", "Weather & Effects", ["RandomSnow"]),
    ("RandomSunFlare", "Weather & Effects", ["RandomSunFlare"]),
    ("RandomToneCurve", "Color", ["RandomToneCurve"]),
    ("RingingOvershoot", "Enhancement", ["RingingOvershoot"]),
    ("SaltAndPepper", "Blur & Noise", ["SaltAndPepper"]),
    ("ShotNoise", "Blur & Noise", ["ShotNoise"]),
    ("Spatter", "Weather & Effects", ["Spatter"]),
    ("Superpixels", "Enhancement", ["Superpixels"]),
    ("ToFloat", "Color", ["ToFloat"]),
    ("ToRGB", "Color", ["ToRGB"]),
    ("Vignetting", "Color", ["Vignetting", "RandomVignetting"]),
    ("ZoomBlur", "Blur & Noise", ["ZoomBlur"]),
]

for _name, _category, _class_candidates in _OPTIONAL_REQUESTED_AUGMENTATIONS:
    _register_optional_augmentation(_name, _category, _class_candidates)


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
    elif name == "ShiftScaleRotate":
        kwargs["shift_limit"] = param_values.get("shift_limit", 0.1)
        kwargs["scale_limit"] = param_values.get("scale_limit", 0.1)
        kwargs["rotate_limit"] = param_values.get("rotate_limit", 30)
    elif name == "RandomGamma":
        gamma_low = param_values.get("gamma_limit_low", 80)
        gamma_high = param_values.get("gamma_limit_high", 120)
        kwargs["gamma_limit"] = (min(gamma_low, gamma_high), max(gamma_low, gamma_high))
    elif name == "Sharpen":
        alpha_min = param_values.get("alpha_min", 0.2)
        alpha_max = param_values.get("alpha_max", 0.5)
        lightness_min = param_values.get("lightness_min", 0.5)
        lightness_max = param_values.get("lightness_max", 1.0)
        kwargs["alpha"] = (min(alpha_min, alpha_max), max(alpha_min, alpha_max))
        kwargs["lightness"] = (min(lightness_min, lightness_max), max(lightness_min, lightness_max))
    elif name == "Emboss":
        alpha_min = param_values.get("alpha_min", 0.2)
        alpha_max = param_values.get("alpha_max", 0.5)
        strength_min = param_values.get("strength_min", 0.2)
        strength_max = param_values.get("strength_max", 0.7)
        kwargs["alpha"] = (min(alpha_min, alpha_max), max(alpha_min, alpha_max))
        kwargs["strength"] = (min(strength_min, strength_max), max(strength_min, strength_max))
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
        var_min = max(0, var_min)
        var_max = max(1, var_max)
        kwargs["var_limit"] = (min(var_min, var_max), max(var_min, var_max))
    elif name == "ISONoise":
        color_shift_min = param_values.get("color_shift_min", 0.01)
        color_shift_max = param_values.get("color_shift_max", 0.05)
        intensity_min = param_values.get("intensity_min", 0.1)
        intensity_max = param_values.get("intensity_max", 0.5)
        kwargs["color_shift"] = (min(color_shift_min, color_shift_max), max(color_shift_min, color_shift_max))
        kwargs["intensity"] = (min(intensity_min, intensity_max), max(intensity_min, intensity_max))
    elif name == "MultiplicativeNoise":
        mult_min = param_values.get("multiplier_min", 0.9)
        mult_max = param_values.get("multiplier_max", 1.1)
        kwargs["multiplier"] = (min(mult_min, mult_max), max(mult_min, mult_max))
        kwargs["per_channel"] = param_values.get("per_channel", False)
        kwargs["elementwise"] = param_values.get("elementwise", False)
    elif name == "UnsharpMask":
        blur_limit = int(param_values.get("blur_limit", 7))
        blur_limit = max(3, blur_limit)
        if blur_limit % 2 == 0:
            blur_limit += 1
        sigma_min = param_values.get("sigma_limit_min", 0.1)
        sigma_max = param_values.get("sigma_limit_max", 1.0)
        alpha_min = param_values.get("alpha_min", 0.2)
        alpha_max = param_values.get("alpha_max", 0.5)
        kwargs["blur_limit"] = (3, blur_limit)
        kwargs["sigma_limit"] = (min(sigma_min, sigma_max), max(sigma_min, sigma_max))
        kwargs["alpha"] = (min(alpha_min, alpha_max), max(alpha_min, alpha_max))
        kwargs["threshold"] = param_values.get("threshold", 10)
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
                ptype = p[1]
                pvalue = param_values[pname]
                if ptype == "literal" and isinstance(pvalue, str):
                    try:
                        kwargs[pname] = ast.literal_eval(pvalue)
                    except (ValueError, SyntaxError):
                        kwargs[pname] = pvalue
                else:
                    kwargs[pname] = pvalue

    return kwargs


def build_pipeline(selected) -> A.Compose:
    """
    Build an Albumentations Compose pipeline from the selected augmentations.

    selected supports either:
      - list of step dicts with keys: name, params, p
      - legacy mapping: {aug_name: {"params": {...}, "p": float}}
    """
    transforms = []
    if isinstance(selected, list):
        for step in selected:
            name = step["name"]
            entry = AUGMENTATION_REGISTRY[name]
            cls = entry["class"]
            kwargs = _build_kwargs(name, step.get("params", {}))
            kwargs["p"] = step.get("p", 1.0)
            transforms.append(cls(**kwargs))
    else:
        for name, config in selected.items():
            entry = AUGMENTATION_REGISTRY[name]
            cls = entry["class"]
            kwargs = _build_kwargs(name, config.get("params", {}))
            kwargs["p"] = config.get("p", 1.0)
            transforms.append(cls(**kwargs))

    return A.Compose(transforms)

