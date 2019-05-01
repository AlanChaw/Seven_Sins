function (doc) {
  // var count = 5000;
  positive = Math.floor(Math.random() * 1000)
  negative = Math.floor(Math.random() * 1000)
  neutral = Math.floor(Math.random() * 1000)
  total = positive + negative + neutral
  key = {
    "name": doc.properties.name,
    // "cartodb_id": doc.properties.cartodb_id
  }
  values = {
    "positive": positive,
    "negative": negative,
    "neutral": neutral,
    "total": total
  }
  emit(properties, values);
}
