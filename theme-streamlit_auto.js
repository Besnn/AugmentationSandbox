ace.define("ace/theme/streamlit_auto", ["require", "exports", "module", "ace/lib/dom"], function(require, exports, module) {
    exports.isDark = false;
    exports.cssClass = "ace-streamlit-auto";
    exports.cssText = ".ace-streamlit-auto .ace_gutter{background:var(--secondary-background-color,#f0f2f6);color:var(--text-color,#262730)}.ace-streamlit-auto .ace_print-margin{width:1px;background:var(--secondary-background-color,#e6e9ef)}.ace-streamlit-auto{background-color:var(--background-color,#ffffff);color:var(--text-color,#262730)}.ace-streamlit-auto .ace_cursor{color:var(--text-color,#262730)}.ace-streamlit-auto .ace_marker-layer .ace_selection{background:color-mix(in srgb, var(--primary-color,#ff4b4b) 28%, transparent)}.ace-streamlit-auto .ace_marker-layer .ace_active-line{background:color-mix(in srgb, var(--secondary-background-color,#f0f2f6) 82%, transparent)}.ace-streamlit-auto .ace_gutter-active-line{background:color-mix(in srgb, var(--secondary-background-color,#f0f2f6) 82%, transparent)}.ace-streamlit-auto .ace_keyword,.ace-streamlit-auto .ace_storage{color:#d73a49}.ace-streamlit-auto .ace_constant.ace_numeric,.ace-streamlit-auto .ace_constant.ace_language{color:#005cc5}.ace-streamlit-auto .ace_string{color:#0a6c3f}.ace-streamlit-auto .ace_comment{color:#6a737d}.ace-streamlit-auto .ace_entity.ace_name.ace_function,.ace-streamlit-auto .ace_support.ace_function{color:#6f42c1}.ace-streamlit-auto .ace_variable.ace_parameter{color:#e36209}";

    var dom = require("../lib/dom");
    dom.importCssString(exports.cssText, exports.cssClass);
});

