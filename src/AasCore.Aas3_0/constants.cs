/*
 * This code has been automatically generated by aas-core-codegen.
 * Do NOT edit or append.
 */

using System.Collections.Generic;  // can't alias

namespace AasCore.Aas3_0
{
    /// <summary>
    /// Provide constant values of the meta-model.
    /// </summary>
    public static class Constants
    {
        public static readonly HashSet<string> ValidCategoriesForDataElement = (
            new HashSet<string>()
            {
                "CONSTANT",
                "PARAMETER",
                "VARIABLE"
            });

        public static readonly HashSet<KeyTypes?> GenericFragmentKeys = (
            new HashSet<KeyTypes?>()
            {
                KeyTypes.FragmentReference
            });

        public static readonly HashSet<KeyTypes?> GenericGloballyIdentifiables = (
            new HashSet<KeyTypes?>()
            {
                KeyTypes.GlobalReference
            });

        public static readonly HashSet<KeyTypes?> AasIdentifiables = (
            new HashSet<KeyTypes?>()
            {
                KeyTypes.AssetAdministrationShell,
                KeyTypes.ConceptDescription,
                KeyTypes.Identifiable,
                KeyTypes.Submodel
            });

        public static readonly HashSet<KeyTypes?> AasSubmodelElementsAsKeys = (
            new HashSet<KeyTypes?>()
            {
                KeyTypes.AnnotatedRelationshipElement,
                KeyTypes.BasicEventElement,
                KeyTypes.Blob,
                KeyTypes.Capability,
                KeyTypes.DataElement,
                KeyTypes.Entity,
                KeyTypes.EventElement,
                KeyTypes.File,
                KeyTypes.MultiLanguageProperty,
                KeyTypes.Operation,
                KeyTypes.Property,
                KeyTypes.Range,
                KeyTypes.ReferenceElement,
                KeyTypes.RelationshipElement,
                KeyTypes.SubmodelElement,
                KeyTypes.SubmodelElementCollection,
                KeyTypes.SubmodelElementList
            });

        public static readonly HashSet<KeyTypes?> AasReferableNonIdentifiables = (
            new HashSet<KeyTypes?>()
            {
                KeyTypes.AnnotatedRelationshipElement,
                KeyTypes.BasicEventElement,
                KeyTypes.Blob,
                KeyTypes.Capability,
                KeyTypes.DataElement,
                KeyTypes.Entity,
                KeyTypes.EventElement,
                KeyTypes.File,
                KeyTypes.MultiLanguageProperty,
                KeyTypes.Operation,
                KeyTypes.Property,
                KeyTypes.Range,
                KeyTypes.ReferenceElement,
                KeyTypes.RelationshipElement,
                KeyTypes.SubmodelElement,
                KeyTypes.SubmodelElementCollection,
                KeyTypes.SubmodelElementList
            });

        public static readonly HashSet<KeyTypes?> AasReferables = (
            new HashSet<KeyTypes?>()
            {
                KeyTypes.AssetAdministrationShell,
                KeyTypes.ConceptDescription,
                KeyTypes.Identifiable,
                KeyTypes.Submodel,
                KeyTypes.AnnotatedRelationshipElement,
                KeyTypes.BasicEventElement,
                KeyTypes.Blob,
                KeyTypes.Capability,
                KeyTypes.DataElement,
                KeyTypes.Entity,
                KeyTypes.EventElement,
                KeyTypes.File,
                KeyTypes.MultiLanguageProperty,
                KeyTypes.Operation,
                KeyTypes.Property,
                KeyTypes.Range,
                KeyTypes.ReferenceElement,
                KeyTypes.Referable,
                KeyTypes.RelationshipElement,
                KeyTypes.SubmodelElement,
                KeyTypes.SubmodelElementCollection,
                KeyTypes.SubmodelElementList
            });

        public static readonly HashSet<KeyTypes?> GloballyIdentifiables = (
            new HashSet<KeyTypes?>()
            {
                KeyTypes.GlobalReference,
                KeyTypes.AssetAdministrationShell,
                KeyTypes.ConceptDescription,
                KeyTypes.Identifiable,
                KeyTypes.Submodel
            });

        public static readonly HashSet<KeyTypes?> FragmentKeys = (
            new HashSet<KeyTypes?>()
            {
                KeyTypes.FragmentReference,
                KeyTypes.AnnotatedRelationshipElement,
                KeyTypes.BasicEventElement,
                KeyTypes.Blob,
                KeyTypes.Capability,
                KeyTypes.DataElement,
                KeyTypes.Entity,
                KeyTypes.EventElement,
                KeyTypes.File,
                KeyTypes.MultiLanguageProperty,
                KeyTypes.Operation,
                KeyTypes.Property,
                KeyTypes.Range,
                KeyTypes.ReferenceElement,
                KeyTypes.RelationshipElement,
                KeyTypes.SubmodelElement,
                KeyTypes.SubmodelElementCollection,
                KeyTypes.SubmodelElementList
            });

        public static readonly HashSet<DataTypeIec61360?> DataTypeIec61360ForPropertyOrValue = (
            new HashSet<DataTypeIec61360?>()
            {
                DataTypeIec61360.Date,
                DataTypeIec61360.String,
                DataTypeIec61360.StringTranslatable,
                DataTypeIec61360.IntegerMeasure,
                DataTypeIec61360.IntegerCount,
                DataTypeIec61360.IntegerCurrency,
                DataTypeIec61360.RealMeasure,
                DataTypeIec61360.RealCount,
                DataTypeIec61360.RealCurrency,
                DataTypeIec61360.Boolean,
                DataTypeIec61360.Rational,
                DataTypeIec61360.RationalMeasure,
                DataTypeIec61360.Time,
                DataTypeIec61360.Timestamp
            });

        public static readonly HashSet<DataTypeIec61360?> DataTypeIec61360ForReference = (
            new HashSet<DataTypeIec61360?>()
            {
                DataTypeIec61360.String,
                DataTypeIec61360.Iri,
                DataTypeIec61360.Irdi
            });

        public static readonly HashSet<DataTypeIec61360?> DataTypeIec61360ForDocument = (
            new HashSet<DataTypeIec61360?>()
            {
                DataTypeIec61360.File,
                DataTypeIec61360.Blob,
                DataTypeIec61360.Html
            });

        public static readonly HashSet<DataTypeIec61360?> Iec61360DataTypesWithUnit = (
            new HashSet<DataTypeIec61360?>()
            {
                DataTypeIec61360.IntegerMeasure,
                DataTypeIec61360.RealMeasure,
                DataTypeIec61360.RationalMeasure,
                DataTypeIec61360.IntegerCurrency,
                DataTypeIec61360.RealCurrency
            });
    }  // public static class Constants
}  // namespace AasCore.Aas3_0

/*
 * This code has been automatically generated by aas-core-codegen.
 * Do NOT edit or append.
 */
