using SharpFuzz;
using System;
using NHapi.Base.Parser;
using NHapi.Base;
using System.IO;

namespace nHapi.Fuzz
{
        public class Program
        {
                public static void Main(string[] args)
                {
                        Fuzzer.RunOnce(stream =>
                        {
                                var parser = new PipeParser();
                                StreamReader reader = new StreamReader(stream);
                                string text = reader.ReadToEnd();
                                try
                                {
                                        var hl7Message = parser.Parse(text);
                                }
                                catch (Exception e) { 
                                        Console.WriteLine(e.ToString());
                                }
                        });
                }
        }
}
