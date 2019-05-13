function (doc) {
  if (doc.related == 1){
    key = {
      "name": doc.suburb
    }
    value = doc.sentiment
    emit(key, value)
  }
}
