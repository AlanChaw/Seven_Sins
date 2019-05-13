function (doc) {
  emit(doc.properties.name, doc.geometry.coordinates);
}
