ace.define("ace/theme/github_dark", ["require", "exports", "module", "ace/lib/dom"], function(require, exports, module) {
    exports.isDark = true;
    exports.cssClass = "ace-github-dark";
    exports.cssText = ".ace-github-dark .ace_gutter{background:#0d1117;color:#8b949e}.ace-github-dark .ace_print-margin{width:1px;background:#30363d}.ace-github-dark{background-color:#0d1117;color:#c9d1d9}.ace-github-dark .ace_cursor{color:#c9d1d9}.ace-github-dark .ace_marker-layer .ace_selection{background:#264f78}.ace-github-dark .ace_marker-layer .ace_active-line{background:#161b22}.ace-github-dark .ace_gutter-active-line{background-color:#161b22}.ace-github-dark .ace_keyword,.ace-github-dark .ace_storage{color:#ff7b72}.ace-github-dark .ace_constant.ace_numeric,.ace-github-dark .ace_constant.ace_language{color:#79c0ff}.ace-github-dark .ace_string{color:#a5d6ff}.ace-github-dark .ace_comment{color:#8b949e}.ace-github-dark .ace_entity.ace_name.ace_function,.ace-github-dark .ace_support.ace_function{color:#d2a8ff}.ace-github-dark .ace_variable.ace_parameter{color:#ffa657}";

    var dom = require("../lib/dom");
    dom.importCssString(exports.cssText, exports.cssClass);
});

