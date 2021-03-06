﻿using System;
using System.Collections.Generic;
using DSS.Delegate;
using DSS.RMQ;
using Newtonsoft.Json;

namespace DSS.FuzzyInference
{

    public class ValueInfo 
    {
		[JsonProperty("value")]
		public string Value;

    }

    public class Measurement
    {
		public string measurement_type { get; set; }
		public string unit_type { get; set; }
		public int timestamp { get; set; }
		public string user { get; set; }
		public string device { get; set; }
        public ValueInfo value_info { get; set; }
		public string gateway_id { get; set; }
        public bool ok { get; set; }
        public string id { get; set; }
        public string resource_uri { get; set; }
    }


    public class MeasurementHandler : IRouterHandler
    {
        private StoreAPI storeAPI;
        private RMQ.INS.InsertionAPI insertionAPI;
        public string Name => "MEASUREMENT";

        public MeasurementHandler()
        {

            storeAPI = new StoreAPI("http://cami-store:8008/api/v1");
			//storeAPI = new StoreAPI("http://141.85.241.224:8008/api/v1");

            insertionAPI = new RMQ.INS.InsertionAPI("http://cami-insertion:8010/api/v1/insertion");
			//insertionAPI = new RMQ.INS.InsertionAPI("http://141.85.241.224:8010/api/v1/insertion");
		}

        public void Handle(string json) 
        {
            Console.WriteLine("Measurement handler invoked");

            var obj = JsonConvert.DeserializeObject<Measurement>(json);
            obj.timestamp = (int) (DateTime.UtcNow.Subtract(new DateTime(1970, 1, 1))).TotalSeconds;


			if (obj.measurement_type == "weight")
			{
                var val = float.Parse( obj.value_info.Value);

				var kg = storeAPI.GetLatestWeightMeasurement();



               if (Math.Abs(val - kg) > 2)                {                     var msg = val > kg ? "Have lighter meals" : "Have more consistent meals";                     storeAPI.PushJournalEntry(msg, "Abnormal change in weight noticed", "weight");
                    storeAPI.PushJournalEntry("Abnormal change in weight noticed", "Abnormal change in weight noticed", "weight");

					insertionAPI.InsertPushNotification(JsonConvert.SerializeObject(new DSS.RMQ.INS.PushNotification() { message = msg, user_id = 2 }));
     
                    obj.ok = false;
				}                 else                  {                     obj.ok = true;                }             }
            else if(obj.measurement_type == "pulse") 
            {
                var val = float.Parse(obj.value_info.Value);
                var min = 50;
                var max = 120;

                if (val < min || val > max) 
                {
					obj.ok = false;

					if(storeAPI.AreLastNHeartRateCritical(3, min, max)) 
                    {
                        var anEvent = new RMQ.INS.Event() { category = "HEART_RATE", content = new RMQ.INS.Content() { num_value = val } };
                        insertionAPI.InsertEvent( JsonConvert.SerializeObject(anEvent));
                    }

				    storeAPI.PushJournalEntry("Pulse is abnormal", "Pulse is abnormal", "pulse");
				}
                else 
                {
                    obj.ok = true;
				}
			}

            storeAPI.PushMeasurement(JsonConvert.SerializeObject(obj));
		}
	}
}


