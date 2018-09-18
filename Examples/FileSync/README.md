# File Sync example
_This example uses a middleware mix to push changes from a master directory
tree to one or more slave directories._

Middleware mix (click to view, right-click to save):

* [FileSync](https://rawgit.com/jacobythwaites/examples/file_sync/Examples/FileSync/FileSync.xml)

Video of this example (4 minutes):

* [FileSync video](https://vimeo.com/289874337)

## Dependencies

* Use `git clone https://opensparkl/examples` to clone this repo
* The master and slave agents use the [sse_cli](https://github.com/opensparkl/sse_cli)
* The `master.py` agent uses the [watchdog](https://pythonhosted.org/watchdog/) utility which
  must be installed first.

## Instructions
1. Change to the `Examples/FileSync` directory and save it as $PKG_DIR
   ```
   cd Examples/FileSync
   export PKG_DIR=`pwd`
   ```
2. Connect and login to an OpenSPARKL node
   ```
   sparkl connect http://localhost:8000
   sparkl login admin@localhost
   ```
3. Upload the middleware mix to, say, the Scratch folder
   ```
   sparkl put FileSync.xml Scratch
   ```
4. Create an empty master directory and slave directory
5. Go into the master directory, then start the master agent in it
   ```
   sparkl service -p $PKG_DIR Scratch/FileSync/Master master
   ```
5. Go into the slave directory, then start the slave agent in it
   ```
   sparkl service -p $PKG_DIR Scratch/FileSync/Slave slave
   ```

Now go ahead and make changes to the master directory, see them 
propagated to the slave.
