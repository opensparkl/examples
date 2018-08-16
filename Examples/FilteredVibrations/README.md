# Filtered Vibrations example
_In this example we use conditionalized subroutines. Depending on the value of a vibration generated in the master transaction, one of three subroutines fires._

### 1. Getting the code
You can either:
* Clone the whole repository from git
* Save the source code of this particular example by:
    * Right-clicking [this link](https://raw.githubusercontent.com/sparkl/examples/master/Examples/FilteredVibrations/FilteredVibrations.xml)
    * Clicking **Save Link As...**

### 2. Running the mix
_If the example is not in your configuration tree yet, you need to import it into the Developer Console. See [how](https://github.com/sparkl/examples#use_examples)._

1. Select the `Vibrations` service.
2. Start it by clicking the play symbol.

As soon as you start the service, the `GenVibr` notify operation fires. 
It keeps firing every 30 seconds as long as the service is running.

![vibr_subr_mix](https://cloud.githubusercontent.com/assets/17043451/25705876/b76286c4-30d6-11e7-873e-9eb665e53a2d.png)


### 3. So how does it work?
Read an [explanation](http://docs.sparkl.com/#TopicRoot/Examples/mixed_examples/vibrations__filtered_subroutines_c.html) of the mix. 
