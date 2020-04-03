module.exports = {
    "plugins": [
      "import"
    ],
    "env": {
        "browser": true,
    },
    "extends": [
        "eslint:recommended", 
        "airbnb"
    ],
    "rules": {
        "indent": [2, 4, {SwitchCase: 1}],
        "quotes": [2, "double"],
        "react/jsx-indent": [2, 4, {checkAttributes: true}],
        "react/jsx-indent-props": [2, 4],
        "react/jsx-filename-extension": [1, { "extensions": [".jsx"] }],
        "react/jsx-no-bind": [2, {allowBind: true}],
        "jsx-a11y/label-has-for": [0], // Deprecated since october 2018
        "jsx-a11y/media-has-caption": [0],
        "react/forbid-prop-types": [false],
    },
    "settings": {
        "import/resolver": {
            node: { 
                extensions: [
                    ".js",
                    ".jsx",
                ]
            }
        }
    }
};