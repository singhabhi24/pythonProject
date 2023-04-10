from typing import List
import json
from collections import namedtuple
from json import JSONEncoder

class Area:
    tacs: List[str]

    def __init__(self, tacs: List[str]) -> None:
        self.tacs = tacs

    def get_tacs(self):
        return self.tacs

    def set_tacs(self, tacs: List[str]):
        self.tacs = tacs


class SingleNssai:
    sd: str
    sst: int

    def __init__(self, sd: str, sst: int) -> None:
        self.sd = sd
        self.sst = sst


class Nssai:
    default_single_nssais: List[SingleNssai]
    single_nssais: List[SingleNssai]

    def __init__(self, default_single_nssais: List[SingleNssai], single_nssais: List[SingleNssai]) -> None:
        self.default_single_nssais = default_single_nssais
        self.single_nssais = single_nssais


class The00101:
    rfsp_index: int

    def __init__(self, rfsp_index: int) -> None:
        self.rfsp_index = rfsp_index


class PlmnAmData:
    the_00101: The00101

    def __init__(self, the_00101: The00101) -> None:
        self.the_00101 = the_00101


class ServiceAreaRestriction:
    restriction_type: str
    areas: List[Area]
    max_num_of_t_as: int

    def __init__(self, restriction_type: str, areas: List[Area], max_num_of_t_as: int) -> None:
        self.restriction_type = restriction_type
        self.areas = areas
        self.max_num_of_t_as = max_num_of_t_as


class SubscribedUeAmbr:
    downlink: str
    uplink: str

    def __init__(self, downlink: str, uplink: str) -> None:
        self.downlink = downlink
        self.uplink = uplink


class Am1JSON:
    gpsis: List[str]
    internal_group_ids: List[str]
    nssai: Nssai
    subscribed_ue_ambr: SubscribedUeAmbr
    subscribed_dnn_list: List[str]
    forbidden_areas: List[Area]
    service_area_restriction: ServiceAreaRestriction
    plmn_am_data: PlmnAmData
    rfsp_index: int
    subs_reg_timer: int
    ue_usage_type: int
    mico_allowed: bool

    # def __init__(self, gpsis: List[str], internal_group_ids: List[str], nssai: Nssai,
    #              subscribed_ue_ambr: SubscribedUeAmbr, subscribed_dnn_list: List[str], forbidden_areas: List[Area],
    #              service_area_restriction: ServiceAreaRestriction, plmn_am_data: PlmnAmData, rfsp_index: int,
    #              subs_reg_timer: int, ue_usage_type: int, mico_allowed: bool) -> None:
    #     self.gpsis = gpsis
    #     self.internal_group_ids = internal_group_ids
    #     self.nssai = nssai
    #     self.subscribed_ue_ambr = subscribed_ue_ambr
    #     self.subscribed_dnn_list = subscribed_dnn_list
    #     self.forbidden_areas = forbidden_areas
    #     self.service_area_restriction = service_area_restriction
    #     self.plmn_am_data = plmn_am_data
    #     self.rfsp_index = rfsp_index
    #     self.subs_reg_timer = subs_reg_timer
    #     self.ue_usage_type = ue_usage_type
    #     self.mico_allowed = mico_allowed

    def get_gpsis(self):
        return self.gpsis

    def set_gpsis(self, gpsis: List[str]):
        self.gpsis = gpsis


class StudentEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def customStudentDecoder(studentDict):
    return namedtuple('X', studentDict.keys())(*studentDict.values())


class Am1Json:
    am1_json: Am1JSON

    def __init__(self, am1_json: Am1JSON) -> None:
        self.am1_json = am1_json
