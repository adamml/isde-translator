class _XPathQueries():
    """
    XPath queries to build a Dataset from an ISO19115/19139 record
    """
    dataset_title: str = (
            ".//{http://www.isotc211.org/2005/gmd}identificationInfo/" +
            "{http://www.isotc211.org/2005/gmd}MD_DataIdentification/" +
            "{http://www.isotc211.org/2005/gmd}citation/" +
            "{http://www.isotc211.org/2005/gmd}CI_Citation/" +
            "{http://www.isotc211.org/2005/gmd}title/" +
            "{http://www.isotc211.org/2005/gco}CharacterString")
    """Xpath query for the title of a isde_dataset"""

    dataset_abstract: str = (
            ".//{http://www.isotc211.org/2005/gmd}identificationInfo/" +
            "{http://www.isotc211.org/2005/gmd}MD_DataIdentification/" +
            "{http://www.isotc211.org/2005/gmd}abstract/" +
            "{http://www.isotc211.org/2005/gco}CharacterString")
    """Xpath query for the abstract of a isde_dataset"""

    dataset_file_identifier: str = (
            ".//{http://www.isotc211.org/2005/gmd}fileIdentifier/" +
            "{http://www.isotc211.org/2005/gco}CharacterString")
    """Xpath query for the file identifier of a isde_dataset"""

    dataset_bounding_north: str = (
            ".//{http://www.isotc211.org/2005/gmd}identificationInfo/" +
            "{http://www.isotc211.org/2005/gmd}MD_DataIdentification/" +
            "{http://www.isotc211.org/2005/gmd}extent/" +
            "{http://www.isotc211.org/2005/gmd}EX_Extent/" +
            "{http://www.isotc211.org/2005/gmd}geographicElement/" +
            "{http://www.isotc211.org/2005/gmd}EX_GeographicBoundingBox/" +
            "{http://www.isotc211.org/2005/gmd}northBoundLatitude/" +
            "{http://www.isotc211.org/2005/gco}Decimal")

    dataset_bounding_south: str = (
            ".//{http://www.isotc211.org/2005/gmd}identificationInfo/" +
            "{http://www.isotc211.org/2005/gmd}MD_DataIdentification/" +
            "{http://www.isotc211.org/2005/gmd}extent/" +
            "{http://www.isotc211.org/2005/gmd}EX_Extent/" +
            "{http://www.isotc211.org/2005/gmd}geographicElement/" +
            "{http://www.isotc211.org/2005/gmd}EX_GeographicBoundingBox/" +
            "{http://www.isotc211.org/2005/gmd}southBoundLatitude/" +
            "{http://www.isotc211.org/2005/gco}Decimal")

    dataset_bounding_east: str = (
            ".//{http://www.isotc211.org/2005/gmd}identificationInfo/" +
            "{http://www.isotc211.org/2005/gmd}MD_DataIdentification/" +
            "{http://www.isotc211.org/2005/gmd}extent/" +
            "{http://www.isotc211.org/2005/gmd}EX_Extent/" +
            "{http://www.isotc211.org/2005/gmd}geographicElement/" +
            "{http://www.isotc211.org/2005/gmd}EX_GeographicBoundingBox/" +
            "{http://www.isotc211.org/2005/gmd}eastBoundLongitude/" +
            "{http://www.isotc211.org/2005/gco}Decimal")

    dataset_bounding_west: str = (
            ".//{http://www.isotc211.org/2005/gmd}identificationInfo/" +
            "{http://www.isotc211.org/2005/gmd}MD_DataIdentification/" +
            "{http://www.isotc211.org/2005/gmd}extent/" +
            "{http://www.isotc211.org/2005/gmd}EX_Extent/" +
            "{http://www.isotc211.org/2005/gmd}geographicElement/" +
            "{http://www.isotc211.org/2005/gmd}EX_GeographicBoundingBox/" +
            "{http://www.isotc211.org/2005/gmd}westBoundLongitude/" +
            "{http://www.isotc211.org/2005/gco}Decimal")

    dataset_themes: str = (
            ".//{http://www.isotc211.org/2005/gmd}identificationInfo/" +
            "{http://www.isotc211.org/2005/gmd}MD_DataIdentification/" +
            "{http://www.isotc211.org/2005/gmd}topicCategory/" +
            "{http://www.isotc211.org/2005/gmd}MD_TopicCategoryCode")

    dataset_uri: str = (
            ".//{http://www.isotc211.org/2005/gmd}dataSetURI/" +
            "{http://www.isotc211.org/2005/gco}CharacterString")

    dataset_citation: str = (
            ".//{http://www.isotc211.org/2005/gmd}identificationInfo/" +
            "{http://www.isotc211.org/2005/gmd}MD_DataIdentification/" +
            "{http://www.isotc211.org/2005/gmd}citation/" +
            "{http://www.isotc211.org/2005/gmd}CI_Citation/" +
            "{http://www.isotc211.org/2005/gmd}otherCitationDetails/" +
            "{http://www.isotc211.org/2005/gco}CharacterString")
