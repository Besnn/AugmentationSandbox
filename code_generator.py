"""
Generates a copy-pasteable Python code snippet from the current augmentation config.
"""

from augmentations import AUGMENTATION_REGISTRY, _build_kwargs


def generate_code(selected) -> str:
    """
    Generate Python code for the current augmentation pipeline.

    selected supports either:
      - list of step dicts with keys: name, params, p
      - legacy mapping: {aug_name: {"params": {...}, "p": float}}
    """
    lines = [
        "import albumentations as A",
        "",
        "transform = A.Compose([",
    ]

    if isinstance(selected, list):
        iterable = [
            (step["name"], {"params": step.get("params", {}), "p": step.get("p", 1.0)})
            for step in selected
        ]
    else:
        iterable = list(selected.items())

    for name, config in iterable:
        entry = AUGMENTATION_REGISTRY[name]
        kwargs = _build_kwargs(name, config.get("params", {}))
        kwargs["p"] = config.get("p", 1.0)
        class_name = entry["class"].__name__

        kwargs_str = ", ".join(f"{k}={_format_value(v)}" for k, v in kwargs.items())
        lines.append(f"    A.{class_name}({kwargs_str}),")

    lines.append("])")
    lines.append("")
    lines.append("# Apply to an image (numpy array, RGB, uint8):")
    lines.append("# result = transform(image=image)")
    lines.append('# augmented_image = result["image"]')

    return "\n".join(lines)


def _format_value(v) -> str:
    if isinstance(v, float):
        return f"{v:.2f}"
    if isinstance(v, tuple):
        formatted = ", ".join(_format_value(x) for x in v)
        return f"({formatted})"
    return repr(v)

