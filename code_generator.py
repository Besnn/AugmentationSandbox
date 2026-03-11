"""
Generates a copy-pasteable Python code snippet from the current augmentation config.
"""

from augmentations import _build_kwargs


def generate_code(selected: dict) -> str:
    """
    Generate Python code for the current augmentation pipeline.

    selected: {aug_name: {"params": {param_name: value}, "p": float}}
    """
    lines = [
        "import albumentations as A",
        "",
        "transform = A.Compose([",
    ]

    for name, config in selected.items():
        kwargs = _build_kwargs(name, config.get("params", {}))
        kwargs["p"] = config.get("p", 1.0)

        kwargs_str = ", ".join(f"{k}={_format_value(v)}" for k, v in kwargs.items())
        lines.append(f"    A.{name}({kwargs_str}),")

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

