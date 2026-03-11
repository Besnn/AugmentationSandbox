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
from pathlib import Path
from typing import Any, List, Optional, Tuple, cast

from augmentations import AUGMENTATION_REGISTRY, build_pipeline
from code_generator import generate_code

try:
    from streamlit_ace import THEMES as ACE_THEMES, st_ace
except ImportError:
    st_ace = None
    ACE_THEMES = []


def _load_github_dark_theme_js() -> str:
    """Load the local GitHub Dark Ace theme file bundled with this app."""
    theme_asset = Path(__file__).with_name("theme-github_dark.js")
    return theme_asset.read_text(encoding="utf-8")


def _ensure_github_dark_theme() -> None:
    """Create the ACE GitHub Dark theme file if the installed package is missing it."""
    if st_ace is None:
        return
    try:
        import streamlit_ace

        theme_path = (
            Path(streamlit_ace.__file__).resolve().parent
            / "frontend"
            / "build"
            / "theme-github_dark.js"
        )
        if not theme_path.exists():
            theme_path.write_text(_load_github_dark_theme_js(), encoding="utf-8")
        if "github_dark" not in ACE_THEMES:
            ACE_THEMES.append("github_dark")
    except Exception:
        # Keep the app usable even if site-packages is read-only.
        pass

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

if "custom_run_results" not in st.session_state:
    st.session_state.custom_run_results = []

if "custom_editor_version" not in st.session_state:
    st.session_state.custom_editor_version = 0

if "last_generated_code" not in st.session_state:
    st.session_state.last_generated_code = ""

if "custom_run_iterations" not in st.session_state:
    st.session_state.custom_run_iterations = 1

if "selected_custom_output" not in st.session_state:
    st.session_state.selected_custom_output = "Pipeline"


def _bump_counter():
    st.session_state.run_counter += 1
    st.session_state.selected_custom_output = "Pipeline"


def _run_custom_code(
    code: str, image: np.ndarray, iterations: int = 1
) -> List[Tuple[Optional[np.ndarray], Optional[str]]]:
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

    def _execute_once(current_image: np.ndarray) -> Tuple[Optional[np.ndarray], Optional[str]]:
        local_scope: dict[str, Any] = {"image": current_image.copy()}

        try:
            exec(code, global_scope, local_scope)
            if "augmented_image" in local_scope:
                output = local_scope["augmented_image"]
            elif "result" in local_scope and isinstance(local_scope["result"], dict):
                result_obj = local_scope["result"]
                output = result_obj.get("image")
            elif callable(local_scope.get("apply")):
                apply_fn = local_scope["apply"]
                output = apply_fn(current_image.copy())
            elif callable(local_scope.get("transform")):
                transform_fn = local_scope["transform"]
                output = transform_fn(image=current_image)["image"]
            else:
                return None, "Define transform, augmented_image, result['image'], or apply(image)."

            if not isinstance(output, np.ndarray):
                return None, "Custom code output must be a numpy.ndarray image."
            return output, None
        except Exception as exc:
            return None, str(exc)

    run_results: List[Tuple[Optional[np.ndarray], Optional[str]]] = []
    for _ in range(max(1, iterations)):
        # Run each iteration from the same base image instead of chaining outputs.
        output, error = _execute_once(image)
        if output is None and error is None:
            error = "Custom code returned no image output."
        run_results.append((output, error))

    return run_results


def _get_editor_theme() -> str:
    """Use GitHub Dark for the custom code editor."""
    _ensure_github_dark_theme()
    if "github_dark" in ACE_THEMES:
        return "github_dark"
    return "monokai"


def _outlined_container():
    """Use a bordered container when supported by the installed Streamlit version."""
    try:
        return st.container(border=True)
    except TypeError:
        return st.container()


def _format_summary_value(value: Any) -> str:
    """Format parameter values for compact, readable table cells."""
    if isinstance(value, float):
        return f"{value:.4g}"
    if isinstance(value, (list, tuple)):
        return ", ".join(_format_summary_value(v) for v in value)
    return str(value)


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
st.sidebar.markdown("### Jump to Section")
st.sidebar.markdown(
    "\n".join(
        [
            "- [Image Comparison](#image-comparison)",
            "- [Custom Outputs](#custom-outputs)",
            "- [Pipeline Code](#pipeline-code)",
            "- [Pipeline Summary](#pipeline-summary)",
        ]
    )
)
st.sidebar.divider()
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
st.markdown('<div id="top"></div>', unsafe_allow_html=True)
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

# Resolve which image should appear in the Augmented pane.
selected_label = st.session_state.selected_custom_output
selected_custom_img = None
selected_custom_err = None
if selected_label != "Pipeline" and st.session_state.custom_run_results:
    try:
        run_index = int(str(selected_label).split(" ")[1]) - 1
        if 0 <= run_index < len(st.session_state.custom_run_results):
            selected_custom_img, selected_custom_err = st.session_state.custom_run_results[run_index]
    except (ValueError, IndexError):
        selected_custom_img = None
        selected_custom_err = "Invalid custom output selection."

# Display images side by side
st.markdown('<div id="image-comparison"></div>', unsafe_allow_html=True)
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
    elif selected_custom_err:
        st.error(f"Selected custom output error: {selected_custom_err}")
        st.image(augmented, width="stretch")
    elif selected_custom_img is not None:
        st.image(selected_custom_img, width="stretch")
        h2, w2 = selected_custom_img.shape[:2]
        st.caption(f"Size: {w2} × {h2}")
    else:
        st.image(augmented, width="stretch")
        h2, w2 = augmented.shape[:2]
        st.caption(f"Size: {w2} × {h2}")

st.markdown('<div id="custom-outputs"></div>', unsafe_allow_html=True)
if st.session_state.custom_run_results:
    st.subheader("Custom Outputs")
    output_options = ["Pipeline"] + [
        f"Run {i}" for i in range(1, len(st.session_state.custom_run_results) + 1)
    ]
    if st.session_state.selected_custom_output not in output_options:
        st.session_state.selected_custom_output = "Pipeline"
    if st.button("Show pipeline output", key="select_pipeline_output", width="content"):
        st.session_state.selected_custom_output = "Pipeline"
        st.rerun()
    output_cols = st.columns(4)
    for idx, (out_img, out_err) in enumerate(st.session_state.custom_run_results, start=1):
        with output_cols[(idx - 1) % len(output_cols)]:
            run_label = f"Run {idx}"
            is_selected = st.session_state.selected_custom_output == run_label
            button_text = f"Selected: {run_label}" if is_selected else f"Show {run_label}"
            if st.button(button_text, key=f"select_custom_run_{idx}", width="stretch"):
                st.session_state.selected_custom_output = run_label
                st.rerun()
            if out_err:
                st.error(out_err)
            elif out_img is not None:
                st.image(out_img, width="stretch")

# Pipeline info
st.markdown('<div id="pipeline-code"></div>', unsafe_allow_html=True)
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
        run_button_col, run_count_col = st.columns([2, 1])
        with run_button_col:
            run_custom = st.button("Run code", key="run_custom_code", width="stretch")
        with run_count_col:
            st.number_input(
                "Runs",
                min_value=1,
                max_value=100,
                step=1,
                key="custom_run_iterations",
                help="Number of independent runs from the same base image.",
            )
        if st.button("Clear output", key="clear_custom_output"):
            st.session_state.custom_run_results = []
            st.session_state.custom_augmented = None
            st.session_state.custom_error = None
            st.session_state.selected_custom_output = "Pipeline"
            st.rerun()

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
        run_results = _run_custom_code(
            st.session_state.custom_code,
            image,
            iterations=int(st.session_state.custom_run_iterations),
        )
        st.session_state.custom_run_results = run_results
        successful_indexes = [
            idx for idx, (img, err) in enumerate(run_results, start=1) if img is not None and err is None
        ]
        st.session_state.selected_custom_output = (
            f"Run {successful_indexes[0]}" if successful_indexes else "Pipeline"
        )
        # Keep legacy state keys populated for compatibility with any pending UI reads.
        successful = [img for img, err in run_results if img is not None and err is None]
        errors = [err for _, err in run_results if err]
        st.session_state.custom_augmented = successful[-1] if successful else None
        st.session_state.custom_error = "\n".join(errors) if errors else None
        st.rerun()

    st.markdown('<div id="pipeline-summary"></div>', unsafe_allow_html=True)
    st.subheader("Pipeline Summary")

    overview_rows: List[dict[str, Any]] = []
    param_rows: List[dict[str, str]] = []
    for name, config in selected.items():
        params = config["params"]
        overview_rows.append(
            {
                "Augmentation": name,
                "Probability (p)": f"{config['p']:.2f}",
                "Parameter count": len(params),
            }
        )
        if params:
            for pname, pvalue in params.items():
                param_rows.append(
                    {
                        "Augmentation": name,
                        "Parameter": pname,
                        "Value": _format_summary_value(pvalue),
                    }
                )
        else:
            param_rows.append(
                {
                    "Augmentation": name,
                    "Parameter": "(none)",
                    "Value": "-",
                }
            )

    st.caption("Selected augmentations")
    st.dataframe(overview_rows, hide_index=True, width="stretch")
    st.caption("All parameters")
    st.dataframe(param_rows, hide_index=True, width="stretch")
else:
    st.info("👈 Select augmentations from the sidebar to get started!")

# Footer
st.divider()
st.caption(
    "Built with [Streamlit](https://streamlit.io) & "
    "[Albumentations](https://albumentations.ai) • "
)
