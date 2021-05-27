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
                        Fuzzer.OutOfProcess.Run(stream =>
                        {
                                var parser = new PipeParser();
                                StreamReader reader = new StreamReader(stream);
                                string text = reader.ReadToEnd();
                                try
                                {
                                        var hl7Message = parser.Parse(text);
                                }
                                // HL7 Exceptions
                                catch (EncodingNotSupportedException e) { Console.WriteLine(e.ToString()); }
                                catch (DataTypeException e) { Console.WriteLine(e.ToString()); }
                                catch (HL7Exception e) { Console.WriteLine(e.ToString()); }
                        });
                }
        }
}
