function (doc) {
  // var count = 5000;
  count = Math.floor(Math.random() * 1000)
  properties = {
    "name": doc.properties.name,
    "count": count
    // "cartodb_id": doc.properties.cartodb_id
  }
  emit(properties, 0);
}
