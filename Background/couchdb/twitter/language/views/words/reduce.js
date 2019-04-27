function (keys, values, rereduce) {
  var langs = [];
  var count = 0;
  if (!rereduce) {
    keys.forEach(function (key) {
      var lang = key[0][1];
      if (langs.indexOf(lang) < 0) {
        langs.push(lang);
      }
      count++;
    });
  } else {
    values.forEach(function (value) {
      value.languages.forEach(function (lang) {
        if (langs.indexOf(lang) < 0) {
          langs.push(lang);
        }
        count += value.count;
      });
    });
  }
  return {languages: langs, count: count};
}