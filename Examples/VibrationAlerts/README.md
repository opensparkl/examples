# Vibration Alerts example
_In this example we use SPARKL to generate a vibration alert if the variable Vibration exceeds 100 at least 3 times in any 10-minute fixed timeslot._

### 1. Getting the code
You can either:
* Clone the whole repository from git
* Save the source code of this particular example by:
    * Right-clicking [this link](https://raw.githubusercontent.com/sparkl/examples/master/Examples/VibrationAlerts/VibrationAlerts.xml)
    * Clicking **Save Link As...**

### 2. Running the mix
_If the example is not in your configuration tree yet, you need to import it into the Developer Console. See [how](https://github.com/sparkl/examples#use_examples)._

1. Select the `Mix` view of the configuration in the Navigation Tree panel.
2. Click the `SensorReading` operation.
3. Enter a number of 100 or higher.
4. Click **Test**.
5. Repeat steps **2** and **3** twice within 10 minutes.

![vibr_alert](https://cloud.githubusercontent.com/assets/17043451/25706508/8f08d744-30d8-11e7-8dba-d600ff77b3f1.png)

### 3. So how does it work?
Read an [explanation](http://docs.sparkl.com/#TopicRoot/Examples/expr_examples/triggering_vibration_alerts_c.html) of the mix.