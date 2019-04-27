function (keys, values, rereduce) {
  var result = 0;
  if (rereduce) {
    values.forEach(function (v) {
      result += v;
    });
  } else {
    values.forEach(function (vObj) {
      result += vObj.followers * vObj.textlength;
    });
  }
  return (result);
}