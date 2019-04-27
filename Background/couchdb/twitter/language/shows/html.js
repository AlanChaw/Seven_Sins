function (doc, req) {
  var bold = (req.query.bold) ? "<b>" : "";
  return "<h2>" + doc.user.screen_name + "</h2><p>" + bold + doc.text + "</p>";
}