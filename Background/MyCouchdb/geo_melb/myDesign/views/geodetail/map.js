function (doc) {
  // var count = 5000;
  positive = Math.floor(Math.random() * 1000);
  negative = Math.floor(Math.random() * 1000);
  neutral = Math.floor(Math.random() * 1000);
  total = positive + negative + neutral;
  key = {
    "name": doc.properties.SA2_NAME16,
    // "cartodb_id": doc.properties.cartodb_id
  };
  pos_example = "I am a positive twitter example. Very Happy!";
  neg_example = "I am a negative twitter example. F**k!";
  neu_example = "I am a neutral twitter example. Whatever.";
  values = {
    "positive": positive,
    "negative": negative,
    "neutral": neutral,
    "total": total,
    "examples":{
      "pos_example": pos_example,
      "neg_example": neg_example,
      "neu_example": neu_example
    }
  }
  emit(key, values);
}
