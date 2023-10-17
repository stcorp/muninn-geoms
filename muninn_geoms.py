import os
import logging
from datetime import datetime

from muninn.exceptions import Error
from muninn.struct import Struct
from muninn.schema import Mapping, optional, Text, Timestamp


# Muninn 'geoms' namespace

class GEOMSNamespace(Mapping):
    pi_name = Text
    pi_affiliation = Text
    pi_address = Text
    pi_email = Text

    do_name = Text
    do_affiliation = Text
    do_address = Text
    do_email = Text

    ds_name = Text
    ds_affiliation = Text
    ds_address = Text
    ds_email = Text

    data_description = optional(Text)
    data_discipline = Text
    data_group = Text
    data_location = Text
    data_source = Text
    data_variables = Text
    data_start_date = Timestamp
    data_stop_date = Timestamp
    data_file_version = Text
    data_modifications = optional(Text)
    data_caveats = optional(Text)
    data_rules_of_use = optional(Text)
    data_acknowledgement = optional(Text)
    data_quality = optional(Text)
    data_template = optional(Text)
    data_processor = optional(Text)

    file_name = Text
    file_generation_date = Timestamp
    file_access = Text
    file_project_id = optional(Text)
    file_association = optional(Text)
    file_meta_version = Text
    file_doi = Text


def namespaces():
    return ['geoms']


def namespace(name):
    return GEOMSNamespace


# Support functions for geoms product types

FILE_NAME_PATTERN = r"(?P<data_discipline_03>[a-z0-9.]+)_(?P<data_source>[a-z0-9.]+)_" \
    r"(?P<affiliation>[a-z0-9.]+)(?P<identifier>[\d]{3})(_(?P<processing_version>[a-z0-9.]+))?_" \
    r"(?P<data_location>[a-z0-9.]+)_(?P<data_start_date>[\dt]{15}z)_(?P<data_stop_date>[\dt]{15}z)_" \
    r"(?P<data_file_version>\d{3})\.(hdf|h5|nc)$"

DATETIME_FORMAT = "%Y%m%dT%H%M%SZ"


def extract_geoms_metadata(path):
    # Retrieve geoms metadata from a product file
    global_attrs = {}
    try:
        import coda
        with coda.open(path) as product:
            for k, v in vars(coda.get_attributes(product)).items():
                if k[0] != '_':
                    global_attrs[k] = v.strip('\0')
    except Exception as e:
        logging.getLogger(__name__).exception(e)
        raise Error(str(e))

    geoms = Struct()

    geoms.pi_name = global_attrs['PI_NAME']
    geoms.pi_affiliation = global_attrs['PI_AFFILIATION']
    geoms.pi_address = global_attrs['PI_ADDRESS']
    geoms.pi_email = global_attrs['PI_EMAIL']

    geoms.do_name = global_attrs['DO_NAME']
    geoms.do_affiliation = global_attrs['DO_AFFILIATION']
    geoms.do_address = global_attrs['DO_ADDRESS']
    geoms.do_email = global_attrs['DO_EMAIL']

    geoms.ds_name = global_attrs['DS_NAME']
    geoms.ds_affiliation = global_attrs['DS_AFFILIATION']
    geoms.ds_address = global_attrs['DS_ADDRESS']
    geoms.ds_email = global_attrs['DS_EMAIL']

    if 'DATA_DESCRIPTION' in global_attrs:
        geoms.data_description = global_attrs['DATA_DESCRIPTION']
    geoms.data_discipline = global_attrs['DATA_DISCIPLINE']
    geoms.data_group = global_attrs['DATA_GROUP']
    geoms.data_location = global_attrs['DATA_LOCATION']
    geoms.data_source = global_attrs['DATA_SOURCE']
    geoms.data_variables = global_attrs['DATA_VARIABLES']
    geoms.data_start_date = datetime.strptime(global_attrs['DATA_START_DATE'], DATETIME_FORMAT)
    geoms.data_stop_date = datetime.strptime(global_attrs['DATA_STOP_DATE'], DATETIME_FORMAT)
    geoms.data_file_version = global_attrs['DATA_FILE_VERSION']
    if 'DATA_MODIFICATIONS' in global_attrs:
        geoms.data_modifications = global_attrs['DATA_MODIFICATIONS']
    if 'DATA_CAVEATS' in global_attrs:
        geoms.data_caveats = global_attrs['DATA_CAVEATS']
    if 'DATA_RULES_OF_USE' in global_attrs:
        geoms.data_rules_of_use = global_attrs['DATA_RULES_OF_USE']
    if 'DATA_ACKNOWLEDGEMENT' in global_attrs:
        geoms.data_acknowledgement = global_attrs['DATA_ACKNOWLEDGEMENT']
    if 'DATA_QUALITY' in global_attrs:
        geoms.data_quality = global_attrs['DATA_QUALITY']
    if 'DATA_TEMPLATE' in global_attrs:
        geoms.data_template = global_attrs['DATA_TEMPLATE']
    if 'DATA_PROCESSOR' in global_attrs:
        geoms.data_processor = global_attrs['DATA_PROCESSOR']

    geoms.file_name = global_attrs['FILE_NAME']
    geoms.file_generation_date = datetime.strptime(global_attrs['FILE_GENERATION_DATE'], DATETIME_FORMAT)
    geoms.file_access = global_attrs['FILE_ACCESS']
    if 'FILE_PROJECT_ID' in global_attrs:
        geoms.file_project_id = global_attrs['FILE_PROJECT_ID']
    if 'FILE_ASSOCIATION' in global_attrs:
        geoms.file_association = global_attrs['FILE_ASSOCIATION']
    geoms.file_meta_version = global_attrs['FILE_META_VERSION']
    geoms.file_doi = global_attrs['FILE_DOI']

    return geoms
