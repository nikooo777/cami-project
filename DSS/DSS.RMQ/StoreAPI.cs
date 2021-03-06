﻿using System;
using System.Net.Http;
using Newtonsoft.Json;

namespace DSS.RMQ
{


	public class ValueInfo
	{
		public int val { get; set; }
	}

	public class JournalEntry
	{
		public string user { get; set; }
		public string severity { get; set; }
		public string timestamp { get; set; }
		public string description { get; set; }
		public string message { get; set; }
        public string reference_id { get; set; }
		public string resource_uri { get; set; }
		public string type { get; set; }
        public bool acknowledged { get; set; }
	}

    public class StoreAPI
    {

        public string url { get; set; }

        public StoreAPI(string baseUrl)
        {
            this.url = baseUrl;
		}

        public void PushMeasurement( string json )
        {
			HttpContent content = new StringContent(json);
            content.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue("application/json");
           
            var response = new HttpClient().PostAsync( url +"/measurement/", content);

			//Console.WriteLine("PUSH MEASUREMNT:" + response.Result);
			Console.WriteLine("Measurement inserted");

		}

        public bool AreLastNHeartRateCritical(int n, int low, int high){

            var urlVS = url + "/measurement/?limit=3&measurement_type=pulse&order_by=-timestamp&user=2&device=2";

            var response = new HttpClient().GetAsync(urlVS);

            if (response.Result.IsSuccessStatusCode)
            {
                dynamic deserialized = JsonConvert.DeserializeObject<dynamic>(response.Result.Content.ReadAsStringAsync().Result);
                var isCritical = true;


                //Console.WriteLine(deserialized);

                if (n  == deserialized["measurements"].Count)
                {


                    for (int i = 0; i < deserialized["measurements"].Count; i++)
                    {
                        var item = deserialized["measurements"][i];

                        var hr =  (int) (item["value_info"]["value"] ?? item["value_info"]["Value"]);

                        Console.WriteLine("HR: " + hr);

                        if ( hr > low && hr < high)
                        {
                            isCritical = false;
						}
                    }

					Console.WriteLine("IS critical: " + isCritical);
				}

                else 
                {
                    throw new Exception("Server response doesn't match requested number of pulse items " + deserialized);
				}
                return isCritical;
            }
            throw new Exception("Something went wrong on the server side while checking for pulse " + response.Result);
         }

        public float GetLatestWeightMeasurement() 
        {

            var response = new HttpClient().GetAsync(url +"/measurement/?limit=1&measurement_type=weight&order_by=-timestamp&user=2");

            if (response.Result.IsSuccessStatusCode)
            {
                dynamic deserialized = JsonConvert.DeserializeObject<dynamic>(response.Result.Content.ReadAsStringAsync().Result);

                return deserialized["measurements"][0]["value_info"]["value"] ?? deserialized["measurements"][0]["value_info"]["Value"] ;
            }

			throw new Exception("Something went wrong on the server side while geting last wight measurement " + response.Result);

        }

        public void PushJournalEntry(string msg, string desc, string type) 
        {

            Console.WriteLine("Timestamp: " +  ((int) (DateTime.UtcNow.Subtract(new DateTime(1970, 1, 1))).TotalSeconds).ToString());


            var obj = new JournalEntry()
            {
				user = "/api/v1/user/2/",
                description = desc,
                message = msg,
                reference_id = null,
                timestamp = ((int)(DateTime.UtcNow.Subtract(new DateTime(1970, 1, 1))).TotalSeconds).ToString(),
                acknowledged = false,
                type = type
            };

            HttpContent content = new StringContent(JsonConvert.SerializeObject(obj));
			content.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue("application/json");
			var response = new HttpClient().PostAsync(url +"/journal_entries/", content);

			//Console.WriteLine("JOURNAL ENTRTY: " + response.Result);
			Console.WriteLine("Journal entry inserted");

		}

    }
}
