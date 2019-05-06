function (doc) {
  area_name = doc.properties.clue_small_area;
  if (area_name == "Melbourne (CBD)"){
    area_name = "Melbourne"
  }
  if (area_name == "Melbourne (Remainder)"){
    area_name = "Melbourne"
  }
  if (area_name == "West Melbourne (Industrial)"){
    area_name = "West Melbourne"
  }
  if (area_name == "West Melbourne (Residential)"){
    area_name = "West Melbourne"
  }
  emit(area_name, 1);
}
