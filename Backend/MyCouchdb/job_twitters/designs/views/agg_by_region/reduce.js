function (keys, values, rereduce) {
  return_value = {
      "positive": 0,
      "negative": 0,
      "neutral": 0,
      "total": 0
    };
  if (rereduce) {
    for (value in values){
      return_value.positive += values[value].positive
      return_value.negative += values[value].negative
      return_value.neutral += values[value].neutral
      return_value.total += values[value].total
    }
    return return_value

  } else {
    for (value in values){
      if (values[value] == "pos"){
        return_value.positive += 1
      }
      if (values[value] == "neg"){
        return_value.negative += 1;
      }
      if (values[value] == "neu"){
        return_value.neutral += 1;
      }
      return_value.total += 1;
    }
    return return_value;
  }
}
