﻿using Aas = AasCore.Aas3_0;  // renamed
using FileMode = System.IO.FileMode;
using FileStream = System.IO.FileStream;
using JsonException = System.Text.Json.JsonException;
using Nodes = System.Text.Json.Nodes;

using System.Collections.Generic;  // can't alias
using System.Linq;  // can't alias

namespace AasCore.Aas3_0.Tests
{
    public static class CommonJson
    {
        public static Nodes.JsonNode ReadFromFile(string path)
        {
            using var stream = new FileStream(path, FileMode.Open);
            Nodes.JsonNode? node;
            try
            {
                node = Nodes.JsonNode.Parse(stream);
            }
            catch (JsonException exception)
            {
                throw new System.InvalidOperationException(
                    $"Expected the file to be a valid JSON, but it was not: {path}; " +
                    $"exception was: {exception}"
                );
            }

            if (node is null)
            {
                throw new System.InvalidOperationException(
                    "Expected the file to be a non-null JSON value, " +
                    $"but it was null: {path}"
                );
            }

            return node;
        }

        /// <summary>
        /// Serialize <paremref name="something" /> to a uniform JSON text
        /// such that we can use it for comparisons in the tests.
        /// </summary>
        public static Nodes.JsonNode ToJson(object something)
        {
            switch (something)
            {
                case bool aBool:
                    return Nodes.JsonValue.Create(aBool);
                case long aLong:
                    return Nodes.JsonValue.Create(aLong);
                case double aDouble:
                    return Nodes.JsonValue.Create(aDouble);
                case string aString:
                    return Nodes.JsonValue.Create(aString)
                        ?? throw new System.InvalidOperationException(
                            $"Could not convert {something} " +
                            "to a JSON string");
                case byte[] someBytes:
                    return Nodes.JsonValue.Create(
                        System.Convert.ToBase64String(
                            someBytes))
                        ?? throw new System.InvalidOperationException(
                            $"Could not convert {something} to " +
                            "a base64-encoded JSON string");
                case Aas.IClass instance:
                    return Aas.Jsonization.Serialize.ToJsonObject(instance);
                default:
                    throw new System.ArgumentException(
                        $"The conversion of type {something.GetType()} " +
                        $"to a JSON node has not been defined: {something}");
            }
        }

        /// <summary>
        /// Infer the node kind of the JSON node.
        /// </summary>
        /// <remarks>
        /// This function is necessary since NET6 does not fully support node kinds yet.
        /// See:
        /// <ul>
        /// <li>https://github.com/dotnet/runtime/issues/53406</li>
        /// <li>https://github.com/dotnet/runtime/issues/55827</li>
        /// <li>https://github.com/dotnet/runtime/issues/56592</li>
        /// </ul>
        /// </remarks>
        private static string GetNodeKind(Nodes.JsonNode node)
        {
            switch (node)
            {
                case Nodes.JsonArray _:
                    return "array";
                case Nodes.JsonObject _:
                    return "object";
                case Nodes.JsonValue _:
                    return "value";
                default:
                    throw new System.InvalidOperationException(
                        $"Unhandled JsonNode: {node.GetType()}");
            }
        }

        public static void CheckJsonNodesEqual(
            Nodes.JsonNode that,
            Nodes.JsonNode other,
            out Reporting.Error? error)
        {
            error = null;

            var thatNodeKind = GetNodeKind(that);
            var otherNodeKind = GetNodeKind(other);

            if (thatNodeKind != otherNodeKind)
            {
                error = new Reporting.Error(
                    $"Mismatch in node kinds : {thatNodeKind} != {otherNodeKind}"
                );
                return;
            }

            switch (that)
            {
                case Nodes.JsonArray thatArray:
                    {
                        var otherArray = (other as Nodes.JsonArray)!;
                        if (thatArray.Count != otherArray.Count)
                        {
                            error = new Reporting.Error(
                                $"Unequal array lengths: {thatArray.Count} != {otherArray.Count}"
                            );
                            return;
                        }

                        for (int i = 0; i < thatArray.Count; i++)
                        {
                            CheckJsonNodesEqual(thatArray[i]!, otherArray[i]!, out error);
                            if (error != null)
                            {
                                error.PrependSegment(new Reporting.IndexSegment(i));
                                return;
                            }
                        }

                        break;
                    }
                case Nodes.JsonObject thatObject:
                    {
                        var thatDictionary = thatObject as IDictionary<string, Nodes.JsonNode>;
                        var otherDictionary = (other as IDictionary<string, Nodes.JsonNode>)!;

                        var thatKeys = thatDictionary.Keys.ToList();
                        thatKeys.Sort();

                        var otherKeys = otherDictionary.Keys.ToList();
                        otherKeys.Sort();

                        if (!thatKeys.SequenceEqual(otherKeys))
                        {
                            error = new Reporting.Error(
                                "Objects with different properties: " +
                                $"{string.Join(", ", thatKeys)} != " +
                                $"{string.Join(", ", otherKeys)}"
                            );
                            return;
                        }

                        foreach (var key in thatKeys)
                        {
                            CheckJsonNodesEqual(thatDictionary[key], otherDictionary[key], out error);
                            if (error != null)
                            {
                                error.PrependSegment(new Reporting.NameSegment(key));
                                return;
                            }
                        }

                        break;
                    }
                case Nodes.JsonValue thatValue:
                    {
                        string thatAsJsonString = thatValue.ToJsonString();

                        // NOTE (mristin, 2023-03-16):
                        // This is slow, but there is no way around it at the moment with NET6.
                        // See:
                        // * https://github.com/dotnet/runtime/issues/56592
                        // * https://github.com/dotnet/runtime/issues/55827
                        // * https://github.com/dotnet/runtime/issues/53406
                        var otherValue = (other as Nodes.JsonValue)!;
                        string otherAsJsonString = otherValue.ToJsonString();

                        if (thatAsJsonString != otherAsJsonString)
                        {
                            error = new Reporting.Error(
                                $"Unequal values: {thatAsJsonString} != {otherAsJsonString}"
                            );
                            // ReSharper disable once RedundantJumpStatement
                            return;
                        }

                        break;
                    }
                default:
                    throw new System.InvalidOperationException(
                        $"Unhandled JSON node: {that.GetType()}"
                    );
            }
        }

        /// <summary>
        /// Load an instance from a JSON file.
        /// </summary>
        public static Aas.IClass LoadInstance(
            string path)
        {
            Aas.IClass? instance;

            {
                using var stream = new FileStream(path, FileMode.Open);
                var node = Nodes.JsonNode.Parse(stream)
                           ?? throw new System.InvalidOperationException(
                               "node unexpectedly null");

                instance = AasCore.Aas3_0.Jsonization.Deserialize.EnvironmentFrom(
                    node);
            }

            if (instance == null)
            {
                throw new System.InvalidOperationException(
                    "environment unexpectedly null");
            }

            return instance;
        }
    }
}