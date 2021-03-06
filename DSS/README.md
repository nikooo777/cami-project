 
 DSS -  Decision support system
===================
----------
System architecture
-------------
Current implementation of the system. 

![current state of the system](https://github.com/cami-project/cami-project/blob/196-DSS-implementation/DSS/Readme%20Assets/Current%20state.png?raw=true)

The diagram below represents how final architecture should look like.

![final product](https://github.com/cami-project/cami-project/blob/196-DSS-implementation/DSS/Readme%20Assets/Message%20router.png?raw=true)

How to run
-------------
```
mono DSS.Main.exe
```
Make sure **Mono** is installed on the system. (http://www.mono-project.com) 

How to run inside of docker
-------------

Navigate to the root folder **cami-project/DSS** and execute following commands.
```
docker build -t inital-docker-test .
docker run -i inital-docker-test
```

How it works
-------------

![console interface](https://github.com/cami-project/cami-project/blob/196-DSS-implementation/DSS/Readme%20Assets/Console%20interface.png?raw=true)


In case option number one is selected mockup manager creates a fake fall event, pushes it to the RabbitMQ broker,  read it from there and handle it by two channels (CONSOLE and NOTIFICATION). The **PushNotificationHandler** is responsible for taking the message and pushing it back to the RabbitMQ inside of the **frontend_notifications** queue.

The option number two gives the interface for inputing custom the event properties. 


Message format
-------------
All the messages before encoded and pushed to the CAMI RabbitMQ broker are converted into following JSON format:  
```
{ 
	"Name" : "Fall",
	"Type" : "Fall",
	"Val"  : "High"
}
```


Message routing
-------------
All the event/messages types have to be registered and assigned to a specific channel.  Configuration is done in JSON file and look like this:

```
{
  "url": "amqp://cami:cami@141.85.241.224:5673/cami",
  "port": "5673",
  "channels": [
    {
      "name": "CONSOLE",
      "events": [ "Fall" ]
    },
    {
      "name": "NOTIFICATION",
      "events": [ "Fall" ]

    }
  ]
}

```


Download
-------------
Last updated: 31, May. 2017

https://www.dropbox.com/sh/w2ots7t45nf1n0s/AAD59UFT_2yk98UWe2IFx4xga?dl=0 










































































































































































































































































































































































































































































































 
