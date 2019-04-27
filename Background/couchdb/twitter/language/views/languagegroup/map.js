function (doc) {
  var lib = require("views/lib/lib");
  emit([lib.languageFamily(doc.user.lang), doc.user.lang], 1);
}