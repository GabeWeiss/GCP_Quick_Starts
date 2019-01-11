const {google} = require('googleapis');

/*
  Variable block. Should be the only pieces needing editing
*/

// Note, this is BAD for production, don't do this. The service account
// private data should be passed into this function so it's encrypted in
// transit, and so you don't have it static as you may want to change
// permission levels, etc. For the purposes of this blog demo code, I've
// done it for ease of calling and to just show what the data looks like.
// Please please don't do this in production.
var serviceAccount = '<paste contents of the service account json blob here>';

// You shouldn't need to change this variable, it's here for illustration
// purposes. An advantage of calling a Cloud Function within the same project
// is that there are certain environment varibales you get for free like this
// one
var projectId = process.env.GCP_PROJECT;

// change the following to match your project's values
// you could also easily modify the code to receieve these as variables
// in the GET call since I'm relying on that for the config/command switch
// as well as the actual message being sent
var registryId = '<registry_id>';
var deviceId = '<device_id>';

// a couple default values just for the sake of having something there
var msg = "clear"; // by default will reset the LED matrix
var which = "config"; // by default will send a config message

/*
  END VARIABLE BLOCK
*/

/*
  Responds to a HTTP request and updates the specified
  IoT device with either a config or a command depending on
  what is specified in the GET parameter (defaults to config).
 
  @param {Object} req Cloud Function request context.
  @param {Object} res Cloud Function response context.
*/
exports.updateDevice = (req, res) => {

  // variable passed into the Cloud function (as GET or POST)
  const reqMsg = req.query.message;
  // if we didn't pass one in, then just take our default
  const finalMsg = reqMsg ? reqMsg : msg;
  const msgData = Buffer.from(finalMsg).toString('base64');

  // the full path to our device in GCP
  var devicePath = `projects/${projectId}/locations/us-central1/registries/${registryId}/devices/${deviceId}`;

  // This chunk is what authenticates the function with the API so you can
  // call the IoT Core APIs
  const jwtAccess = new google.auth.JWT();
  jwtAccesss.fromJSON(serviceAccount);
  // Note that if you require additional scopes, they should be specified as a
  // string, separated by spaces
  jwtAccess.scopes = 'https://www.googleapis.com/auth/cloud-platform';
  // Set the default authenticatio nto the above JWT access
  google.options({ auth: jwtAccess });


  // And here we have the actual call to the cloudiot REST API for updating a
  // configuration on the device
  var client = google.cloudiot('v1');
  if (which == "config") {
    // This is the blob send to the IoT Core Admin API
    const configRequest = {
      name: devicePath,
      versionToUpdate: '0',
      binaryData: msgData
    };
    client.projects.locations.registries.devices.modifyCloudToDeviceConfig(configRequest,
      (err, data) => {
        if (err) {
          console.log('Message: ', err);
          console.log('Could not update config:', deviceId);
        } else {
          console.log('Success :', data);
        }
      }
    );
  }
  else if (which == "command") {
    const commandRequest = {
      name: devicePath,
      binaryData: msgData
    };
    client.projects.locations.registries.devices.sendCommandToDevice(commandRequest,
      (err, data) => {
        if (err) {
          console.log('Message: ', err);
          console.log('Could not update command:', deviceId);
        } else {
          console.log('Success :', data);
        }
      }
    );
  }

  res.status(200).end();
};
