/**
* @Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
* @Author <miklos@sparkl.com> Miklos Duma.
*
* HTML transformations and client-side SPARKL implementation.
*/


/** Invoked on clicking the Submit button. The function sends
* the submitted name to SPARKL to evaluate it.
*
* If the evaluation succeeds, creates a new row with the
* name and the ID SPARKL assigned to it.
*/
function insertName() {

  // Collect the value of the input field.
  const input_field = document.getElementById("name_input");
  const input_val = input_field.value;

  // Callback function run against the SPARKL response.
  var checkResult = (result) => {
    if (result.response == "Error") {
      window.alert(result.data.error);
        
    } else {
      input_field.value = "";
    }
  };

  // Trigger SPARKL solicit.
  service.solicit({
    solicit: "API/Insert",
    data:{
      name: input_val
    }
  }, checkResult);
};

/**
* Inserts a new row to the table upon receiving
* an ID and name. Also adds a third column with
* a button to delete the row.
*/
function insertRow (id, name) {

    // Get table body, and insert new row.
    var tblBody = document.getElementsByTagName("tbody")[0];
    var row = document.createElement("tr");
    row.setAttribute("id", id);
    tblBody.appendChild(row);
    
    // Add first cell with the value of "id".
    var idCell = document.createElement("td");
    var idCellText = document.createTextNode(id.toString());
    idCell.appendChild(idCellText);
    row.appendChild(idCell);

    // Add second cell with the value of "name".
    var nameCell = document.createElement("td");
    var nameCellText = document.createTextNode(name);
    nameCell.appendChild(nameCellText);
    row.appendChild(nameCell);

    // Create third - transparent cell - with delete button.
    var delCell = document.createElement("td");
    delCell.setAttribute("class", "transparent");
    var delButton = document.createElement("input");
    delButton.setAttribute("type", "button");
    delButton.setAttribute("onclick", "deleteName(this)");
    delButton.setAttribute("value", "X");
    delCell.appendChild(delButton);
    row.appendChild(delCell);
};


/** Deletes a row based on ID. */
function deleteRow(id) {
  var row = document.getElementById(id)
  row.parentNode.removeChild(row)
}


/** 
* Invokes a SPARKL solicit to delete a row of the table.
* If the solicit succeeds, the name gets deleted both from
* array known to SPARKL and the HTML table. Since the ID will
* always be correct, the evaluation cannot fail.
*/
function deleteName(button) {

  // Get the row in which the button is (button -> cell -> row).
  var my_row = button.parentNode.parentNode;

  // Callback to evaluate the SPARKL response.
  var checkDelete = response => {
    if (response.response == "Error") {
      window.alert(response.data.error);
    }
  };

  // Send SPARKL solicit.
  service.solicit({
    solicit: "API/Delete",
    data: {
      id: my_row.id.toString()
    }}, checkDelete);
};


/** 
* Creates the body of the HTML table with
* the headers and the names contained in "list".
*/
function tableCreate(list) {

  // Get table by ID and add it a table body child.
  var tbl = document.getElementById("tiny_table");
  var tblBody = document.createElement("tbody");
  tbl.appendChild(tblBody);

  // Create header row.
  var header = tbl.createTHead();
  var row = header.insertRow(0);
  var idHeader = row.insertCell(0);
  var nameHeader = row.insertCell(1);
  idHeader.innerHTML = "<b>ID</b>";
  nameHeader.innerHTML = "<b>Name</b>";

  // Add a new row per name in "list".
  for (i=0; i < list.length; i++) {
    insertRow(i, list[i]);
  };
};


/**
* Replaces the main div element, which contains the table
* and the submit form, with a single warning. Called if the
* SPARKL service goes down.
*/
function deleteMaster(service_url) {

  // Get master div element by ID and remove it.
  var master_div = document.getElementById("master")
  master_div.parentNode.removeChild(master_div)

  // Append body element with warning text.
  var body = document.getElementsByTagName("body")[0]
  var warning = document.createElement("p")
  warning.setAttribute("style", "text-align:center;color:red;")
  var text = document.createTextNode(service_url + " is closed.")
  warning.appendChild(text)

  body.appendChild(warning)
}