"""
Albumentations Augmentation Sandbox
Run with: streamlit run main.py
"""

import builtins
import albumentations as A
import numpy as np
import streamlit as st
from PIL import Image
from pathlib import Path
from typing import Any, List, Optional, Tuple, cast

from augmentations import AUGMENTATION_REGISTRY, build_pipeline
from code_generator import generate_code

try:
    from streamlit_ace import THEMES as ACE_THEMES, st_ace
except ImportError:
    st_ace = None
    ACE_THEMES = []


def _load_bundled_ace_theme(theme_name: str) -> str:
    """Return bundled Ace theme JS content from in-file constants."""
    bundled_themes = {
        "streamlit_auto": """
ace.define("ace/theme/streamlit_auto", ["require", "exports", "module", "ace/lib/dom"], function(require, exports, module) {
    exports.isDark = false;
    exports.cssClass = "ace-streamlit-auto";
    exports.cssText = ".ace-streamlit-auto .ace_gutter{background:var(--secondary-background-color,#f0f2f6);color:var(--text-color,#262730)}.ace-streamlit-auto .ace_print-margin{width:1px;background:var(--secondary-background-color,#e6e9ef)}.ace-streamlit-auto{background-color:var(--background-color,#ffffff);color:var(--text-color,#262730)}.ace-streamlit-auto .ace_cursor{color:var(--text-color,#262730)}.ace-streamlit-auto .ace_marker-layer .ace_selection{background:color-mix(in srgb, var(--primary-color,#ff4b4b) 28%, transparent)}.ace-streamlit-auto .ace_marker-layer .ace_active-line{background:color-mix(in srgb, var(--secondary-background-color,#f0f2f6) 82%, transparent)}.ace-streamlit-auto .ace_gutter-active-line{background:color-mix(in srgb, var(--secondary-background-color,#f0f2f6) 82%, transparent)}.ace-streamlit-auto .ace_keyword,.ace-streamlit-auto .ace_storage{color:#d73a49}.ace-streamlit-auto .ace_constant.ace_numeric,.ace-streamlit-auto .ace_constant.ace_language{color:#005cc5}.ace-streamlit-auto .ace_string{color:#0a6c3f}.ace-streamlit-auto .ace_comment{color:#6a737d}.ace-streamlit-auto .ace_entity.ace_name.ace_function,.ace-streamlit-auto .ace_support.ace_function{color:#6f42c1}.ace-streamlit-auto .ace_variable.ace_parameter{color:#e36209}";

    var dom = require("../lib/dom");
    dom.importCssString(exports.cssText, exports.cssClass);
});
        """.strip(),
        "github_dark": """
ace.define("ace/theme/github_dark", ["require", "exports", "module", "ace/lib/dom"], function(require, exports, module) {
    exports.isDark = true;
    exports.cssClass = "ace-github-dark";
    exports.cssText = ".ace-github-dark .ace_gutter{background:#0d1117;color:#8b949e}.ace-github-dark .ace_print-margin{width:1px;background:#30363d}.ace-github-dark{background-color:#0d1117;color:#c9d1d9}.ace-github-dark .ace_cursor{color:#c9d1d9}.ace-github-dark .ace_marker-layer .ace_selection{background:#264f78}.ace-github-dark .ace_marker-layer .ace_active-line{background:#161b22}.ace-github-dark .ace_gutter-active-line{background-color:#161b22}.ace-github-dark .ace_keyword,.ace-github-dark .ace_storage{color:#ff7b72}.ace-github-dark .ace_constant.ace_numeric,.ace-github-dark .ace_constant.ace_language{color:#79c0ff}.ace-github-dark .ace_string{color:#a5d6ff}.ace-github-dark .ace_comment{color:#8b949e}.ace-github-dark .ace_entity.ace_name.ace_function,.ace-github-dark .ace_support.ace_function{color:#d2a8ff}.ace-github-dark .ace_variable.ace_parameter{color:#ffa657}";

    var dom = require("../lib/dom");
    dom.importCssString(exports.cssText, exports.cssClass);
});
        """.strip(),
        "github_light": """
ace.define("ace/theme/github_light", ["require", "exports", "module", "ace/lib/dom"], function(require, exports, module) {
    exports.isDark = false;
    exports.cssClass = "ace-github-light";
    exports.cssText = ".ace-github-light .ace_gutter{background:#f6f8fa;color:#6e7781}.ace-github-light .ace_print-margin{width:1px;background:#d0d7de}.ace-github-light{background-color:#ffffff;color:#24292f}.ace-github-light .ace_cursor{color:#24292f}.ace-github-light .ace_marker-layer .ace_selection{background:#b6e3ff}.ace-github-light .ace_marker-layer .ace_active-line{background:#f6f8fa}.ace-github-light .ace_gutter-active-line{background-color:#f6f8fa}.ace-github-light .ace_keyword,.ace-github-light .ace_storage{color:#cf222e}.ace-github-light .ace_constant.ace_numeric,.ace-github-light .ace_constant.ace_language{color:#0550ae}.ace-github-light .ace_string{color:#0a3069}.ace-github-light .ace_comment{color:#6e7781}.ace-github-light .ace_entity.ace_name.ace_function,.ace-github-light .ace_support.ace_function{color:#8250df}.ace-github-light .ace_variable.ace_parameter{color:#953800}";

    var dom = require("../lib/dom");
    dom.importCssString(exports.cssText, exports.cssClass);
});
        """.strip(),
    }
    if theme_name not in bundled_themes:
        raise KeyError(f"Unsupported bundled Ace theme: {theme_name}")
    return bundled_themes[theme_name]


def _ace_theme_path(theme_name: str) -> Path | None:
    """Return the component path for a given Ace theme file."""
    try:
        import streamlit_ace

        return (
            Path(streamlit_ace.__file__).resolve().parent
            / "frontend"
            / "build"
            / f"theme-{theme_name}.js"
        )
    except Exception:
        return None


def _ensure_custom_ace_theme(theme_name: str) -> bool:
    """Ensure a custom Ace theme exists and is registered; return True when usable."""
    if st_ace is None:
        return False

    theme_path = _ace_theme_path(theme_name)
    if theme_path is None:
        return False

    try:
        if not theme_path.exists():
            theme_path.write_text(_load_bundled_ace_theme(theme_name), encoding="utf-8")
    except Exception:
        # Keep the app usable even if site-packages is read-only.
        return False

    if not theme_path.exists():
        return False

    if theme_name not in ACE_THEMES:
        ACE_THEMES.append(theme_name)
    return True

# ──────────────────────────── Page config ────────────────────────────
st.set_page_config(
    page_title="Albumentations Sandbox",
    page_icon="🎨",
    layout="wide",
)

st.markdown(
    """
    <style>
    div[data-testid="stButton"] > button {
        font-size: 1rem;
        min-height: 2.4rem;
        padding: 0.45rem 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
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

if "pipeline_steps" not in st.session_state:
    st.session_state.pipeline_steps = []

if "next_pipeline_step_id" not in st.session_state:
    st.session_state.next_pipeline_step_id = 1

if "pipeline_step_order" not in st.session_state:
    st.session_state.pipeline_step_order = []


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
    """Use Streamlit-aware custom theme when possible; otherwise use built-ins."""
    preferred_theme = "streamlit_auto"
    if _ensure_custom_ace_theme(preferred_theme):
        return preferred_theme

    # Fallback to standard themes if custom theme injection fails
    # Detect dark mode using Streamlit's session state (works everywhere)
    prefer_dark = False

    # Initialize theme detection in session state
    if "theme_dark" not in st.session_state:
        st.session_state.theme_dark = False

    # Use JavaScript to detect the actual theme and store in session state
    theme_script = """
    <script>
        const observer = new MutationObserver(() => {
            const isDark = window.parent.document.body.classList.contains('stAppViewContainer') &&
                          window.parent.document.documentElement.getAttribute('data-theme') === 'dark';
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: isDark}, '*');
        });
        observer.observe(window.parent.document.documentElement, {attributes: true, attributeFilter: ['data-theme']});

        // Initial check
        const isDark = window.parent.document.documentElement.getAttribute('data-theme') === 'dark';
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: isDark}, '*');
    </script>
    """

    # Try to detect from background color as a simpler approach
    try:
        # Check if we can get theme from Streamlit's internal state
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        ctx = get_script_run_ctx()
        if ctx and hasattr(ctx, 'session_state'):
            prefer_dark = st.session_state.get("theme_dark", False)
    except Exception:
        pass

    # Fallback: check background color option
    if not prefer_dark:
        bg_color = st.get_option("theme.backgroundColor")
        if bg_color:
            # Dark themes typically have dark background colors
            # Convert hex to brightness
            bg_color = bg_color.lstrip('#')
            if len(bg_color) == 6:
                r, g, b = int(bg_color[0:2], 16), int(bg_color[2:4], 16), int(bg_color[4:6], 16)
                brightness = (r * 299 + g * 587 + b * 114) / 1000
                prefer_dark = brightness < 128

    # These are standard Ace themes guaranteed to be in streamlit-ace
    return "monokai" if prefer_dark else "chrome"


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


def _default_params_for_entry(entry: dict[str, Any]) -> dict[str, Any]:
    return {param_def[0]: param_def[2] for param_def in entry["params"]}


def _render_step_params(step: dict[str, Any]) -> None:
    step_id = step["id"]
    aug_name = step["name"]
    entry = AUGMENTATION_REGISTRY[aug_name]

    step["p"] = st.slider(
        "Probability",
        min_value=0.0,
        max_value=1.0,
        value=float(step.get("p", 1.0)),
        step=0.05,
        key=f"step_{step_id}_p",
    )

    params: dict[str, Any] = {}
    current_params = step.get("params", {})
    for param_def in entry["params"]:
        pname, ptype, pdefault, *prest = param_def
        current_value = current_params.get(pname, pdefault)
        if ptype == "int":
            pmin, pmax, pstep = prest
            val = st.slider(
                pname,
                min_value=int(pmin),
                max_value=int(pmax),
                value=int(current_value),
                step=int(pstep),
                key=f"step_{step_id}_{pname}",
            )
        elif ptype == "float":
            pmin, pmax, pstep = prest
            val = st.slider(
                pname,
                min_value=float(pmin),
                max_value=float(pmax),
                value=float(current_value),
                step=float(pstep),
                key=f"step_{step_id}_{pname}",
            )
        elif ptype == "bool":
            val = st.checkbox(
                pname,
                value=bool(current_value),
                key=f"step_{step_id}_{pname}",
            )
        elif ptype == "select":
            options = prest[0]
            val = st.selectbox(
                pname,
                options=options,
                index=options.index(current_value) if current_value in options else 0,
                key=f"step_{step_id}_{pname}",
            )
        elif ptype in {"text", "literal"}:
            val = st.text_input(
                pname,
                value=str(current_value),
                key=f"step_{step_id}_{pname}",
            )
        else:
            val = current_value
        params[pname] = val

    step["params"] = params


def _sync_pipeline_step_order() -> None:
    """Keep ordered step id list in sync with current step records."""
    known_ids = [step["id"] for step in st.session_state.pipeline_steps]
    current_order = [sid for sid in st.session_state.pipeline_step_order if sid in known_ids]
    missing_ids = [sid for sid in known_ids if sid not in current_order]
    st.session_state.pipeline_step_order = current_order + missing_ids


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

for cat, aug_names in categories.items():
    with st.sidebar.expander(f"**{cat}**", expanded=False):
        for aug_name in aug_names:
            count = sum(1 for step in st.session_state.pipeline_steps if step["name"] == aug_name)
            row_col1, row_col2 = st.columns([5, 2])
            with row_col1:
                label = f"{aug_name} ({count})" if count else aug_name
                st.caption(label)
            with row_col2:
                if st.button("+", key=f"add_{aug_name}", width="stretch"):
                    entry = AUGMENTATION_REGISTRY[aug_name]
                    new_id = st.session_state.next_pipeline_step_id
                    st.session_state.pipeline_steps.append(
                        {
                            "id": new_id,
                            "name": aug_name,
                            "p": 1.0,
                            "params": _default_params_for_entry(entry),
                        }
                    )
                    st.session_state.pipeline_step_order.append(new_id)
                    st.session_state.next_pipeline_step_id += 1
                    st.rerun()

_sync_pipeline_step_order()
step_by_id = {step["id"]: step for step in st.session_state.pipeline_steps}
selected_steps = [
    step_by_id[step_id]
    for step_id in st.session_state.pipeline_step_order
    if step_id in step_by_id
]

st.sidebar.divider()
st.sidebar.subheader("Pipeline Steps")
with st.sidebar:
    if not selected_steps:
        st.caption("Use Add in the sections above to insert one or more augmentation steps.")

    if selected_steps:
        st.caption("Reorder steps with the arrow buttons on each parameter box.")

    for idx, step in enumerate(selected_steps, start=1):
        with _outlined_container():
            st.markdown(f"**{step['name']}**")

            up_col, down_col, dup_col, remove_col = st.columns([1, 1, 1, 1])
            with up_col:
                if st.button(
                    ":material/arrow_upward:",
                    key=f"move_up_{step['id']}",
                    width="stretch",
                    help="Move step up",
                    disabled=idx == 1,
                ):
                    order = list(st.session_state.pipeline_step_order)
                    pos = order.index(step["id"])
                    order[pos - 1], order[pos] = order[pos], order[pos - 1]
                    st.session_state.pipeline_step_order = order
                    st.rerun()
            with down_col:
                if st.button(
                    ":material/arrow_downward:",
                    key=f"move_down_{step['id']}",
                    width="stretch",
                    help="Move step down",
                    disabled=idx == len(selected_steps),
                ):
                    order = list(st.session_state.pipeline_step_order)
                    pos = order.index(step["id"])
                    order[pos], order[pos + 1] = order[pos + 1], order[pos]
                    st.session_state.pipeline_step_order = order
                    st.rerun()
            with dup_col:
                if st.button(
                    ":material/content_copy:",
                    key=f"dup_step_{step['id']}",
                    width="stretch",
                    help="Duplicate step",
                ):
                    new_id = st.session_state.next_pipeline_step_id
                    st.session_state.pipeline_steps.insert(
                        idx,
                        {
                            "id": new_id,
                            "name": step["name"],
                            "p": step.get("p", 1.0),
                            "params": dict(step.get("params", {})),
                        },
                    )
                    current_pos = st.session_state.pipeline_step_order.index(step["id"])
                    st.session_state.pipeline_step_order.insert(current_pos + 1, new_id)
                    st.session_state.next_pipeline_step_id += 1
                    st.rerun()
            with remove_col:
                if st.button(
                    ":material/delete:",
                    key=f"remove_step_{step['id']}",
                    width="stretch",
                    help="Remove step",
                ):
                    remove_id = step["id"]
                    st.session_state.pipeline_steps = [
                        s for s in st.session_state.pipeline_steps if s["id"] != remove_id
                    ]
                    st.session_state.pipeline_step_order = [
                        sid for sid in st.session_state.pipeline_step_order if sid != remove_id
                    ]
                    st.rerun()
            _render_step_params(step)

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
if selected_steps:
    try:
        pipeline = build_pipeline(selected_steps)
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

st.subheader("Pipeline Code")
generated_code = generate_code(selected_steps)
if (
    not st.session_state.custom_code
    or generated_code != st.session_state.last_generated_code
):
    st.session_state.custom_code = generated_code
    st.session_state.last_generated_code = generated_code
    st.session_state.custom_editor_version += 1

editor_col, actions_col = st.columns([4, 1])
ace_theme = _get_editor_theme()

with actions_col:
    run_custom = st.button("Run code", key="run_custom_code", width="stretch")
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
            ace_key = f"custom_code_ace_{st.session_state.custom_editor_version}_{ace_theme}"
            ace_editor = cast(Any, st_ace)
            edited_code = ace_editor(
                value=st.session_state.custom_code,
                language="python",
                theme=ace_theme,
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

if selected_steps:
    overview_rows: List[dict[str, Any]] = []
    param_rows: List[dict[str, str]] = []
    for idx, step in enumerate(selected_steps, start=1):
        name = step["name"]
        params = step.get("params", {})
        overview_rows.append(
            {
                "Step": idx,
                "Augmentation": name,
                "Probability (p)": f"{step.get('p', 1.0):.2f}",
                "Parameter count": len(params),
            }
        )
        if params:
            for pname, pvalue in params.items():
                param_rows.append(
                    {
                        "Step": idx,
                        "Augmentation": name,
                        "Parameter": pname,
                        "Value": _format_summary_value(pvalue),
                    }
                )
        else:
            param_rows.append(
                {
                    "Step": idx,
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
    st.info("Select augmentations from the sidebar to get started!")

# Footer
st.divider()
st.caption(
    "Built with [Streamlit](https://streamlit.io) & "
    "[Albumentations](https://albumentations.ai)"
)
