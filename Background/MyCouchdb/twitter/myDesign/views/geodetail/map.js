function (doc) {
  // var count = 5000;
  count = Math.floor(Math.random() * 1000)
  properties = {
    "name": doc.properties.name,
    "cartodb_id": doc.properties.cartodb_id
  }
  emit(properties, count);
}
