"""
Albumentations Augmentation Sandbox
Run with: streamlit run main.py
"""

import builtins
import albumentations as A
import numpy as np
import streamlit as st
from PIL import Image
from collections import OrderedDict
from typing import Any, cast

from augmentations import AUGMENTATION_REGISTRY, build_pipeline
from code_generator import generate_code

try:
    from streamlit_ace import THEMES as ACE_THEMES, st_ace
except ImportError:
    st_ace = None
    ACE_THEMES = []

# ──────────────────────────── Page config ────────────────────────────
st.set_page_config(
    page_title="Albumentations Sandbox",
    page_icon="🎨",
    layout="wide",
)

# ──────────────────────────── Session state ──────────────────────────
if "run_counter" not in st.session_state:
    st.session_state.run_counter = 0

if "custom_code" not in st.session_state:
    st.session_state.custom_code = ""

if "custom_augmented" not in st.session_state:
    st.session_state.custom_augmented = None

if "custom_error" not in st.session_state:
    st.session_state.custom_error = None

if "custom_editor_version" not in st.session_state:
    st.session_state.custom_editor_version = 0

if "last_generated_code" not in st.session_state:
    st.session_state.last_generated_code = ""


def _bump_counter():
    st.session_state.run_counter += 1


def _run_custom_code(code: str, image: np.ndarray) -> tuple[np.ndarray | None, str | None]:
    """Execute custom code and return either an image or an error message."""
    safe_builtins = {
        "abs": builtins.abs,
        "all": builtins.all,
        "any": builtins.any,
        "bool": builtins.bool,
        "dict": builtins.dict,
        "enumerate": builtins.enumerate,
        "float": builtins.float,
        "int": builtins.int,
        "len": builtins.len,
        "list": builtins.list,
        "max": builtins.max,
        "min": builtins.min,
        "range": builtins.range,
        "round": builtins.round,
        "set": builtins.set,
        "sum": builtins.sum,
        "tuple": builtins.tuple,
        "zip": builtins.zip,
        "__import__": builtins.__import__,
    }
    global_scope: dict[str, Any] = {"__builtins__": safe_builtins, "A": A, "np": np}
    local_scope: dict[str, Any] = {"image": image.copy()}

    try:
        exec(code, global_scope, local_scope)
        if "augmented_image" in local_scope:
            output = local_scope["augmented_image"]
        elif "result" in local_scope and isinstance(local_scope["result"], dict):
            result_obj = local_scope["result"]
            output = result_obj.get("image")
        elif callable(local_scope.get("apply")):
            apply_fn = local_scope["apply"]
            output = apply_fn(image.copy())
        elif callable(local_scope.get("transform")):
            transform_fn = local_scope["transform"]
            output = transform_fn(image=image)["image"]
        else:
            return None, "Define transform, augmented_image, result['image'], or apply(image)."

        if not isinstance(output, np.ndarray):
            return None, "Custom code output must be a numpy.ndarray image."
        return output, None
    except Exception as exc:
        return None, str(exc)


def _get_editor_theme() -> str:
    """Use GitHub Dark for the custom code editor."""
    return "github_dark"


def _outlined_container():
    """Use a bordered container when supported by the installed Streamlit version."""
    try:
        return st.container(border=True)
    except TypeError:
        return st.container()


# ──────────────────────────── Helper: generate a sample image ────────
def _make_sample_image() -> np.ndarray:
    """Generate a colourful sample image so the app works without uploading."""
    w, h = 640, 480
    img = np.zeros((h, w, 3), dtype=np.uint8)
    # Gradient background
    xs = np.arange(w)
    ys = np.arange(h)
    xv, yv = np.meshgrid(xs, ys)
    img[..., 0] = (255 * xv / w).astype(np.uint8)
    img[..., 1] = (255 * yv / h).astype(np.uint8)
    img[..., 2] = (255 * (1 - xv / w)).astype(np.uint8)
    # Draw some shapes
    img[h // 4 - 10 : h // 4 + 10, w // 6 : 5 * w // 6] = [255, 255, 255]
    img[h // 6 : 5 * h // 6, w // 2 - 10 : w // 2 + 10] = [255, 255, 0]
    img[h // 3 : h // 3 + 80, w // 4 : w // 4 + 80] = [0, 200, 255]
    img[2 * h // 3 - 40 : 2 * h // 3 + 40, 3 * w // 4 - 40 : 3 * w // 4 + 40] = [255, 100, 50]
    return img


# ──────────────────────────── Sidebar ────────────────────────────────
st.sidebar.title("Augmentation Sandbox")
st.sidebar.markdown("Upload an image and configure augmentations.")

# Image upload
uploaded = st.sidebar.file_uploader(
    "Upload an image", type=["png", "jpg", "jpeg", "webp", "bmp"]
)

if uploaded is not None:
    pil_img = Image.open(uploaded).convert("RGB")
    image = np.array(pil_img)
else:
    image = _make_sample_image()

st.sidebar.divider()
st.sidebar.subheader("Select Augmentations")

# Group augmentations by category
categories: dict[str, list[str]] = {}
for name, entry in AUGMENTATION_REGISTRY.items():
    cat = entry["category"]
    categories.setdefault(cat, []).append(name)

# Collect selected augmentations and their params
selected: OrderedDict = OrderedDict()

for cat, aug_names in categories.items():
    with st.sidebar.expander(f"**{cat}**", expanded=False):
        for aug_name in aug_names:
            entry = AUGMENTATION_REGISTRY[aug_name]
            enabled = st.checkbox(aug_name, key=f"enable_{aug_name}")
            if enabled:
                params = {}
                # Probability slider
                p = st.slider(
                    f"{aug_name} — probability",
                    min_value=0.0,
                    max_value=1.0,
                    value=1.0,
                    step=0.05,
                    key=f"p_{aug_name}",
                )
                # Parameter sliders
                for param_def in entry["params"]:
                    pname, ptype, pdefault, *prest = param_def
                    label = f"{aug_name} — {pname}"
                    if ptype == "int":
                        pmin, pmax, pstep = prest
                        val = st.slider(
                            label,
                            min_value=pmin,
                            max_value=pmax,
                            value=pdefault,
                            step=pstep,
                            key=f"param_{aug_name}_{pname}",
                        )
                    elif ptype == "float":
                        pmin, pmax, pstep = prest
                        val = st.slider(
                            label,
                            min_value=pmin,
                            max_value=pmax,
                            value=pdefault,
                            step=pstep,
                            key=f"param_{aug_name}_{pname}",
                        )
                    elif ptype == "bool":
                        val = st.checkbox(
                            label,
                            value=pdefault,
                            key=f"param_{aug_name}_{pname}",
                        )
                    elif ptype == "select":
                        options = prest[0]
                        val = st.selectbox(
                            label,
                            options=options,
                            index=options.index(pdefault) if pdefault in options else 0,
                            key=f"param_{aug_name}_{pname}",
                        )
                    else:
                        val = pdefault
                    params[pname] = val

                selected[aug_name] = {"params": params, "p": p}
                st.markdown("---")

# ──────────────────────────── Main area ──────────────────────────────
st.title("Albumentations Augmentation Sandbox")

# Re-run button
col_btn1, col_btn2, _ = st.columns([1, 1, 4])
with col_btn1:
    st.button("Re-run augmentation", on_click=_bump_counter)
with col_btn2:
    st.markdown(f"*Run #{st.session_state.run_counter}*")

# Apply pipeline
if selected:
    try:
        pipeline = build_pipeline(selected)
        augmented = pipeline(image=image)["image"]
        error_msg = None
    except Exception as e:
        augmented = image.copy()
        error_msg = str(e)
else:
    augmented = image.copy()
    error_msg = None

# Display images side by side
col_orig, col_aug = st.columns(2)

with col_orig:
    st.subheader("Original")
    st.image(image, width="stretch")
    h, w = image.shape[:2]
    st.caption(f"Size: {w} × {h}")

with col_aug:
    st.subheader("Augmented")
    if error_msg:
        st.error(f"Error applying augmentation: {error_msg}")
        st.image(image, width="stretch")
    else:
        st.image(augmented, width="stretch")
        h2, w2 = augmented.shape[:2]
        st.caption(f"Size: {w2} × {h2}")

# Pipeline info
st.divider()

if selected:
    st.subheader("Pipeline Code")
    generated_code = generate_code(selected)
    if (
        not st.session_state.custom_code
        or generated_code != st.session_state.last_generated_code
    ):
        st.session_state.custom_code = generated_code
        st.session_state.last_generated_code = generated_code
        st.session_state.custom_editor_version += 1

    editor_col, actions_col = st.columns([4, 1])
    with actions_col:
        if st.button("Load generated", key="load_generated_code"):
            st.session_state.custom_code = generated_code
            st.session_state.last_generated_code = generated_code
            st.session_state.custom_editor_version += 1
        run_custom = st.button("Run code", key="run_custom_code")
        if st.button("Clear output", key="clear_custom_output"):
            st.session_state.custom_augmented = None
            st.session_state.custom_error = None

    with editor_col:
        editor_shell = _outlined_container()
        with editor_shell:
            if st_ace is not None:
                ace_key = f"custom_code_ace_{st.session_state.custom_editor_version}"
                ace_editor = cast(Any, st_ace)
                edited_code = ace_editor(
                    value=st.session_state.custom_code,
                    language="python",
                    theme=_get_editor_theme(),
                    key=ace_key,
                    height=260,
                    auto_update=True,
                )
                if edited_code is not None:
                    st.session_state.custom_code = edited_code
            else:
                st.text_area(
                    "Editable pipeline code",
                    key="custom_code",
                    height=260,
                    help="Define transform, augmented_image, result['image'], or apply(image).",
                )
                st.caption("Tip: install streamlit-ace for syntax-highlighted editing.")

    if run_custom:
        out_img, out_err = _run_custom_code(st.session_state.custom_code, image)
        st.session_state.custom_augmented = out_img
        st.session_state.custom_error = out_err

    if st.session_state.custom_error:
        st.error(f"Custom code error: {st.session_state.custom_error}")
    elif st.session_state.custom_augmented is not None:
        st.caption("Custom code output")
        st.image(st.session_state.custom_augmented, width="stretch")

    st.subheader("Pipeline Summary")
    summary_cols = st.columns(min(len(selected), 4))
    for i, (name, config) in enumerate(selected.items()):
        with summary_cols[i % len(summary_cols)]:
            st.metric(label=name, value=f"p={config['p']:.2f}")
else:
    st.info("👈 Select augmentations from the sidebar to get started!")

# Footer
st.divider()
st.caption(
    "Built with [Streamlit](https://streamlit.io) & "
    "[Albumentations](https://albumentations.ai) • "
)
