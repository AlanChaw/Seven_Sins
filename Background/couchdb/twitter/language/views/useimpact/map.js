function (doc) {
  emit([doc.user.id, doc._id], {followers: doc.user.followers_count, textlength: doc.text.split(" ").length});
}