// Copyright 2019 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package main

import (
	"context"
	b64 "encoding/base64"
	"fmt"

	"golang.org/x/oauth2/google"
	cloudiot "google.golang.org/api/cloudiot/v1"
)

/*
  Variable block. Should be the only pieces needing editing
*/

// You shouldn't need to change this variable, it's here for illustration
// purposes. An advantage of calling a Cloud Function within the same project
// is that there are certain environment varibales you get for free like this
// one
var projectId = os.Getenv("GCP_PROJECT")

// change the following to match your project's values
// you could also easily modify the code to receieve these as variables
// in the GET call since I'm relying on that for the config/command switch
// as well as the actual message being sent
var registryId = '<registry_id>'
var gcpLocation = '<project location>'
var deviceId = '<device_id>'

// a couple default values just for the sake of having something there
var msg = "clear" // by default will reset the LED matrix
var which = "config" // by default will send a config message

/*
  END VARIABLE BLOCK
*/

// getClient returns a client based on the environment variable GOOGLE_APPLICATION_CREDENTIALS
func getClient() (*cloudiot.Service, error) {
	// Authorize the client using Application Default Credentials.
	// See https://g.co/dv/identity/protocols/application-default-credentials
	ctx := context.Background()
	httpClient, err := google.DefaultClient(ctx, cloudiot.CloudPlatformScope)
	if err != nil {
		return nil, err
	}
	client, err := cloudiot.New(httpClient)
	if err != nil {
		return nil, err
	}

	return client, nil
}

func setConfig(client *cloudiot.Service) (*cloudiot.DeviceConfig, error) {
	req := cloudiot.ModifyCloudToDeviceConfigRequest{
		BinaryData: b64.StdEncoding.EncodeToString([]byte(msg)),
	}

	path := fmt.Sprintf("projects/%s/locations/%s/registries/%s/devices/%s", projectId, gcpLocation, registryId, deviceId)
	response, err := client.Projects.Locations.Registries.Devices.ModifyCloudToDeviceConfig(path, &req).Do()
	if err != nil {
		return nil, err
	}

	return response, nil
}

func main() {

	client, clientErr := getClient()

	if clientErr != nil {
		fmt.Println("Failed to get auth'd client")
	}

	_, configErr := setConfig(client)
	if configErr != nil {
		fmt.Println("Failed to configure something")
		fmt.Printf("%s", configErr)
	}

	fmt.Println("Hello world")
}
