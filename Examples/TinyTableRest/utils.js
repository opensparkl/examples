function WithIndex(list) {
  var list_with_index = [];
  
  for (i = 0; i < list.length; i++) {
    if (list[i] != undefined) {
      list_with_index.push(i + ": " + list[i]);
    }
  }
  return list_with_index;
};

function KeyInList(key, list) {
  if (key > list.length -1) {
    return false;
        
  } else if (list[key] == undefined) {
    return false;
        
  } else {
    return true;      
  }
};

function validInput(value, min_length, max_length) {
  var str_length = value.trim().length;

  if (value == "undefined"){
    return false
  
  } else if (max_length < str_length || str_length < min_length) {
    return false
  
  } else {
    return true;
  }
};