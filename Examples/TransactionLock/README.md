# Transaction Lock example
_When embedded as part of a larger configuration, a lock service enables operations which might otherwise occur simultaneously in different transactions to be serialized until the whole transaction is completed._

### 1. Getting the code
You can either:
* Clone the whole repository from git
* Save the source code of this particular example by:
    * Right-clicking [this link](https://raw.githubusercontent.com/opensparkl/examples/master/Examples/TransactionLock/TransLock.xml)
    * Clicking **Save Link As...**

### 2. Running the mix
_If the example is not in your configuration tree yet, you need to import it into the Developer Console. See [how](https://github.com/opensparkl/examples#use_examples)._

1. Specify the field `LOCK` in the request or consume fields for any given operation
2. Specify the condition under which the unlock occurs in a consume operation

![trans_lock](https://cloud.githubusercontent.com/assets/17043451/25706548/a6e1718c-30d8-11e7-9585-200a58ca2961.png)