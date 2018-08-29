# Traffic Lights Subroutines example
_This version of the Traffic Lights example uses a subroutine transaction to decide whether the pedestrian crossing button was pushed. 
If it was, the traffic lights in the junction change for a short period to allow for pedestrian crossing. 
The junction and the button are both represented as stateful svc_expr services._

### 1. Getting the code
You can either:
* Clone the whole repository from git
* Save the source code of this particular example by:
    * Right-clicking [this link](https://raw.githubusercontent.com/opensparkl/examples/master/Examples/TrafficSubr/Traf_Lig_Subr.xml)
    * Clicking **Save Link As...**

### 2. Running the mix
_If the example is not in your configuration tree yet, you need to import it into the Developer Console. See [how](https://github.com/opensparkl/examples#use_examples)._

#### 2.1 Installing the traffic lights
_The junction with the traffic and pedestrian lights is represented as the `Junction` service._
  1. Select the `Junction` service in the Navigation Tree Panel.
  2. Start the service by clicking the play symbol.

As long as the service is running, it fires the `Start` notify operation every 15 seconds to update the traffic lights.

By default, the traffic lights are set to green and the pedestrian lights are set to red. 

#### 2.2 Pressing the pedestrian button
_The pedestrian button is represented as the `Button` service._
  1. Find the `IsPressed` operation in the `SubrMix` slave mix.
  2. Click this operation.

When you click the operation, it updates the state of the `Button` service indicating someone is waiting.

In the next 15-seconds window when the `Start` notify fires, it updates the lights to allow for pedestrian crossing.

![traf_subr_mix](https://cloud.githubusercontent.com/assets/17043451/25705933/dd1bd910-30d6-11e7-91cd-bbbdb003de3c.png)