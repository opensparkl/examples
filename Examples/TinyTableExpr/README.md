# TinyTable Expressions example
_In this example we use SPARKL to build and maintain a small mock database._

### 1. Getting the code
You can either:
* Clone the whole repository from git
* Save the source code of this particular example by:
    * Right-clicking [this link](https://raw.githubusercontent.com/opensparkl/examples/master/Examples/TinyTableExpr/TinyTable_Expr.xml)
    * Clicking **Save Link As...**

### 2. Running the mix
_If the example is not in your configuration tree yet, you need to import it into the Developer Console. See [how](https://github.com/opensparkl/examples#use_examples)._

1. Select the `Mix` view of the configuration in the Navigation Tree panel.
2. Click either:
   * `ListNames` - to retrieve all records from the database
   * `DeleteName` - to delete a record from the database
   * `InsertName` - to add a new record to the database
   * `GetName` - to get the record that matches the specified key
3. Depending on the operation selected, you either need to:
   * Simply click **Test** to retrieve all records (`ListNames`)
   * Specify the key of the record you want to delete and click **Test** (`DeleteName`)
   * Type in a first and last name for a new record and click **Test** (`InsertName`)
   * Specify the key of the record you want to retrieve and click **Test** (`GetName`)
  
![tinytable_expr](https://cloud.githubusercontent.com/assets/17043451/25705812/824278a0-30d6-11e7-9aa2-bf8fd20e2972.png)