# Traffic Lights Expressions example
_In this example we use SPARKL to control the traffic lights at a junction. 
The junction itself, the traffic lights for cars and pedestrians, and the pedestrian crossing button are all represented in the mix as stateful services. 
The state of the junction and the pedestrian crossing button decides the state of the traffic lights, that is, whether they are green or red._

### 1. Getting the code
You can either:
* Clone the whole repository from git
* Save the source code of this particular example by:
    * Right-clicking [this link](https://raw.githubusercontent.com/opensparkl/examples/master/Examples/TrafficLightsExpr/TrafficLightsExpr.xml)
    * Clicking **Save Link As...**

### 2. Running the mix
_If the example is not in your configuration tree yet, you need to import it into the Developer Console. See [how](https://github.com/opensparkl/examples#use_examples)._

#### 2.1 Installing the traffic lights
_The junction with the traffic and pedestrian lights is represented as the `Junction` service._
  1. Select the `Junction` service in the Navigation Tree Panel.
  2. Start the service by clicking the play symbol.

On service-up, `Junction` sets the traffic lights to green and the pedestrian lights to red.

#### 2.2 Pressing the pedestrian button
_The pedestrian button is represented as the `RequestButton` service._
  1. Select the `Mix` view of the configuration in the Navigation Tree panel.
  2. Click the `Press` operation.
  
When you click the operation, it updates the state of the `RequestButton` service, indicating someone is waiting. The `GiveMode` operation on the service starts ticking. From now on, it is fired every 20 seconds. 

If within any 20-seconds window the `Press` operation is fired, the lights change to allow for pedestrian crossing. Otherwise, the pedestrian lights remain red and the traffic lights green.

![traffic_lights_mix](https://cloud.githubusercontent.com/assets/17043451/25705966/fad3e33a-30d6-11e7-926f-1d8c9d141c22.png)