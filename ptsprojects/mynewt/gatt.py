#
# auto-pts - The Bluetooth PTS Automation Framework
#
# Copyright (c) 2017, Intel Corporation.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms and conditions of the GNU General Public License,
# version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#

"""GATT test cases"""

try:
    from ptsprojects.testcase import TestCase, TestCmd, TestFunc, \
        TestFuncCleanUp, MMI
    from ptsprojects.mynewt.ztestcase import ZTestCase

except ImportError:  # running this module as script
    import sys
    sys.path.append("../..")  # to be able to locate the following imports

    from ptsprojects.testcase import TestCase, TestCmd, TestFunc, \
        TestFuncCleanUp, MMI
    from ptsprojects.mynewt.ztestcase import ZTestCase

from pybtp import btp
from pybtp.types import UUID, Addr, IOCap, Prop, Perm
from time import sleep
from ptsprojects.stack import get_stack
from ptsprojects.mynewt.gatt_wid import gatt_wid_hdl


def hdl_str(hdl):
    return '{0:x}'.format(hdl, 'x')


def u16_hdl_str(hdl):
    return '{0:04x}'.format(hdl, 'x')


def u16_hdl_uc_str(hdl):
    return '{0:04x}'.format(hdl, 'X')


class PTS_DB:
    PTS_UUID_FMT = '0000{}8c26476f89a7a108033a69c7'
    SVC = PTS_UUID_FMT.format('0001')
    CHR_NO_PERM = PTS_UUID_FMT.format('0002')
    CHR_READ = PTS_UUID_FMT.format('0003')
    CHR_RELIABLE_WRITE = PTS_UUID_FMT.format('0004')
    CHR_WRITE_NO_RSP = PTS_UUID_FMT.format('0005')
    CHR_READ_WRITE = PTS_UUID_FMT.format('0006')
    CHR_READ_WRITE_ENC = PTS_UUID_FMT.format('0007')
    CHR_READ_WRITE_AUTHEN = PTS_UUID_FMT.format('0008')
    CHR_READ_WRITE_AUTHOR = PTS_UUID_FMT.format('0009')
    DSC_READ = PTS_UUID_FMT.format('000a')
    DSC_WRITE = PTS_UUID_FMT.format('000b')
    DSC_READ_WRITE = PTS_UUID_FMT.format('000c')
    DSC_READ_WRITE_ENC = PTS_UUID_FMT.format('000d')
    DSC_READ_WRITE_AUTHEN = PTS_UUID_FMT.format('000e')
    INC_SVC = PTS_UUID_FMT.format('000f')
    CHR_READ_WRITE_ALT = PTS_UUID_FMT.format('0010')

    CHR_NO_PERM_ID = 0
    CHR_READ_ID = 1
    CHR_RELIABLE_WRITE_ID = 2
    CHR_WRITE_NO_RSP_ID = 3
    CHR_READ_WRITE_ID = 4
    CHR_READ_WRITE_ENC_ID = 5
    CHR_READ_WRITE_AUTHEN_ID = 6
    CHR_READ_WRITE_AUTHOR_ID = 7
    DSC_READ_ID = 8
    DSC_WRITE_ID = 9
    DSC_READ_WRITE_ID = 10
    DSC_READ_WRITE_ENC_ID = 11
    DSC_READ_WRITE_AUTHEN_ID = 12
    CHR_READ_WRITE_ALT_ID = 13

    iut_attr_db_off = 26

    SVC_HDL = u16_hdl_str(iut_attr_db_off + 0)
    CHR_NO_PERM_HDL = u16_hdl_str(iut_attr_db_off + 2)
    CHR_READ_HDL = u16_hdl_str(iut_attr_db_off + 4)
    CHR_RELIABLE_WRITE_HDL = u16_hdl_str(iut_attr_db_off + 7)
    CHR_WRITE_NO_RSP_HDL = u16_hdl_str(iut_attr_db_off + 9)
    CHR_READ_WRITE_HDL = hdl_str(iut_attr_db_off + 11)
    CHR_READ_WRITE_ENC_HDL = u16_hdl_str(iut_attr_db_off + 14)
    CHR_READ_WRITE_AUTHEN_HDL = u16_hdl_str(iut_attr_db_off + 16)
    CHR_READ_WRITE_AUTHOR_HDL = u16_hdl_str(iut_attr_db_off + 18)
    DSC_READ_HDL = u16_hdl_str(iut_attr_db_off + 19)
    DSC_WRITE_HDL = u16_hdl_str(iut_attr_db_off + 20)
    DSC_READ_WRITE_HDL = u16_hdl_str(iut_attr_db_off + 21)
    DSC_READ_WRITE_ENC_HDL = u16_hdl_str(iut_attr_db_off + 22)
    DSC_READ_WRITE_AUTHEN_HDL = u16_hdl_str(iut_attr_db_off + 23)
    SVC_END_HDL = u16_hdl_str(iut_attr_db_off + 23)
    INC_SVC_HDL = u16_hdl_str(iut_attr_db_off + 25)
    CHR_READ_WRITE_ALT_HDL = u16_hdl_str(iut_attr_db_off + 27)


class Value:
    one_byte = '01'
    two_bytes = '0123'
    eight_bytes_1 = '0123456789ABCDEF'
    eight_bytes_2 = 'FEDCBA9876543210'
    long_1 = eight_bytes_1 * 4
    long_2 = eight_bytes_2 * 4


def set_pixits(pts):
    """Setup GATT profile PIXITS for workspace. Those values are used for test
    case if not updated within test case.

    PIXITS always should be updated accordingly to project and newest version of
    PTS.

    pts -- Instance of PyPTS"""

    pts.set_pixit("GATT", "TSPX_bd_addr_iut", "DEADBEEFDEAD")
    pts.set_pixit("GATT", "TSPX_iut_device_name_in_adv_packet_for_random_address", "")
    pts.set_pixit("GATT", "TSPX_security_enabled", "FALSE")
    pts.set_pixit("GATT", "TSPX_delete_link_key", "TRUE")
    pts.set_pixit("GATT", "TSPX_time_guard", "180000")
    pts.set_pixit("GATT", "TSPX_selected_handle", "0012")
    pts.set_pixit("GATT", "TSPX_use_implicit_send", "TRUE")
    pts.set_pixit("GATT", "TSPX_secure_simple_pairing_pass_key_confirmation", "FALSE")
    pts.set_pixit("GATT", "TSPX_iut_use_dynamic_bd_addr", "FALSE")
    pts.set_pixit("GATT", "TSPX_iut_setup_att_over_br_edr", "FALSE")
    pts.set_pixit("GATT", "TSPX_tester_database_file",
                  "C:\Program Files\Bluetooth SIG\Bluetooth PTS\Data\SIGDatabase\GATT_Qualification_Test_Databases.xml")
    pts.set_pixit("GATT", "TSPX_iut_is_client_periphral", "FALSE")
    pts.set_pixit("GATT", "TSPX_iut_is_server_central", "FALSE")
    pts.set_pixit("GATT", "TSPX_mtu_size", "23")
    pts.set_pixit("GATT", "TSPX_pin_code", "0000")
    pts.set_pixit("GATT", "TSPX_use_dynamic_pin", "FALSE")
    pts.set_pixit("GATT", "TSPX_delete_ltk", "TRUE")
    pts.set_pixit("GATT", "TSPX_tester_appearance", "0000")


def test_cases_server(pts):
    """Returns a list of GATT Server test cases"""

    pts_bd_addr = pts.q_bd_addr
    stack = get_stack()

    pre_conditions = [TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.gap_read_ctrl_info),
                      TestFunc(lambda: pts.update_pixit_param(
                          "GATT", "TSPX_bd_addr_iut",
                          stack.gap.iut_addr_get_str())),
                      TestFunc(lambda: pts.update_pixit_param(
                          "GATT", "TSPX_iut_use_dynamic_bd_addr",
                          "TRUE" if stack.gap.iut_addr_is_random()
                          else "FALSE")),
                      TestFunc(btp.core_reg_svc_gatt),
                      TestFunc(btp.gap_set_conn),
                      TestFunc(btp.gap_set_gendiscov)]

    pre_conditions_1 = [TestFunc(btp.core_reg_svc_gap),
                        TestFunc(btp.core_reg_svc_gatt),
                        TestFunc(btp.gap_read_ctrl_info),
                        TestFunc(lambda: pts.update_pixit_param(
                            "GATT", "TSPX_bd_addr_iut",
                            stack.gap.iut_addr_get_str())),
                        TestFunc(lambda: pts.update_pixit_param(
                            "GATT", "TSPX_iut_use_dynamic_bd_addr",
                            "TRUE" if stack.gap.iut_addr_is_random()
                            else "FALSE"))]

    init_gatt_db = [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                    TestFunc(btp.gatts_add_char, 0,
                             Prop.read | Prop.write,
                             Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                    TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
                             Value.eight_bytes_1 * 32),
                    TestFunc(btp.gatts_start_server)]

    test_cases = [
        ZTestCase("GATT", "GATT/SR/GAC/BV-01-C",
                  pre_conditions_1 + init_gatt_db,
                  generic_wid_hdl=gatt_wid_hdl),
        ZTestCase("GATT", "GATT/SR/GAD/BV-01-C",
                  pre_conditions_1 + init_gatt_db,
                  generic_wid_hdl=gatt_wid_hdl),
        ZTestCase("GATT", "GATT/SR/GAD/BV-02-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)],
                  verify_wids={23: ("UUID= '%s" % UUID.gap_svc,
                                    "start handle = '0001'",
                                    "end handle = '0005'")}),
        ZTestCase("GATT", "GATT/SR/GAD/BV-03-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read | Prop.write,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_add_svc, 0, PTS_DB.INC_SVC),
                   TestFunc(btp.gatts_add_inc_svc, 1),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)],
                  verify_wids={24: ("Attribute Handle = '%s'" %
                                    PTS_DB.INC_SVC_HDL,
                                    "Included Service Attribute handle = '%s'" %
                                    PTS_DB.SVC_HDL,
                                    "End Group Handle = '%s'" %
                                    PTS_DB.SVC_END_HDL,
                                    "Service UUID = '%s'" % PTS_DB.SVC)}),
        ZTestCase("GATT", "GATT/SR/GAD/BV-04-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)],
                  verify_wids={25: ("UUID= '%s'" % UUID.gap_svc,
                                    "handle='0002'")}),
        ZTestCase("GATT", "GATT/SR/GAD/BV-05-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read | Prop.write,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAD/BV-06-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read | Prop.write,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_add_desc, 0, Perm.read | Perm.write,
                            PTS_DB.DSC_READ_WRITE),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read | Prop.write,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BI-01-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0, 0x00, 0x00,
                            PTS_DB.CHR_NO_PERM),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_NO_PERM_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BI-02-C",
                  edit1_wids={118: "ffff"},
                  cmds=pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            0x00, 0x00, PTS_DB.CHR_NO_PERM),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_NO_PERM_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        # Not supported
        # ZTestCase("GATT", "GATT/SR/GAR/BI-03-C",
        #           pre_conditions +
        #           [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
        #            TestFunc(btp.gatts_add_char, 0, Prop.read, Perm.read_authz,
        #                     PTS_DB.CHR_READ_WRITE_AUTHOR),
        #            TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_AUTHOR_ID,
        #                     Value.one_byte),
        #            TestFunc(btp.gatts_start_server),
        #            TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BI-04-C",
                  edit1_wids={2000: btp.var_store_get_passkey},
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.no_input_output),
                   TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0, Prop.read,
                            Perm.read_authn,
                            PTS_DB.CHR_READ_WRITE_AUTHEN),
                   TestFunc(btp.gatts_set_val,
                            PTS_DB.CHR_READ_WRITE_AUTHEN_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BI-05-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0, Prop.read, Perm.read_enc,
                            PTS_DB.CHR_READ_WRITE_ENC),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ENC_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_set_enc_key_size, 2, 0x0f),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BV-03-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read | Prop.write,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BI-06-C",
                  edit1_wids={111: PTS_DB.CHR_NO_PERM,
                              110: PTS_DB.CHR_NO_PERM_HDL},
                  cmds=pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0, 0x00, 0x00,
                            PTS_DB.CHR_NO_PERM),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_NO_PERM_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BI-07-C",
                  edit1_wids={119: 'ffff'},
                  cmds=pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.broadcast | Prop.read,
                            Perm.read | Perm.write,
                            PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BI-08-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.broadcast | Prop.read,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        # Not supported
        # ZTestCase("GATT", "GATT/SR/GAR/BI-09-C",
        #           edit1_wids={113: PTS_DB.CHR_READ_WRITE_AUTHOR,
        #                       112: PTS_DB.CHR_READ_WRITE_AUTHOR_HDL},
        #           cmds=pre_conditions +
        #           [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
        #            TestFunc(btp.gatts_add_char, 0, Prop.read,
        #                     Perm.read_authz,
        #                     PTS_DB.CHR_READ_WRITE_AUTHOR),
        #            TestFunc(btp.gatts_set_val,
        #                     PTS_DB.CHR_READ_WRITE_AUTHOR_ID,
        #                     Value.one_byte),
        #            TestFunc(btp.gatts_start_server),
        #            TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BI-10-C",
                  edit1_wids={115: PTS_DB.CHR_READ_WRITE_AUTHEN,
                              114: PTS_DB.CHR_READ_WRITE_AUTHEN_HDL},
                  cmds=pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0, Prop.read,
                            Perm.read_authn,
                            PTS_DB.CHR_READ_WRITE_AUTHEN),
                   TestFunc(btp.gatts_set_val,
                            PTS_DB.CHR_READ_WRITE_AUTHEN_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BI-11-C",
                  edit1_wids={121: PTS_DB.CHR_READ_WRITE_ENC_HDL,
                              122: PTS_DB.CHR_READ_WRITE_ENC},
                  cmds=pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0, Prop.read,
                            Perm.read_enc, PTS_DB.CHR_READ_WRITE_ENC),
                   TestFunc(btp.gatts_set_val,
                            PTS_DB.CHR_READ_WRITE_ENC_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_set_enc_key_size, 0, 0x0f),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BV-04-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read | Prop.write,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
                            Value.long_1),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)],
                  verify_wids={52: ("Please confirm IUT Handle='%s'" %
                                    PTS_DB.CHR_READ_WRITE_HDL,
                                    "value='" + Value.long_1 + "'")}),
        ZTestCase("GATT", "GATT/SR/GAR/BI-12-C",
                  edit1_wids={110: PTS_DB.CHR_NO_PERM_HDL},
                  cmds=pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0, 0x00, 0x00,
                            PTS_DB.CHR_NO_PERM),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_NO_PERM_ID,
                            Value.long_1),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BI-13-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read | Prop.write,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
                            Value.long_1),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BI-14-C",
                  edit1_wids={118: "ffff"},
                  cmds=pre_conditions +
                   [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                    TestFunc(btp.gatts_add_char, 0,
                             Prop.read | Prop.write,
                             Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                    TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
                             Value.long_1),
                    TestFunc(btp.gatts_start_server),
                    TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        # Not supported
        # ZTestCase("GATT", "GATT/SR/GAR/BI-15-C",
        #           pre_conditions +
        #           [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
        #            TestFunc(btp.gatts_add_char, 0, Prop.read, Perm.read_authz,
        #                     PTS_DB.CHR_READ_WRITE_AUTHOR),
        #            TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_AUTHOR_ID,
        #                     Value.long_1),
        #            TestFunc(btp.gatts_start_server),
        #            TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BI-16-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0, Prop.read, Perm.read_authn,
                            PTS_DB.CHR_READ_WRITE_AUTHEN),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_AUTHEN_ID,
                            Value.long_1),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BI-17-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read, Perm.read_enc,
                            PTS_DB.CHR_READ_WRITE_ENC),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ENC_ID,
                            Value.long_1),
                   TestFunc(btp.gatts_set_enc_key_size, 0, 0x0f),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BV-05-C",
                  pre_conditions,
                  generic_wid_hdl=gatt_wid_hdl),
        ZTestCase("GATT", "GATT/SR/GAR/BI-18-C",
                  edit1_wids={110: PTS_DB.CHR_NO_PERM_HDL},
                  cmds=pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            0x00, 0x00, PTS_DB.CHR_NO_PERM),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_NO_PERM_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read | Prop.write,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
                            Value.two_bytes),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BI-19-C",
                  edit1_wids={118: "ffff"},
                  cmds=pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            0x00, 0x00, PTS_DB.CHR_NO_PERM),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_NO_PERM_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read, Perm.read, PTS_DB.CHR_READ),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_ID,
                            Value.two_bytes),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read | Prop.write,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        # Not supported
        # ZTestCase("GATT", "GATT/SR/GAR/BI-20-C",
        #           edit1_wids={123: "0003", 124: "0005"},
        #           cmds=pre_conditions +
        #           [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
        #            TestFunc(btp.gatts_add_char, 0,
        #                     Prop.read, Perm.read, PTS_DB.CHR_READ),
        #            TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_ID,
        #                     Value.one_byte),
        #            TestFunc(btp.gatts_add_char, 0,
        #                     Prop.read, Perm.read_authz,
        #                     PTS_DB.CHR_READ_WRITE_AUTHOR),
        #            TestFunc(btp.gatts_set_val,
        #                     PTS_DB.CHR_READ_WRITE_AUTHOR_ID,
        #                     Value.two_bytes),
        #            TestFunc(btp.gatts_add_char, 0,
        #                     Prop.read | Prop.write,
        #                     Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
        #            TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
        #                     Value.one_byte),
        #            TestFunc(btp.gatts_start_server),
        #            TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BI-21-C",
                  edit1_wids={123: "0003", 124: "0005"},
                  cmds=pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read, Perm.read_authn,
                            PTS_DB.CHR_READ_WRITE_AUTHEN),
                   TestFunc(btp.gatts_set_val,
                            PTS_DB.CHR_READ_WRITE_AUTHEN_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read, Perm.read, PTS_DB.CHR_READ),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_ID,
                            Value.two_bytes),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read | Prop.write,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BI-22-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read, Perm.read, PTS_DB.CHR_READ),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_ID, '0512'),
                   TestFunc(btp.gatts_add_char, 0, Prop.read,
                            Perm.read_enc, PTS_DB.CHR_READ_WRITE_ENC),
                   TestFunc(btp.gatts_set_val,
                            PTS_DB.CHR_READ_WRITE_ENC_ID, '01'),
                   TestFunc(btp.gatts_set_enc_key_size, 0, 0x0f),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAR/BV-06-C",
                  pre_conditions_1 +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read, Perm.read, PTS_DB.CHR_READ),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_ID,
                            Value.eight_bytes_1),
                   TestFunc(btp.gatts_add_desc, 0, Perm.read,
                            PTS_DB.DSC_READ),
                   TestFunc(btp.gatts_set_val, PTS_DB.DSC_READ_ID,
                            Value.eight_bytes_2),
                   TestFunc(btp.gatts_start_server)],
                  generic_wid_hdl=gatt_wid_hdl),
        ZTestCase("GATT", "GATT/SR/GAR/BV-07-C",
                  pre_conditions_1 +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read, Perm.read, PTS_DB.CHR_READ),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_add_desc, 0, Perm.read,
                            PTS_DB.DSC_READ),
                   TestFunc(btp.gatts_set_val, PTS_DB.DSC_READ_ID,
                            Value.long_1),
                   TestFunc(btp.gatts_start_server)],
                  generic_wid_hdl=gatt_wid_hdl),
        ZTestCase("GATT", "GATT/SR/GAR/BV-08-C",
                  pre_conditions_1 +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read, Perm.read, PTS_DB.CHR_READ),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_add_desc, 0, Perm.read,
                            PTS_DB.DSC_READ),
                   TestFunc(btp.gatts_set_val, PTS_DB.DSC_READ_ID,
                            Value.long_1),
                   TestFunc(btp.gatts_start_server)],
                  generic_wid_hdl=gatt_wid_hdl),
        ZTestCase("GATT", "GATT/SR/GAW/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.broadcast | Prop.read | Prop.write_wo_resp,
                            Perm.read | Perm.write, PTS_DB.CHR_WRITE_NO_RSP),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_WRITE_NO_RSP_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)],
                  verify_wids={75: ("Please confirm IUT Write characteristic "
                                    "handle= '%s'O value= 'BE'O" %
                                    PTS_DB.CHR_WRITE_NO_RSP_HDL,)}),
        # Not supported
        # ZTestCase("GATT", "GATT/SR/GAW/BV-02-C",
        #           pre_conditions +
        #           [TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
        #            TestFunc(btp.gatts_add_char, 0,
        #                     Prop.read | Prop.write | Prop.auth_swrite,
        #                     Perm.read | Perm.write, UUID.VND16_2),
        #            TestFunc(btp.gatts_set_val, 0, Value.eight_bytes_1),
        #            TestFunc(btp.gatts_start_server),
        #            TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        # ZTestCase("GATT", "GATT/SR/GAW/BI-01-C",
        #           pre_conditions +
        #           [TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
        #            TestFunc(btp.gatts_add_char, 0,
        #                     Prop.read | Prop.auth_swrite,
        #                     Perm.read | Perm.write_authn, UUID.VND16_2),
        #            TestFunc(btp.gatts_set_val, 0, Value.eight_bytes_1),
        #            TestFunc(btp.gatts_start_server),
        #            TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAW/BV-03-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0, Prop.read | Prop.write,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
                            Value.two_bytes),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAW/BI-02-C",
                  edit1_wids={118: "ffff"},
                  cmds=pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.broadcast | Prop.read | Prop.write_wo_resp,
                            Perm.read | Perm.write,
                            PTS_DB.CHR_WRITE_NO_RSP),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_WRITE_NO_RSP_ID,
                            Value.two_bytes),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAW/BI-03-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.broadcast | Prop.read, Perm.read,
                            PTS_DB.CHR_READ),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_ID,
                            Value.two_bytes),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        # Not supported
        # ZTestCase("GATT", "GATT/SR/GAW/BI-04-C",
        #           pre_conditions +
        #           [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
        #            TestFunc(btp.gatts_add_char, 0, Prop.read | Prop.write,
        #                     Perm.read | Perm.write_authz,
        #                     PTS_DB.CHR_READ_WRITE_AUTHOR),
        #            TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_AUTHOR_ID,
        #                     Value.two_bytes),
        #            TestFunc(btp.gatts_start_server),
        #            TestFunc(btp.gap_adv_ind_on)]),
        ZTestCase("GATT", "GATT/SR/GAW/BI-05-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0, Prop.read | Prop.write,
                            Perm.read | Perm.write_authn,
                            PTS_DB.CHR_READ_WRITE_AUTHEN),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_AUTHEN_ID,
                            Value.two_bytes),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        ZTestCase("GATT", "GATT/SR/GAW/BI-06-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0, Prop.read | Prop.write,
                            Perm.read | Perm.write_enc,
                            PTS_DB.CHR_READ_WRITE_ENC),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ENC_ID,
                            Value.two_bytes),
                   TestFunc(btp.gatts_set_enc_key_size, 0, 0x0f),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAW/BV-05-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read | Prop.write,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
                            Value.long_1),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAW/BI-07-C",
                  edit1_wids={118: "ffff"},
                  cmds=pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.broadcast | Prop.read | Prop.write_wo_resp,
                            Perm.read | Perm.write,
                            PTS_DB.CHR_WRITE_NO_RSP),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_WRITE_NO_RSP_ID,
                            Value.long_1),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAW/BI-08-C",
                  edit1_wids={120: "0002"},
                  cmds=pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.broadcast | Prop.read, Perm.read,
                            PTS_DB.CHR_READ),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_ID,
                            Value.long_1),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAW/BI-09-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0, Prop.read | Prop.write,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
                            Value.long_1),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        # Not supported
        # ZTestCase("GATT", "GATT/SR/GAW/BI-11-C",
        #           pre_conditions +
        #           [TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
        #            TestFunc(btp.gatts_add_char, 0, Prop.read | Prop.write,
        #                     Perm.read | Perm.write_authz, UUID.VND16_2),
        #            TestFunc(btp.gatts_set_val, 0, Value.long_1),
        #            TestFunc(btp.gatts_start_server),
        #            TestFunc(btp.gap_adv_ind_on)]),
        ZTestCase("GATT", "GATT/SR/GAW/BI-12-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0, Prop.read | Prop.write,
                            Perm.read | Perm.write_authn,
                            PTS_DB.CHR_READ_WRITE_AUTHEN),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_AUTHEN_ID,
                            Value.long_1),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        ZTestCase("GATT", "GATT/SR/GAW/BI-13-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0, Prop.read | Prop.write,
                            Perm.read | Perm.write_enc,
                            PTS_DB.CHR_READ_WRITE_ENC),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ENC_ID,
                            Value.long_1),
                   TestFunc(btp.gatts_set_enc_key_size, 0, 0x0f),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAW/BV-06-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.broadcast | Prop.read | Prop.write,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
                            Value.long_1),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAW/BV-07-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.broadcast | Prop.read | Prop.write,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
                            Value.long_1),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAW/BV-08-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read, Perm.read, PTS_DB.CHR_READ),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_add_desc, 0,
                            Perm.read | Perm.write, PTS_DB.DSC_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.DSC_READ_WRITE_ID,
                            Value.two_bytes),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAW/BV-09-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read, Perm.read, PTS_DB.CHR_READ),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_add_desc, 0,
                            Perm.read | Perm.write, PTS_DB.DSC_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.DSC_READ_WRITE_ID,
                            Value.long_1),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAW/BV-10-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read | Prop.write,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
                            Value.long_1),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.read | Prop.write,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE_ALT),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ALT_ID,
                            Value.long_2),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAW/BV-11-C",
                  pre_conditions,
                  generic_wid_hdl=gatt_wid_hdl),
        ZTestCase("GATT", "GATT/SR/GAW/BI-32-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0, Prop.read | Prop.write,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
                            Value.one_byte),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAW/BI-33-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0, Prop.read | Prop.write,
                            Perm.read | Perm.write, PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID,
                            Value.long_1),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1)]),
        ZTestCase("GATT", "GATT/SR/GAN/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.nofity | Prop.read | Prop.write, Perm.read,
                            PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID, '00'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1),
                   TestFunc(sleep, 1, start_wid=92),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID, '01',
                            start_wid=92)]),
        ZTestCase("GATT", "GATT/SR/GAI/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.indicate | Prop.read | Prop.write, Perm.read,
                            PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID, '00'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1),
                   TestFunc(sleep, 1, start_wid=98),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID, '01',
                            start_wid=98)]),
        ZTestCase("GATT", "GATT/SR/GAS/BV-01-C",
                  edit1_wids={2000: btp.var_store_get_passkey},
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_adv_ind_on, start_wid=1),

                   # Service Changed is triggered for bonded devices only
                   TestFunc(btp.gap_wait_for_connection,
                            start_wid=1),
                   TestFunc(btp.gap_pair, start_wid=1),
                   TestFunc(btp.gap_wait_for_disconnection, post_wid=96),
                   TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC, post_wid=96),
                   TestFunc(btp.gatts_start_server, post_wid=96)]),
        ZTestCase("GATT", "GATT/SR/GAT/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gatts_add_svc, 0, PTS_DB.SVC),
                   TestFunc(btp.gatts_add_char, 0,
                            Prop.indicate | Prop.read | Prop.write, Perm.read,
                            PTS_DB.CHR_READ_WRITE),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID, '00'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on, start_wid=1),
                   TestFunc(sleep, 1, start_wid=98),
                   TestFunc(btp.gatts_set_val, PTS_DB.CHR_READ_WRITE_ID, '01',
                            start_wid=98)]),
        ZTestCase("GATT", "GATT/SR/UNS/BI-01-C",
                  pre_conditions,
                  generic_wid_hdl=gatt_wid_hdl),
        ZTestCase("GATT", "GATT/SR/UNS/BI-02-C",
                  pre_conditions,
                  generic_wid_hdl=gatt_wid_hdl),
    ]

    return test_cases


def test_cases_client(pts):
    """Returns a list of GATT Client test cases

    pts -- Instance of PyPTS

    """

    pts_bd_addr = pts.q_bd_addr
    stack = get_stack()

    pre_conditions = [TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.gap_read_ctrl_info),
                      TestFunc(lambda: pts.update_pixit_param(
                          "GATT", "TSPX_bd_addr_iut",
                          stack.gap.iut_addr_get_str())),
                      TestFunc(btp.core_reg_svc_gatt)]

    test_cases = [
        ZTestCase("GATT", "GATT/CL/GAC/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_exchange_mtu,
                            Addr.le_public, pts_bd_addr,
                            start_wid=12),
                   TestFunc(btp.gattc_write_long, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, 0, '12', MMI.arg_2,
                            start_wid=69),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=69),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)]),
        ZTestCase("GATT", "GATT/CL/GAD/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_disc_prim_svcs,
                            Addr.le_public, pts_bd_addr, start_wid=10),
                   TestFunc(btp.gattc_disc_prim_svcs_rsp, start_wid=10),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={17: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAD/BV-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_disc_prim_uuid,
                            Addr.le_public, pts_bd_addr,
                            MMI.arg_1, start_wid=18),
                   TestFunc(btp.gattc_disc_prim_uuid_rsp, True, start_wid=18),
                   TestFunc(btp.gattc_disc_prim_uuid,
                            Addr.le_public, pts_bd_addr,
                            MMI.arg_1, start_wid=20),
                   TestFunc(btp.gattc_disc_prim_uuid_rsp, True, start_wid=20),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={19: btp.verify_description,
                               21: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAD/BV-03-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_find_included,
                            Addr.le_public, pts_bd_addr, None,
                            None, start_wid=15),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={24: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAD/BV-04-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_disc_all_chrc,
                            Addr.le_public, pts_bd_addr,
                            MMI.arg_2, MMI.arg_3, start_wid=27),
                   TestFunc(btp.gattc_disc_all_chrc_rsp, True, start_wid=27),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={28: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAD/BV-05-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_disc_chrc_uuid,
                            Addr.le_public, pts_bd_addr,
                            MMI.arg_1, MMI.arg_2, MMI.arg_3, start_wid=29),
                   TestFunc(btp.gattc_disc_chrc_uuid_rsp, True, start_wid=29),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={30: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAD/BV-06-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_disc_all_desc,
                            Addr.le_public, pts_bd_addr,
                            MMI.arg_1, MMI.arg_2, start_wid=31),
                   TestFunc(btp.gattc_disc_all_desc_rsp, True, start_wid=31),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={32: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BV-01-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, start_wid=48),
                   TestFunc(btp.gattc_read_rsp, store_val=True,
                            start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={50: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BI-01-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, start_wid=48),
                   TestFunc(btp.gattc_read_rsp, store_rsp=True,
                            start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={40: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BI-02-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, start_wid=48),
                   TestFunc(btp.gattc_read_rsp, store_rsp=True,
                            start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={41: btp.verify_description}),
        # Not supported
        # ZTestCase("GATT", "GATT/CL/GAR/BI-03-C",
        #           cmds=pre_conditions +
        #           [TestFunc(btp.gap_conn, pts_bd_addr,
        #                     Addr.le_public, start_wid=2),
        #            TestFunc(btp.gattc_read, Addr.le_public,
        #                     pts_bd_addr, MMI.arg_1, start_wid=48),
        #            TestFunc(btp.gattc_read_rsp, store_rsp=True,
        #                     start_wid=48),
        #            TestFunc(btp.gap_disconn, pts_bd_addr,
        #                     Addr.le_public, start_wid=3)],
        #           verify_wids={42: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BI-04-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, start_wid=48),
                   TestFunc(btp.gattc_read_rsp,
                            store_rsp=True, start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={43: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BI-05-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, start_wid=48),
                   TestFunc(btp.gattc_read_rsp, store_rsp=True,
                            start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={44: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BV-03-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read_uuid, Addr.le_public,
                            pts_bd_addr, 0x0001, 0xffff, MMI.arg_1,
                            start_wid=108),
                   TestFunc(btp.gattc_read_uuid_rsp, store_val=True,
                            start_wid=108),
                   TestFunc(btp.gattc_read_uuid, Addr.le_public,
                            pts_bd_addr, 0x0001, 0xffff, MMI.arg_1,
                            start_wid=109),
                   TestFunc(btp.gattc_read_uuid_rsp, store_val=True,
                            start_wid=109),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={50: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BI-06-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read_uuid, Addr.le_public,
                            pts_bd_addr, MMI.arg_2, MMI.arg_3, MMI.arg_1,
                            start_wid=51),
                   TestFunc(btp.gattc_read_uuid_rsp, store_rsp=True,
                            start_wid=51),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={41: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BI-07-C",
                  cmds=pre_conditions +
                       [TestFunc(btp.gap_conn, pts_bd_addr,
                                 Addr.le_public, start_wid=2),
                        TestFunc(btp.gattc_read_uuid, Addr.le_public,
                                 pts_bd_addr, MMI.arg_2, MMI.arg_3, MMI.arg_1,
                                 start_wid=51),
                        TestFunc(btp.gattc_read_uuid_rsp, store_rsp=True,
                                 start_wid=51),
                        TestFunc(btp.gap_disconn, pts_bd_addr,
                                 Addr.le_public, start_wid=3)],
                  verify_wids={45: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BI-10-C",
                  cmds=pre_conditions +
                       [TestFunc(btp.gap_conn, pts_bd_addr,
                                 Addr.le_public, start_wid=2),
                        TestFunc(btp.gattc_read_uuid, Addr.le_public,
                                 pts_bd_addr, MMI.arg_2, MMI.arg_3, MMI.arg_1,
                                 start_wid=51),
                        TestFunc(btp.gattc_read_uuid_rsp, store_rsp=True,
                                 start_wid=51),
                        TestFunc(btp.gap_disconn, pts_bd_addr,
                                 Addr.le_public, start_wid=3)],
                  verify_wids={43: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BI-11-C",
                  cmds=pre_conditions +
                       [TestFunc(btp.gap_conn, pts_bd_addr,
                                 Addr.le_public, start_wid=2),
                        TestFunc(btp.gattc_read_uuid, Addr.le_public,
                                 pts_bd_addr, MMI.arg_2, MMI.arg_3, MMI.arg_1,
                                 start_wid=51),
                        TestFunc(btp.gattc_read_uuid_rsp, store_rsp=True,
                                 start_wid=51),
                        TestFunc(btp.gap_disconn, pts_bd_addr,
                                 Addr.le_public, start_wid=3)],
                  verify_wids={44: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BV-04-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read_long, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, 0, start_wid=48),
                   TestFunc(btp.gattc_read_long_rsp, store_val=True,
                            start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={52: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BI-12-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, start_wid=48),
                   TestFunc(btp.gattc_read_rsp, store_rsp=True,
                            start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={41: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BI-13-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read_long,
                            Addr.le_public, pts_bd_addr,
                            MMI.arg_1, MMI.arg_2, 1, start_wid=53),
                   TestFunc(btp.gattc_read_long_rsp, store_rsp=True,
                            start_wid=53),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={46: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BI-14-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, start_wid=48),
                   TestFunc(btp.gattc_read_rsp, store_rsp=True,
                            start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={40: btp.verify_description}),
        # Not supported
        # ZTestCase("GATT", "GATT/CL/GAR/BI-15-C",
        #           cmds=pre_conditions +
        #           [TestFunc(btp.gap_conn, pts_bd_addr,
        #                     Addr.le_public, start_wid=2),
        #            TestFunc(btp.gattc_read, Addr.le_public,
        #                     pts_bd_addr, MMI.arg_1, start_wid=48),
        #            TestFunc(btp.gattc_read_rsp, store_rsp=True,
        #                     start_wid=48),
        #            TestFunc(btp.gap_disconn, pts_bd_addr,
        #                     Addr.le_public, start_wid=3)],
        #           verify_wids={42: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BI-16-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, start_wid=48),
                   TestFunc(btp.gattc_read_rsp, store_rsp=True,
                            start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={43: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BI-17-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, start_wid=48),
                   TestFunc(btp.gattc_read_rsp, store_rsp=True,
                            start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={44: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BV-05-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read_multiple,
                            Addr.le_public, pts_bd_addr,
                            MMI.arg_1, MMI.arg_2, start_wid=57),
                   TestFunc(btp.gattc_read_multiple_rsp,
                            store_val=True, start_wid=57),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={55: btp.verify_multiple_read_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BI-18-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read_multiple,
                            Addr.le_public, pts_bd_addr,
                            MMI.arg_1, MMI.arg_2, start_wid=57),
                   TestFunc(btp.gattc_read_multiple_rsp, store_rsp=True,
                            start_wid=57),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={41: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BI-19-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read_multiple,
                            Addr.le_public, pts_bd_addr,
                            MMI.arg_1, MMI.arg_2, start_wid=57),
                   TestFunc(btp.gattc_read_multiple_rsp, store_rsp=True,
                            start_wid=57),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={40: btp.verify_description}),
        # Not supported
        # ZTestCase("GATT", "GATT/CL/GAR/BI-20-C",
        #           cmds=pre_conditions +
        #           [TestFunc(btp.gap_conn, pts_bd_addr,
        #                     Addr.le_public, start_wid=2),
        #            TestFunc(btp.gattc_read_multiple,
        #                     Addr.le_public, pts_bd_addr,
        #                     MMI.arg_1, MMI.arg_2, start_wid=57),
        #            TestFunc(btp.gattc_read_multiple_rsp, store_rsp=True,
        #                     start_wid=57),
        #            TestFunc(btp.gap_disconn, pts_bd_addr,
        #                     Addr.le_public, start_wid=3)],
        #           verify_wids={42: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BI-21-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read_multiple,
                            Addr.le_public, pts_bd_addr,
                            MMI.arg_1, MMI.arg_2, start_wid=57),
                   TestFunc(btp.gattc_read_multiple_rsp, store_rsp=True,
                            start_wid=57),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={43: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BI-22-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read_multiple,
                            Addr.le_public, pts_bd_addr,
                            MMI.arg_1, MMI.arg_2, start_wid=57),
                   TestFunc(btp.gattc_read_multiple_rsp,
                            store_rsp=True, start_wid=57),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={44: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BV-06-C",
                  edit1_wids={104: btp.var_store_get_passkey},
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, start_wid=58),
                   TestFunc(btp.gattc_read_rsp, store_val=True,
                            start_wid=58),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={59: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BV-07-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, start_wid=58),
                   TestFunc(btp.gattc_read_rsp, store_val=True,
                            start_wid=58),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={52: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAR/BI-35-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, start_wid=48),
                   TestFunc(btp.gattc_read_rsp, store_rsp=True,
                            start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={47: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAW/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_write_without_rsp,
                            Addr.le_public, pts_bd_addr,
                            MMI.arg_1, '12', MMI.arg_2, start_wid=70),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)]),
        # Not supported
        # PTS issue #15965
        # ZTestCase("GATT", "GATT/CL/GAW/BV-02-C",
        #           pre_conditions +
        #           [TestFunc(btp.gap_conn, pts_bd_addr,
        #                     Addr.le_public, start_wid=2),
        #            TestFunc(btp.gattc_signed_write,
        #                     Addr.le_public, pts_bd_addr,
        #                     MMI.arg_1, '12', None, start_wid=72),
        #            TestFunc(btp.gap_disconn, pts_bd_addr,
        #                     Addr.le_public, start_wid=3)]),
        ZTestCase("GATT", "GATT/CL/GAW/BV-03-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_write, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, '12', MMI.arg_2,
                            start_wid=74),
                   TestFunc(btp.gattc_write_rsp, start_wid=74),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)]),
        ZTestCase("GATT", "GATT/CL/GAW/BI-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_write, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, '12', MMI.arg_2,
                            start_wid=74),
                   TestFunc(btp.gattc_write_rsp, True, start_wid=74),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={61: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAW/BI-03-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_write, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, '12', MMI.arg_2,
                            start_wid=74),
                   TestFunc(btp.gattc_write_rsp, True, start_wid=74),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={62: btp.verify_description}),
        # Not supported
        # ZTestCase("GATT", "GATT/CL/GAW/BI-04-C",
        #           pre_conditions +
        #           [TestFunc(btp.gap_conn, pts_bd_addr,
        #                     Addr.le_public, start_wid=2),
        #            TestFunc(btp.gattc_write, Addr.le_public,
        #                     pts_bd_addr, MMI.arg_1, '12', MMI.arg_2,
        #                     start_wid=74),
        #            TestFunc(btp.gattc_write_rsp, True, start_wid=74),
        #            TestFunc(btp.gap_disconn, pts_bd_addr,
        #                     Addr.le_public, start_wid=3)],
        #           verify_wids={63: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAW/BI-05-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_write, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, '12', MMI.arg_2,
                            start_wid=74),
                   TestFunc(btp.gattc_write_rsp, True, start_wid=74),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={64: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAW/BI-06-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_write, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, '12', MMI.arg_2,
                            start_wid=74),
                   TestFunc(btp.gattc_write_rsp, True, start_wid=74),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={65: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAW/BV-05-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_write_long, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, 0, '12', MMI.arg_2,
                            start_wid=76),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=76),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)]),
        ZTestCase("GATT", "GATT/CL/GAW/BI-07-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_write_long, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, 0, '12', MMI.arg_2,
                            start_wid=76),
                   TestFunc(btp.gattc_write_long_rsp, True, start_wid=76),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={61: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAW/BI-08-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_write_long, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, 0, '12', MMI.arg_2,
                            start_wid=76),
                   TestFunc(btp.gattc_write_long_rsp, True, start_wid=76),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={62: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAW/BI-09-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_write_long, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, MMI.arg_2, '12', None,
                            start_wid=77),
                   TestFunc(btp.gattc_write_long_rsp, True, start_wid=77),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={66: btp.verify_description}),
        # Not supported
        # ZTestCase("GATT", "GATT/CL/GAW/BI-11-C",
        #           pre_conditions +
        #           [TestFunc(btp.gap_conn, pts_bd_addr,
        #                     Addr.le_public, start_wid=2),
        #            TestFunc(btp.gattc_write_long, Addr.le_public,
        #                     pts_bd_addr, MMI.arg_1, 0, '12', MMI.arg_2,
        #                     start_wid=76),
        #            TestFunc(btp.gattc_write_long_rsp, True, start_wid=76),
        #            TestFunc(btp.gap_disconn, pts_bd_addr,
        #                     Addr.le_public, start_wid=3)],
        #           verify_wids={63: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAW/BI-12-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_write_long, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, 0, '12', MMI.arg_2,
                            start_wid=76),
                   TestFunc(btp.gattc_write_long_rsp, True, start_wid=76),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={64: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAW/BI-13-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_write_long, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, 0, '12', MMI.arg_2,
                            start_wid=76),
                   TestFunc(btp.gattc_write_long_rsp, True, start_wid=76),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={65: btp.verify_description}),
        # TODO: GATT/CL/GAW/BV-06-C
        ZTestCase("GATT", "GATT/CL/GAW/BV-08-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_write, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, '12', MMI.arg_2,
                            start_wid=74),
                   TestFunc(btp.gattc_write_rsp, start_wid=74),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)]),
        ZTestCase("GATT", "GATT/CL/GAW/BV-09-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_write_long, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, 0, '12', MMI.arg_2,
                            start_wid=76),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=76),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)]),
        # TODO: GATT/CL/GAW/BI-32-C
        ZTestCase("GATT", "GATT/CL/GAW/BI-33-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_write, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, '1234', MMI.arg_2,
                            start_wid=80),
                   TestFunc(btp.gattc_write_rsp, True, start_wid=80),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={67: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAW/BI-34-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_write_long, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, 0, '1234', MMI.arg_2,
                            start_wid=81),
                   TestFunc(btp.gattc_write_long_rsp, True, start_wid=81),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)],
                  verify_wids={67: btp.verify_description}),
        ZTestCase("GATT", "GATT/CL/GAN/BV-01-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_cfg_notify, Addr.le_public,
                            pts_bd_addr, 1, MMI.arg_1, start_wid=91),
                   TestFunc(btp.gattc_notification_ev, pts_bd_addr,
                            Addr.le_public, 1, start_wid=91),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)]),
        ZTestCase("GATT", "GATT/CL/GAI/BV-01-C",
                  cmds=pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_cfg_indicate, Addr.le_public,
                            pts_bd_addr, 1, MMI.arg_1, start_wid=99),
                   TestFunc(btp.gattc_notification_ev, pts_bd_addr,
                            Addr.le_public, 2, start_wid=99),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)]),
        ZTestCase("GATT", "GATT/CL/GAS/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)]),
        # PTS CASE0036198
        ZTestCase("GATT", "GATT/CL/GAT/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_read, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, start_wid=48),
                   TestFunc(btp.gattc_read_rsp, False, False, 40,
                            start_wid=49),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)]),
        # PTS CASE0036198
        ZTestCase("GATT", "GATT/CL/GAT/BV-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn, pts_bd_addr,
                            Addr.le_public, start_wid=2),
                   TestFunc(btp.gattc_write, Addr.le_public,
                            pts_bd_addr, MMI.arg_1, '12', MMI.arg_2,
                            start_wid=74),
                   TestFunc(btp.gattc_write_rsp, False, 40, start_wid=71),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=3)]),
    ]

    return test_cases


def test_cases(pts):
    """Returns a list of GATT test cases"""

    stack = get_stack()

    stack.gap_init()

    pts.update_pixit_param("GATT", "TSPX_delete_link_key", "TRUE")
    pts.update_pixit_param("GATT", "TSPX_delete_ltk", "TRUE")

    test_cases = test_cases_client(pts)
    test_cases += test_cases_server(pts)

    return test_cases


def main():
    """Main."""
    import ptsprojects.mynewt.iutctl as iutctl

    iutctl.init_stub()

    test_cases_ = test_cases("AB:CD:EF:12:34:56")

    for test_case in test_cases_:
        print
        print test_case

        if test_case.edit1_wids:
            print "edit1_wids: %r" % test_case.edit1_wids

        if test_case.verify_wids:
            print "verify_wids: %r" % test_case.verify_wids

        for index, cmd in enumerate(test_case.cmds):
            str_cmd = str(cmd)

            if isinstance(cmd, TestFunc):
                if cmd.func == btp.gatts_add_char:
                    str_cmd += ", Properties: %s" % Prop.decode(cmd.args[1])
                    str_cmd += ", Permissions: %s" % Perm.decode(cmd.args[2])
                elif cmd.func == btp.gatts_add_desc:
                    str_cmd += ", Permissions: %s" % Perm.decode(cmd.args[1])

            print "%d) %s" % (index, str_cmd)


if __name__ == "__main__":
    main()
