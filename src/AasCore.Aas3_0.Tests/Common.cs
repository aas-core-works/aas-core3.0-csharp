﻿using Aas = AasCore.Aas3_0; // renamed

using System.Collections.Generic; // can't alias
using System.Linq; // can't alias
using NUnit.Framework; // can't alias

namespace AasCore.Aas3_0.Tests
{
    /// <summary>
    /// Provide common functionality to be re-used across different tests
    /// such as reading of environment variables.
    /// </summary>
    public static class Common
    {
        // NOTE (mristin, 2023-03-16):
        // It is tedious to record manually all the expected error messages. Therefore we include this variable
        // to steer the automatic recording. We intentionally inter-twine the recording code with the test code
        // to keep them close to each other so that they are easier to maintain.
        public static readonly bool RecordMode = (
            System.Environment.GetEnvironmentVariable("AAS_CORE_AAS3_0_TESTS_RECORD_MODE")?.ToLower() == "true"
        );

        public static readonly string TestDataDir = (
            System.Environment.GetEnvironmentVariable(
            "AAS_CORE_AAS3_0_TESTS_TEST_DATA_DIR")
            ?? throw new System.InvalidOperationException(
                "The path to the test data directory is missing in the environment: " +
                "AAS_CORE_AAS3_0_TESTS_TEST_DATA_DIR")
        );

        /// <summary>
        /// Find the first instance of <typeparamref name="T"/> in the <paramref name="container" />,
        /// including the <paramref name="container" /> itself.
        /// </summary>
        public static T MustFind<T>(Aas.IClass container) where T : Aas.IClass
        {
            var instance = (
                (container is T)
                    ? container
                    : container
                          .Descend()
                          .First(something => something is T)
                      ?? throw new System.InvalidOperationException(
                          $"No instance of {nameof(T)} could be found")
            );

            return (T)instance;
        }

        public static void AssertNoVerificationErrors(List<Aas.Reporting.Error> errors, string path)
        {
            if (errors.Count > 0)
            {
                var builder = new System.Text.StringBuilder();
                builder.Append(
                    $"Expected no errors when verifying the instance de-serialized from {path}, " +
                    $"but got {errors.Count} error(s):\n");
                for (var i = 0; i < errors.Count; i++)
                {
                    builder.Append(
                        $"Error {i + 1}:\n" +
                        $"{Reporting.GenerateJsonPath(errors[i].PathSegments)}: {errors[i].Cause}\n");
                }

                Assert.Fail(builder.ToString());
            }
        }

        public static readonly List<string> CausesForVerificationFailure = (
            new List<string>()
            {
                "DateTimeStampUtcViolationOnFebruary29th",
                "MaxLengthViolation",
                "MinLengthViolation",
                "PatternViolation",
                "InvalidValueExample",
                "InvalidMinMaxExample",
                "SetViolation",
                "ConstraintViolation"
            });

        public static void AssertEqualsExpectedOrRerecordVerificationErrors(
            List<Aas.Reporting.Error> errors, string path)
        {
            if (errors.Count == 0)
            {
                Assert.Fail(
                    $"Expected at least one verification error when verifying {path}, but got none");
            }

            string got = string.Join(
                ";\n",
                errors.Select(
                    error => $"{Reporting.GenerateJsonPath(error.PathSegments)}: {error.Cause}"));

            string errorsPath = path + ".errors";
            if (RecordMode)
            {
                System.IO.File.WriteAllText(errorsPath, got);
            }
            else
            {
                if (!System.IO.File.Exists(errorsPath))
                {
                    throw new System.IO.FileNotFoundException(
                        $"The file with the recorded errors does not exist: {errorsPath}");
                }

                string expected = System.IO.File.ReadAllText(errorsPath);
                Assert.AreEqual(
                    expected.Replace("\r\n", "\n"),
                    got.Replace("\r\n", "\n"),
                    $"The expected verification errors do not match the actual ones for the file {path}");
            }
        }
    }
}