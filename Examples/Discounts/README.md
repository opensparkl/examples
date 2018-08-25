# Discounts Calendar example
_This example manipulates and querries an external database of discounts and sends notifications through Slack on live discounts._

## 1. Getting the code
You can either:
* Clone the whole repository from git
* Save the source code of this particular example by:
    * Right-clicking [this link](https://raw.githubusercontent.com/opensparkl/examples/master/Examples/Discounts/DiscountsCalendar.xml)
    * Clicking **Save Link As...**

## 2. Running the mix
_If the example is not in your configuration tree yet, you need to import it into the Developer Console. See [how](https://github.com/opensparkl/examples#use_examples)._

![discounts_calendar](https://cloud.githubusercontent.com/assets/17043451/26110306/db806d6a-3a49-11e7-95e6-25b1f4afa698.png)

### 2.0 Pre-requisites
* Import the [Slack library](https://github.com/opensparkl/examples/tree/master/Library/lib_slack) into your configuration tree
* Create a Slack custom integration (incoming webhook) to send messages to a Slack channel
   > See [Slack API documentation](https://api.slack.com/)
* Edit the Slack library configuration by changing the `url` attribute of the `slack` property to match the URL of the incoming webhook 
  ```xml
  <service name="Slack" provision="expr">
    ...
    <prop name="slack" url="InsertSlackChannelURL"/>
  </service>  
  ```
* If you want to use the restore script make sure you have installed the SPARKL CLI  

### 2.1 Starting notifications
1. Select the `Discounts` service.
2. Click the play symbol to start a service instance.

The `Start` notify operation on the `Discounts` service is fired every 30 minutes as long as the service instance is up.

To stop execution just kill the service instance by clicking the stop symbol. 

You get a notification if:
1. The time the notify is fired is within a discount period
2. You haven't received a notification on that discount yet

![discount_alert](https://cloud.githubusercontent.com/assets/17043451/26110594/b3a65240-3a4a-11e7-97f3-b3409d2894e8.png)

### 2.2 Managing the database
You can use the operations in the `API` folder to manipulate the database.
> The database itself is [here](https://console.firebase.google.com/u/0/project/discounts-4bb20/database/data/).
* `GetKeys` retrieves the IDs of all records in the database
* `GetRecord` retrieves a record based on ID
* `DeleteRecord` deletes a record based on ID
* `Feed` creates a new record in the DB and returns the ID assigned to it
* `Backup` saves the content of the database as an Erlang map
  > The backup file is saved to the directory of the node running SPARKL. It is named `Backup.erl`.
* `BulkFeed` creates multiple records in the DB. You can use it to restore the DB from backup.

### 2.3 Restoring the DB from backup
You can restore the DB using a Bash script. The script tries to find the `Backup.erl` file in the same directory and use it as the input of the `BulkFeed` operation. To use the script, you need to have the SPARKL CLI installed.
1. Make sure you have a valid `Backup.erl` file in the same directory as the `updateCalendar.sh` script.
2. Run the script with the following arguments:
   * The URL of the SPARKL instance you want to connect to
   * Your username that corresponds to an existing account on the SPARKL instance
   
   ```bash
   ./updateCalendar.sh https://saas.sparkl.com admin@sparkl.com
   ```




