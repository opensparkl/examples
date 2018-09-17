/**
* @Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
* @Author <miklos@sparkl.com> Miklos Duma.
*
* Implementation of SPARKL server-side operations (i.e. requests).
*/

// Array holding all the names. 
var table = ["Jacoby", "Andrew", "Miklos"];


/** Logic behind Impl/Insert operation. */
const insertImpl = 
  (request, callback) => {
    var name = request.data.name;

    if (table.includes(name)) {
      callback({
        reply: "Error",
        data: {
          error: "Name already in table: " + name + "."
        }
      });

    } else if (!(validInput(name, 3, 16))) {
      callback({
        reply: "Error",
        data: {
          error: "Name's length must be between" + 
            " 3 and 16 characters."
        }
      });
    
    } else {
      var new_key = table.length;
      table[new_key] = name;
      insertRow(new_key, name);

      callback({
        reply: "Ok",
        data: {
          id: new_key
        }
      });
    }
  };


/** Logic behind Impl/Delete operation. */
const deleteImpl = 
  (request, callback) => {
    var id = request.data.id;
    
    if (KeyInList(id, table)) {
      callback({
        reply: "Ok",
        data: {
          name: table[id]
        }
      });
      delete table[id];
      deleteRow(id);
      
    } else {
      callback({
        reply: "Error",
        data: {
          error: "No such key: " + id + "."
        }
      });
    }
  };


/** Logic behind Impl/Get operation. */
const getImpl = 
  (request, callback) => {
    var id = request.data.id;

    if (KeyInList(id, table)) {
      callback({
        reply: "Ok",
        data: {
          name: table[id]
        }
      });
    
    } else {
      callback({
        reply: "Error",
        data: {
          error: "No such key: " + id + "."
        }
      });
    }
  };


/** Logic behind Impl/List operation. */
const listImpl = 
  (request, callback) => {
    existing_names = WithIndex(table);

    if (existing_names.length > 0) {
      callback({
        reply: "Ok",
        data: {
          all_names: existing_names.join(", ")
        }
      });

    } else {
      callback({
        reply: "Error",
        data: {
          error: "The database is empty."
        }
      }); 
    }
  };


// Map logic to operation paths.
const impl = {
  "Impl/Insert": insertImpl,
  "Impl/Delete": deleteImpl,
  "Impl/Get": getImpl,
  "Impl/List": listImpl
}


// Create websocket for SPARKL service implementation.
const service = new sparkl.Service(
  "ws://localhost:8000", "Scratch/TinyRest/Mix/REST", impl);


// Hook for service-up event. Creates the HTML table.
service.onopen = 
  () => {
    console.log("Opened: " + service.ws_url);
    tableCreate(table);
  };


// Hook for service-down event. Destroys the HTML table
// and the submit form.
service.onclose =
  () => {
    deleteMaster(service.ws_url);
    close();
  };