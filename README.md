# Melcloud AC Control 

This library allows to control whatever Mitsubishi AC device connected to Mistubishi Melcloud

## Getting Started

The requirements to allow handling this device are: a Mitsubishi split, that supports the MAC-567IF-E interface.
See http://library.mitsubishielectric.co.uk/pdf/search/MAC-567IF, and Mistubishi Melcloud account, https://www.melcloud.com/ 

### Prerequisites

Our AC device, will be registered in the Melcloud plattform, in order to be used by our library.

For example:
The device:
![MyLivingRoomAC](https://fcopuerto.github.io/docs/melget/MyLivingRoom.png) which is setup in the builindg myBulding, can be controlled with the API:
![MyLivingRoomAC](https://fcopuerto.github.io/docs/melget/MyLivingRoomAC_Details.png)

## Capabilities
- Start AC
- Stop AC
- Set temperature
- Set fun speed
- Get temperature of the room
- Get temperature of the room, target temperature and fan speed


### Installing

This serverless library, should be deployed as a Lambda, runing Python 3.7 in AWS. 
Tha handler of this lambda will be indexhandler the dependent library Melget should also be deployed which
will take in charge of the communication with the Mitubishi device through Melcloud.

This library was mad to bein used from Amazon Alexa https://developer.amazon.com

## Running the tests

Not available yet

### Break down into end to end tests

Not available yet

```
Give an example: Not available yet
```

### And coding style tests

Not available yet

```
Give an example: Not available yet
```

## Deployment

See deploy.yml file.

## Built With

* [Python3](https://docs.python.org/release/3.7.3/) - The main code used
* [AWS Lambda](https://aws.amazon.com/es/lambda/) - The serverless infrastucture


## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Fran Puerto ** - *Initial work* - (https://github.com/fcopuerto)

See also the list of [contributors](https://github.com/fcopuerto/melget/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* This driver is not official, so it's done with reverse engineering, because Mitsubishi didn't publish its Melcloud API.
* Soon updates and Alexa integration

