﻿using System;
using DSS.Delegate;
using DSS.FuzzyInference;
using DSS.RMQ;
using Newtonsoft.Json;
using System.Net.Http;
using System.Text;

namespace DSS.Main
{
    
    class Program
    {
        
        public static void Main(string[] args)
        {
            Console.WriteLine("DSS invoked...");
			Console.WriteLine("Connecting to the msg broker...");

            //var rmqAPI = new RmqAPI("http://141.85.241.224:8010/api/v1/insertion");
            //rmqAPI.PushEvent(new Event("Fall").ToJson());
            //rmqAPI.PushNotification("{  user_id: 2,  message: \"Your blood pressure is way too low!\"}");

			var router = new Router<Event>();
            var url = "amqp://cami:cami@141.85.241.224:5673/cami";

            var rmqConfig = new RmqConfig( url, "cami", "cami", "events");

            var rmq = new Rmq<Event>(url,
                              "cami",
                              "cami",
                              "test-queue",
                              (result) =>
                              {
                                Console.WriteLine("RECIEVED: " + result);
                                router.Handle(JsonConvert.DeserializeObject<Event>(result));
                             } );

            var rmqExchange = new RmqExchange(rmqConfig);


            IRouterHandler<Event>[] handlers =
            {
                new ConsolePrintHandler<Event>(),
                new PushNotificationHandler<Event>(new RmqWriter<Event>(url, "cami", "cami", "frontend_notifications")),
                new FuzzyHandler()
			};




			var config = new Config("default.config", router, handlers);


            var run = true;

            while(run)
            {
				Console.WriteLine("=========================");
                Console.WriteLine("[1] - Generate default fall event {\"Category\":\"Fall\"}");
				Console.WriteLine("[2] - Generate fall event with custom data");
                Console.WriteLine("[3] - HIGH HEART_RATE");
				Console.WriteLine("[4] - EXERCISE_MODE_ON");
				Console.WriteLine("[5] - FALL");


				Console.WriteLine("ctrl + c - Exit");
				Console.WriteLine("=========================");

                var num = Console.ReadLine();

                if (num == "1")
					// rmq.Write(JsonConvert.SerializeObject(new Event("Fall")));
                    rmq.Write(new Event("Fall").ToJson());


				if (num == "2")
                {
                    var input = new string [4];
                    Console.Write("Category: ");
                    input[0] = Console.ReadLine();
                    rmq.Write(new Event(input[0]).ToJson());
				}

                if(num == "3")
					handlers[2].Handle(new Event("Heart-Rate", new Content() { name = "Heart-Rate", val = new Value() { numVal = 90 } }, new Annotations()));
                if(num == "4")
					handlers[2].Handle(new Event("USER-INPUT", new Content() { name = "EXERCISE_MODE_ON" }, new Annotations()));
                if(num == "5")
                {
					handlers[2].Handle(new Event("IMPACT", new Content() { name = "IMPACT", val = new Value() { numVal = 90 } }, new Annotations()));
					handlers[2].Handle(new Event("ON_GROUND", new Content() { name = "ON_GROUND", val = new Value() { numVal = 1.4f } }, new Annotations()));
					handlers[2].Handle(new Event("TIME_ON_GROUND", new Content() { name = "TIME_ON_GROUND", val = new Value() { numVal = 700 } }, new Annotations()));
				}

				run = num != "6";
			}
            rmq.Dispose();

        }

    }
}
