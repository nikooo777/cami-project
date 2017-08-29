﻿using System;
using DSS.Delegate;
using DSS.FuzzyInference;
using DSS.RMQ;
using Newtonsoft.Json;
using System.Net.Http;
using System.Text;
using System.Threading;
using log4net;
using log4net.Config;
using System.Xml;

namespace DSS.Main
{
    
    class Program
    {

        private static readonly ILog log = LogManager.GetLogger(typeof(Program));

		public static void Main(string[] args)
        {
            Console.WriteLine("DSS invoked...");
			Console.WriteLine("Connecting to the msg broker...");

            XmlConfigurator.Configure(new System.IO.FileInfo("log4net.config.xml"));

            log.Info("THIS IS A MSG FROM DSS DOCKER");
            log.Debug("THIS IS A MSG FROM DSS DOCKER");



            //cami-insertion
			//var rmqAPI = new RmqAPI("amqp://cami:cami@cami-insertion:8010");
			
            var rmqAPIVS = new RmqAPI("http://cami.vitaminsoftware.com:8008");

			
            //rmqAPIVS.PushMeasuremnt("");
            //rmqAPIVS.PushJournalEntry("");
            rmqAPIVS.PushNotification("");

			//rmqAPI.PushEvent(new Event("Fall").ToJson());
			//rmqAPI.PushNotification("{  user_id: 2,  message: \"Your blood pressure is way too low!\"}");

			var router = new Router<Event>();
            //var url = "amqp://cami:cami@141.85.241.224:5673/cami";

            //var rmqConfig = new RmqConfig( url, "cami", "cami", "events");

            //var rmq = new Rmq<Event>(url,
            //                  "cami",
            //                  "cami",
            //                  "test-queue",
            //                  (result) =>
            //                  {
            //                    Console.WriteLine("RECIEVED: " + result);
            //                    router.Handle(JsonConvert.DeserializeObject<Event>(result));
            //                 } );

            //var rmqExchange = new RmqExchange(rmqConfig);


            IRouterHandler<Event>[] handlers =
            {
                new ConsolePrintHandler<Event>(),
                //new PushNotificationHandler<Event>(new RmqWriter<Event>(url, "cami", "cami", "frontend_notifications")),
                new FuzzyHandler()
			};

			var config = new Config("default.config", router, handlers);

            {
				Console.WriteLine("=========================");
				Console.WriteLine("[3] - HIGH HEART_RATE");
                Console.WriteLine("[4] - EXERCISE_MODE_ON");
                Console.WriteLine("[5] - FALL");
				Console.WriteLine("[6] - HIGH HEART_RATE every 10 sec");
				Console.WriteLine("ctrl + c - Exit");
				Console.WriteLine("=========================");

				var num = Console.ReadLine();

                if(num == "3")
					handlers[1].Handle(new Event("Heart-Rate", new Content() { name = "Heart-Rate", val = new Value() { numVal = 90 } }, new Annotations()));
                if(num == "4")
					handlers[1].Handle(new Event("USER-INPUT", new Content() { name = "EXERCISE_MODE_ON" }, new Annotations()));
                if(num == "5")
                {
					handlers[1].Handle(new Event("IMPACT", new Content() { name = "IMPACT", val = new Value() { numVal = 90 } }, new Annotations()));
					handlers[1].Handle(new Event("ON_GROUND", new Content() { name = "ON_GROUND", val = new Value() { numVal = 1.4f } }, new Annotations()));
					handlers[1].Handle(new Event("TIME_ON_GROUND", new Content() { name = "TIME_ON_GROUND", val = new Value() { numVal = 700 } }, new Annotations()));
				}
                if(num == "6")
                {
                    var timer = new Timer((handler) => {
                        Console.WriteLine("HR invoked...");
                        (handler as FuzzyHandler).Handle(new Event("Heart-Rate", new Content() { name = "Heart-Rate", val = new Value() { numVal = 90 } }, new Annotations()));

                    }, handlers[1], 1, 10000);
                }
			}
           // rmq.Dispose();

            while (true)
            {

            }


        }

    }
}
