# Secret Santa example
_In this example we use SPARKL to randomly draw names from a list, and send the names to Secret Santas through the instant message application Slack. Each Secret Santa has to buy a present for the person whose name he or she has received._

### 1. Getting the code
You can either:
* Clone the whole repository from git
* Save the source code of this particular example by:
    * Right-clicking [this link](https://raw.githubusercontent.com/opensparkl/examples/master/Examples/SecretSanta/SecretSanta.xml)
    * Clicking **Save Link As...**

### 2. Running the mix
_If the example is not in your configuration tree yet, you need to import it into the Developer Console. See [how](https://github.com/opensparkl/examples#use_examples)._

1. Create Slack custom integrations (incoming webhooks) to be able to send messages to the private channel of the participants.
   > See [Slack API documentation](https://api.slack.com/).
2. Edit the mix in the [Editor](http://docs.sparkl.com/#TopicRoot/Editor/the_editor_c.html) by customizing:
   * The name of the participants (you can add as many as you feel like)
   * The URLs that point at their private channel
3. Select the `Mix` view of the configuration in the Navigation Tree panel.  
4. Click the `Start` operation.
5. Click **Test**.

![secret_santa_mix](https://cloud.githubusercontent.com/assets/17043451/25705721/2ca3662a-30d6-11e7-9a4a-0e3594622c65.png)