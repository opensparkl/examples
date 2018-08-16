# Slack library mix
This library mix can be used to send data generated in a SPARKL transaction as a Slack message.

### Using the library mix
  1. Create a Slack custom integration (incoming webhook) to be able to send messages to a Slack channel.
   > See [Slack API documentation](https://api.slack.com/).
  2. Edit the `Slack` service by changing the `url` attribute of the `slack` property to match the URL of the incoming webhook.
  3. Add a service that has:
     * The `subr.import` property
     * With the key `lib.slack.Slack`
     * Specifying the user - `demo_lib@sparkl.com`, from whose tree the mix is imported from 

     ```xml
     <service name="LibSlack" provision="subr">
       <prop name="subr.import" key="lib.slack.Slack" user="demo_lib@sparkl.com"/>
     </service>
     ```

  4. Add a consume operation that:
     * Is implemented by the service just added
     * Is named `SendMessage`
     * Receives the following three fields:
       * `colour` sets the theme of the message (e.g. green)
       * `heading` is the heading of the message
       * `map` should be a valid Erlang map, where the key is the heading of the message and the value is the value of the message 
     ```xml
     <consume name="SendMessage" 
       service="LibSlack" 
       fields="colour heading map"/>
     ```
  
