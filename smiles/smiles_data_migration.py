import ijson
import json
import decimal
import re
import random
from . import data_catalog_service as dcs
from . import smiles_dp_util
from . import metadata_util

from .smiles_dp_util import SmilesDP
from .proto import computational_dp_pb2 as comp_pb2
from google.protobuf.json_format import ParseDict
from google.protobuf.struct_pb2 import Value
from celery import shared_task


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def migrate_smiles_dps(request_data, filename, dp_id):
    dp_type = SmilesDP(dp_id)
    if dp_type == SmilesDP.COMPUTATIONAL:
        upload_computational_data_products.delay(request_data, filename)
    elif dp_type == SmilesDP.EXPERIMENTAL:
        upload_experimental_data_products.delay(request_data, filename)
    elif dp_type == SmilesDP.LITERATURE:
        upload_literature_data_products.delay(request_data, filename)
    else:
        raise Exception("Undefined SMILES data product type: " + str(dp_type))


def to_snake_case(key):
    special_cases = {"InChI": "inchi", "InChIFile": "inchi_file", "InChIKey": "inchi_key",
                     "Link0Commands": "link_0_commands"}
    if key in special_cases:
        return special_cases[key]
    s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()


def transform_keys(obj):
    if isinstance(obj, dict):
        return {to_snake_case(k): transform_keys(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [transform_keys(v) for v in obj]
    else:
        return obj


@shared_task()
def upload_computational_data_products(request_data, filename):
    with open(filename, 'rb') as input_file:
        jsonobj = ijson.items(input_file, 'item')
        jsons = (o for o in jsonobj)
        count = 0
        failed_count = 0

        for j in jsons:
            try:
                del j["_id"]
                j = transform_keys(j)

                if j.get("calculation")["mo_energies"] is not None:
                    pb_value = Value()
                    str_mo_energies = json.dumps(j.get("calculation")["mo_energies"], cls=DecimalEncoder)
                    ParseDict(str_mo_energies, pb_value)
                    del j.get("calculation")["mo_energies"]

                if j.get("calculated_properties")["dipole"] is not None:
                    dipole = comp_pb2.Dipole()
                    dipole_values = j.get("calculated_properties")["dipole"].split(",")
                    dipole.x = float(dipole_values[0])
                    dipole.y = float(dipole_values[1])
                    dipole.z = float(dipole_values[2])
                    del j.get("calculated_properties")["dipole"]

                computational_dp = ParseDict(j, smiles_dp_util.get_smiles_dp(SmilesDP.COMPUTATIONAL),
                                             ignore_unknown_fields=True)
                if pb_value is not None:
                    computational_dp.calculation.mo_energies.CopyFrom(pb_value)

                if dipole is not None:
                    computational_dp.calculated_properties.dipole.CopyFrom(dipole)

                data_product = smiles_dp_util.map_smiles_dp_to_catalog_dp(request_data, computational_dp,
                                                                          SmilesDP.COMPUTATIONAL)
                catalog_service = dcs.DataCatalogService(request_data)
                result_dp = catalog_service.create_data_product(data_product)
                metadata_util.add_dp_to_schemas(request_data, result_dp)
                count += 1

            except Exception as e:
                failed_count += 1
                continue

        print("Computational DP success count/error count %d/%d" % (count, failed_count))


def transform_experimental_dp(old_json):
    new_json = {
        key: old_json.get(to_snake_case(key), None)
        for key in [
            'name',
            'mol_id',
            'cas_nr',
            'mw',
            'mw_source',
            'mw_monoiso',
            'rdb',
            'validated_by',
            'journal',
            'auth_of_intr',
            'jour_cit',
            'year_publ',
            'doi_link',
            'comp_class',
            'cuniq',
            'calc_perf',
            'org_met',
            'mol_chrg',
            'inter_thngs',
        ]
    }

    # Add the fields that have been moved to new messages

    new_json['structural_data'] = {
        key: old_json.get(to_snake_case(key), None)
        for key in [
            'smiles',
            'smiles_stereo',
            'inchi',
            'molfile_blob_source',
            'emp_formula',
            'emp_formula_sort',
            'emp_formula_source',
        ]
    }

    new_json['spectral_data'] = {
        key: old_json.get(to_snake_case(key), None)
        for key in [
            'state_ofmat',
            'color_white',
            'color_uv',
            'absorb_max',
            'solvent_ae',
            'absorb',
            'conc',
            'extinc',
            'emis_max',
            'temp_abs',
            'emis_qy',
            'temp_ems',
            'lifetime',
        ]
    }

    new_json['electro_chemical'] = {
        key: old_json.get(to_snake_case(key), None)
        for key in [
            'temp_cv',
            'reduc_pot',
            'hw_or_pk_rp',
            'oxid_pot',
            'hw_or_pk_op',
            'solvent_cv',
            'electrolyte',
            'ref_electrd',
        ]
    }

    return new_json


@shared_task()
def upload_experimental_data_products(request_data, filename):
    with open(filename, 'rb') as input_file:
        jsonobj = ijson.items(input_file, 'item')
        jsons = (o for o in jsonobj)
        count = 0
        error_count = 0
        for j in jsons:
            try:
                del j["_id"]
                if j["mol_chrg"] == "":
                    j["mol_chrg"] = None

                j = transform_experimental_dp(j)

                if j.get("year_publ") is not None and j.get("year_publ"):
                    j["year_publ"] = int(j.get("year_publ"))
                else:
                    del j["year_publ"]

                if j.get("calc_perf") is not None and j.get("calc_perf"):
                    j["calc_perf"] = bool(j.get("calc_perf"))
                else:
                    del j["calc_perf"]

                exp_dp = ParseDict(j, smiles_dp_util.get_smiles_dp(SmilesDP.EXPERIMENTAL), ignore_unknown_fields=True)
                data_product = smiles_dp_util.map_smiles_dp_to_catalog_dp(request_data, exp_dp, SmilesDP.EXPERIMENTAL)
                catalog_service = dcs.DataCatalogService(request_data)
                result_dp = catalog_service.create_data_product(data_product)
                metadata_util.add_dp_to_schemas(request_data, result_dp)
                count += 1

            except Exception as e:
                error_count += 1
                continue

        print("Experimental DP success count/error count %d/%d" % (count, error_count))


def transform_literature_dp(old_json):
    # initial keys
    new_json = {'note': None, 'user': None, 'search_keywords': None, 'redox_info': None}

    # biblio key
    if 'biblio' in old_json:
        new_json['biblio'] = {
            'publisher': None,
            **old_json['biblio'],
        }

    # records key
    records_new = []
    for record in old_json.get('records', []):
        record_new = {key: record.get(key, None) for key in ['smiles', 'smiles_validation_failed']}
        record_new['dye_family'] = None
        record_new['structure'] = None
        record_new['other_names'] = record.get('names', [])

        if 'electrochemical_potentials' in record and len(record['electrochemical_potentials']) > 0:
            record_new['electrochemical_potential'] = {
                'value_quoted_ref': record['electrochemical_potentials'][0].get('value', None),
                'cathodic': {
                    'red_v': None,
                    'hw_or_pk': None,
                    'solvent': None,
                    'electrolyte': None,
                },
                'anodic': {
                    'ox_v': None,
                    'hw_or_pk': None,
                    'solvent': None,
                    'electrolyte': None,
                },
            }

        if 'fluorescence_lifetimes' in record and len(record['fluorescence_lifetimes']) > 0:
            record_new['fluorescence_lifetime'] = record['fluorescence_lifetimes'][0]

        if 'uvvis_spectra' in record or 'emisn_spectra' in record:
            record_new['spectral_data'] = {
                'emisn_spectra': record.get('emisn_spectra', [{}])[0],
                'absorp_spectra': record.get('uvvis_spectra', [{}])[0],
            }

        records_new.append(record_new)

    new_json['records'] = records_new

    if records_new and records_new[0].get("other_names") and records_new[0]["other_names"]:
        new_json['name'] = records_new[0]["other_names"][0]
    else:
        new_json['name'] = "Literature DP" + str(random.randint(1, 1000))

    return new_json


def process_peaks(peaks):
    for p in peaks:
        p["extinction"] = int(p.get("extinction")) if p.get("extinction") is not None else None
        p["value"] = float(p.get("value")) if p.get("value") is not None else None
        p["value_validation_failed"] = bool(p.get("value_validation_failed")) if p.get(
            "value_validation_failed") is not None else None
        p["extinction_validation_failed"] = bool(p.get("extinction_validation_failed")) if p.get(
            "extinction_validation_failed") is not None else None


def process_temperature(data):
    if "temperature" in data and data["temperature"] is not None:
        data["temperature"] = 25 if data["temperature"] == "room temperature" else float(
            data["temperature"].replace('–', '-'))


@shared_task()
def upload_literature_data_products(request_data, filename):
    with open(filename, 'rb') as input_file:
        jsonobj = ijson.items(input_file, 'item')
        jsons = (o for o in jsonobj)
        count = 0
        error_count = 0
        for j in jsons:
            try:
                del j["_id"]

                j = transform_literature_dp(j)

                if len(j.get("records")) > 0:
                    for record in j.get("records"):

                        if "smiles_validation_failed" in record and record["smiles_validation_failed"] is not None:
                            record["smiles_validation_failed"] = bool(record.get("smiles_validation_failed"))

                        if record.get("fluorescence_lifetime") is not None:
                            fl = record.get("fluorescence_lifetime")
                            if "temperature" in fl and fl["temperature"] is not None:
                                if fl["temperature"] == "room temperature":
                                    fl["temperature"] = 25
                                else:
                                    fl["temperature"] = float(fl.get("temperature").replace('–', '-'))

                            if "value" in fl and fl["value"] is not None:
                                fl["value"] = float(fl.get("value").replace('–', '-'))

                        spectral_data = record.get("spectral_data")
                        if spectral_data is not None:
                            emisn_spectra = spectral_data.get("emisn_spectra")
                            absorp_spectra = spectral_data.get("absorp_spectra")

                            if emisn_spectra is not None:
                                process_temperature(emisn_spectra)
                                peaks = emisn_spectra.get("peaks") or []
                                process_peaks(peaks)

                            if absorp_spectra is not None:
                                process_temperature(absorp_spectra)
                                peaks = absorp_spectra.get("peaks") or []
                                process_peaks(peaks)

                lit_dp = ParseDict(j, smiles_dp_util.get_smiles_dp(SmilesDP.LITERATURE), ignore_unknown_fields=True)
                data_product = smiles_dp_util.map_smiles_dp_to_catalog_dp(request_data, lit_dp, SmilesDP.LITERATURE)
                catalog_service = dcs.DataCatalogService(request_data)
                result_dp = catalog_service.create_data_product(data_product)
                metadata_util.add_dp_to_schemas(request_data, result_dp)
                count += 1

            except Exception as e:
                error_count += 1
                continue

        print("Literature DP success count/error count %d/%d" % (count, error_count))
