#!/usr/bin/env python3

import argparse

from google.protobuf import struct_pb2
from lte.protos.pmn_systems_pb2 import PMNSubscriberData
from lte.protos.models.any_type_pb2 import AnyType
from lte.protos.models.access_and_mobility_subscription_data_pb2 import AccessAndMobilitySubscriptionData
from lte.protos.models.authentication_subscription_pb2 import AuthenticationSubscription
from lte.protos.pmn_systems_pb2_grpc import PMNSubscriberConfigServicerStub
from lte.protos.models.snssai_pb2 import Snssai
from lte.protos.models.nssai_pb2 import Nssai
from lte.protos.models.ambr_rm_pb2 import AmbrRm
from lte.protos.models.sequence_number_pb2 import SequenceNumber
from lte.protos.models.sign_pb2 import Sign
from lte.protos.models.smf_selection_subscription_data_pb2 import SmfSelectionSubscriptionData
from lte.protos.models.sms_management_subscription_data_pb2 import SmsManagementSubscriptionData
from lte.protos.models.ue_policy_set_pb2 import UePolicySet
from lte.protos.models.sms_subscription_data_pb2 import SmsSubscriptionData
from lte.protos.models.am_policy_data_pb2 import AmPolicyData
from lte.protos.models.session_management_subscription_data_pb2 import SessionManagementSubscriptionData
from lte.protos.models.smf_selection_subscription_data_pb2 import SmfSelectionSubscriptionData
from lte.protos.models.sm_policy_snssai_data_pb2 import SmPolicySnssaiData
from lte.protos.models.plmn_id_pb2 import PlmnId

def assemble_am1(args) -> AccessAndMobilitySubscriptionData:

    plmnAmData = struct_pb2.Struct()
    plmnAmData["{}-{}".format(args.mcc, args.mnc)]={}

    return AccessAndMobilitySubscriptionData(
              nssai=Nssai(defaultSingleNssais=[Snssai(sst=args.st, sd=args.sd)],
                          singleNssais=[Snssai(sst=args.st, sd=args.sd)]),
              subscribedUeAmbr=AmbrRm(uplink=args.subs_ambr_ul,
                                      downlink=args.subs_ambr_dl),
              subscribedDnnList=[args.dnn_name],
              plmnAmData=plmnAmData)

def assemble_plmnSmfSelData(plmnSmfSelData):
    #protos don't match the models replace AccessAndMobilitySubscriptionDataSubscribedDnnListInner
    # with DnnRouteSelectionDescriptor
    arrayEntry=plmnSmfSelData.subscribedSnssaiInfos["1-000001"].dnnInfos.add()
    arrayEntry.iwkEpsInd = True

def assemble_smPolicySnssaiData(smPolicySnssaiData):
    snssai=Snssai(sst=1,sd="000001")
    smPolicySnssaiData.snssai.MergeFrom(snssai)
    mapEntry = smPolicySnssaiData.smPolicyDnnData["apn1.mnc001.mcc001.gprs"]
    mapEntry.dnn="apn1.mnc001.mcc001.gprs"
    mapEntry.allowedServices.MergeFrom(["A","B"])
    mapEntry.subscCats.MergeFrom(["Brass"])
    mapEntry.gbrUl="200kbps"
    mapEntry.gbrDl="100kbps"
    mapEntry.ipv4Index=2
    mapEntry.ipv6Index=3
    mapEntry.offline=False
    mapEntry.online=True

def assemble_smsdata(smsdata):
    snssai=Snssai(sst=1,sd="000001")
    smsdata.singleNssai.MergeFrom(snssai)
    mapEntry = smsdata.dnnConfigurations["apn1"]
    mapEntry.pduSessionTypes.defaultSessionType.pduSessTypes="IPV4"
    arrayEntry = mapEntry.pduSessionTypes.allowedSessionTypes.add()
    arrayEntry.pduSessTypes="IPV4V6"
    mapEntry.internal_5gQosProfile.internal_5qi=9
    mapEntry.internal_5gQosProfile.arp.priorityLevel=7
    #dum.internal_5gQosProfile.arp.preemptCap= Empty in protos
    #dum.internal_5gQosProfile.arp.preemptVuln= Empty in protos
    mapEntry.sessionAmbr.uplink="1000 Mbps"
    mapEntry.sessionAmbr.downlink="2000 Mbps"
    mapEntry.sscModes.defaultSscMode.sscModes="SSC_MODE_1"
    arrayEntry = mapEntry.sscModes.allowedSscModes.add()
    arrayEntry.sscModes="SSC_MODE_1"
    arrayEntry = mapEntry.sscModes.allowedSscModes.add()
    arrayEntry.sscModes="SSC_MODE_2"
    arrayEntry = mapEntry.sscModes.allowedSscModes.add()
    arrayEntry.sscModes="SSC_MODE_3"

def assemble_am_policy_data(am_policy_data):
    plmnId = PlmnId(mcc="001",mnc="01")

    am_policy_data.subscCats.MergeFrom([
      "Brass",
      "sit",
      "bronze"
    ])

    mapEntry = am_policy_data.praInfos["ad_3"]
    mapEntry.praId = "yyrueiii"
    arrayEntry = mapEntry.ecgiList.add()
    arrayEntry.plmnId.CopyFrom(plmnId)
    arrayEntry.eutraCellId = "C2e48fF"
    arrayEntry = mapEntry.ncgiList.add()
    arrayEntry.plmnId.CopyFrom(plmnId)
    arrayEntry.nrCellId = "E70D48fE7"
    arrayEntry = mapEntry.trackingAreaList.add()
    arrayEntry.plmnId.CopyFrom(plmnId)
    arrayEntry.tac="EAdd"

def assemble_ue_policy_data(ue_policy_data):
    plmnId = PlmnId(mcc="001",mnc="01")
    snssai=Snssai(sst=1,sd="000001")
    ue_policy_data.subscCats.MergeFrom(["Categorieslist"])
    ue_policy_data.upsis.MergeFrom(["UpsiInfo1"])
    mapEntry = ue_policy_data.uePolicySections["ade"]
    mapEntry.uePolicySectionInfo = bytes("C0RF",'utf-8')
    mapEntry.upsi = "UPSI-Data"
    mapEntry = ue_policy_data.allowedRouteSelDescs["deserunt38"]
    mapEntry.servingPlmn.CopyFrom(plmnId)
    arrayEntry = mapEntry.snssaiRouteSelDescs.add()
    arrayEntry.snssai.CopyFrom(snssai)
    subArrayEntry = arrayEntry.dnnRouteSelDescs.add()
    subArrayEntry.dnn = "apn1.mnc001.mcc001.gprs"
    arrayEntry = subArrayEntry.sscModes.add()
    arrayEntry.sscModes = "SSC_MODE_1"
    arrayEntry = subArrayEntry.pduSessTypes.add()
    arrayEntry.pduSessTypes="IPV4"
    arrayEntry = subArrayEntry.pduSessTypes.add()
    arrayEntry.pduSessTypes="IPV4V6"

def assemble_sms_data(sms_data):
    sms_data.smsSubscribed=True

def assemble_sms_mng_data(sms_mng_data):
    # sms_mng_data.supportedFeatures =
    sms_mng_data.mtSmsSubscribed=True
    sms_mng_data.mtSmsBarringAll=True
    sms_mng_data.mtSmsBarringRoaming=True
    # sms_mng_data.moSmsSubscribed =
    # sms_mng_data.moSmsBarringAll =
    sms_mng_data.moSmsBarringRoaming=True

def assemble_auth_subs_data(auth_subs_data, args):
    auth_subs_data.KTAB="AUTHSUBS"
    #authsubsData.authenticationMethod=AuthMethod()
    auth_subs_data.algorithmId="MILENAGE.1"
    auth_subs_data.authenticationManagementField="8000"
    auth_subs_data.protectionParameterId="none"
    sequenceNumber = struct_pb2.Struct()
    sequenceNumber["{}-{}".format(0, 5, "NON_TIME_BASED", {}, args.sqn)]={}
    # sequenceNumber = SequenceNumber(
    #     difSign = Sign.Sign_POSITIVE,
    #     indLength = 5,
    #     sqnScheme="NON_TIME_BASED",
    #     lastIndexes={"ausf":22},
    #     sqn="000000000ac0"
    # )
    auth_subs_data.sequenceNumber.MergeFrom(sequenceNumber)
    auth_subs_data.encOpcKey=args.opc
    auth_subs_data.encPermanentKey=args.auth_key
    auth_subs_data.encTopcKey="some_key"
    auth_subs_data.vectorGenerationInHss=True
    #authsubsData.n5gcA    # smsdata = SessionManagementSubscriptionData()
    # assemble_smsdata(smsdata)uthMethod=AuthMethod()
    auth_subs_data.rgAuthenticationInd=True
    auth_subs_data.supi=args.imsi

def add_subscriber(client, args):
    am1 = assemble_am1(args)

    plmnSmfSelData = SmfSelectionSubscriptionData()
    assemble_plmnSmfSelData(plmnSmfSelData)

    smPolicySnssaiData = SmPolicySnssaiData()
    assemble_smPolicySnssaiData(smPolicySnssaiData)

    auth_subs_data = AuthenticationSubscription()
    assemble_auth_subs_data(auth_subs_data, args)

    sms_data = SmsSubscriptionData()
    assemble_sms_data(sms_data)

    sms_mng_data = SmsManagementSubscriptionData()
    assemble_sms_mng_data(sms_mng_data)

    am_policy_data = AmPolicyData()
    assemble_am_policy_data(am_policy_data)

    ue_policy_data = UePolicySet()
    assemble_ue_policy_data(ue_policy_data)

    pmn_subs_data=PMNSubscriberData(am1=am1,
                      plmnSmfSelData=plmnSmfSelData,
                      smPolicySnssaiData=smPolicySnssaiData,
                      auth_subs_data=auth_subs_data,
                      am_policy_data=am_policy_data,
                      ue_policy_data = ue_policy_data,
                      sms_data=sms_data,
                      sms_mng_data=sms_mng_data,
                      )

    smsdata = pmn_subs_data.plmnSmData["001-01"]
    assemble_smsdata(smsdata)

    from google.protobuf.json_format import MessageToJson
    print(MessageToJson(pmn_subs_data))
    #client.PMNSubscriberConfig(pmn_subs_data)

def create_parser():
    """
    Creates the argparse parser with all the arguments.
    """
    parser = argparse.ArgumentParser(
        description='Management CLI for PMN Subscriber',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Add subcommands
    subparsers = parser.add_subparsers(title="subcommands", dest="cmd")
    parser_add = subparsers.add_parser("add", help="Add a new subscriber")

    # Add arguments
    for cmd in [parser_add]:
        cmd.add_argument("--mcc", help="Mobile Country Code")
        cmd.add_argument("--mnc", help="Mobile Network Code")
        cmd.add_argument("--imsi", help="Subscriber ID")
        cmd.add_argument("--st", type=int, help="Slice type")
        cmd.add_argument("--sd", help="Slice differentiator")
        cmd.add_argument("--opc", help="encOpcKey")
        cmd.add_argument("--auth_key", help="encPermanentKey")
        cmd.add_argument("--subs_ambr_ul", help="Subscriber uplink Ambr")
        cmd.add_argument("--subs_ambr_dl", help="Subscriber downlink Ambr")
        cmd.add_argument("--dnn_name", help="Name of the dnn")
        cmd.add_argument("--dnn_ambr_ul", help="Dnn's uplink ambr")
        cmd.add_argument("--dnn_ambr_dl", help="Dnn's downlink ambr")
        cmd.add_argument("--qos_profile_5qi", help="Dnn's 5qi profile")


# Add function callbacks
    parser_add.set_defaults(func=add_subscriber)
    return parser

def main():
    parser = create_parser()

    # Parse the args
    args = parser.parse_args()
    if not args.cmd:
        parser.print_usage()
        exit(1)

    if args.cmd == 'add':
        if args.subs_ambr_dl is None or args.subs_ambr_ul is None or args.imsi is None\
                or args.sd is None or args.st is None or args.opc is None\
                or args.auth_key is None:
           parser.print_usage()
           exit(1)

    # Execute the subcommand function
    args.func(None, args)


if __name__ == "__main__":
    main()

#python3.9  pmn_subscriber_cli.py add --mcc 724 --mnc 99 --imsi 724990000000008 --st 1 --sd "fff" --opc E8ED289DEBA952E4283B54E88E6183CA --auth_key 465B5CE8B199B49FAA5F0A2EE238A6BC --subs_ambr_ul "10 Mbps" --subs_ambr_dl "20 Mbps" --dnn_name "apn1" --dnn_ambr_ul "10 Mbps"   --dnn_ambr_dl "20 Mbps" --qos_profile_5qi 5
