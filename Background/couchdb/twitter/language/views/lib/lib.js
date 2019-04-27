var families = {"eu": ["es", "en", "de", "pt", "fr", "it", "ru"], "as": ["ko", "ja", "id", "zh-cn", "tr"]};
exports.languageFamily = function (lang) {
  var langFamily = null;
  Object.getOwnPropertyNames(families).forEach(function (family) {
    if (families[family].indexOf(lang) >= 0) {
      langFamily = family;
    }
  });
  return langFamily;
};