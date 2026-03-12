ace.define("ace/theme/github_light", ["require", "exports", "module", "ace/lib/dom"], function(require, exports, module) {
    exports.isDark = false;
    exports.cssClass = "ace-github-light";
    exports.cssText = ".ace-github-light .ace_gutter{background:#f6f8fa;color:#6e7781}.ace-github-light .ace_print-margin{width:1px;background:#d0d7de}.ace-github-light{background-color:#ffffff;color:#24292f}.ace-github-light .ace_cursor{color:#24292f}.ace-github-light .ace_marker-layer .ace_selection{background:#b6e3ff}.ace-github-light .ace_marker-layer .ace_active-line{background:#f6f8fa}.ace-github-light .ace_gutter-active-line{background-color:#f6f8fa}.ace-github-light .ace_keyword,.ace-github-light .ace_storage{color:#cf222e}.ace-github-light .ace_constant.ace_numeric,.ace-github-light .ace_constant.ace_language{color:#0550ae}.ace-github-light .ace_string{color:#0a3069}.ace-github-light .ace_comment{color:#6e7781}.ace-github-light .ace_entity.ace_name.ace_function,.ace-github-light .ace_support.ace_function{color:#8250df}.ace-github-light .ace_variable.ace_parameter{color:#953800}";

    var dom = require("../lib/dom");
    dom.importCssString(exports.cssText, exports.cssClass);
});

