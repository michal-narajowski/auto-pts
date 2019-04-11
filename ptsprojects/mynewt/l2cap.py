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

"""L2CAP test cases"""

try:
    from ptsprojects.testcase import TestCase, TestCmd, TestFunc, \
        TestFuncCleanUp
    from ptsprojects.mynewt.ztestcase import ZTestCase

except ImportError:  # running this module as script
    import sys
    sys.path.append("../..")  # to be able to locate the following imports

    from ptsprojects.testcase import TestCase, TestCmd, TestFunc, \
        TestFuncCleanUp
    from ptsprojects.mynewt.ztestcase import ZTestCase

from pybtp import btp
from pybtp.types import Addr
from ptsprojects.stack import get_stack


le_psm = 128


def set_pixits(pts):
    """Setup L2CAP profile PIXITS for workspace. Those values are used for test
    case if not updated within test case.

    PIXITS always should be updated accordingly to project and newest version of
    PTS.

    pts -- Instance of PyPTS"""

    pts.set_pixit("L2CAP", "TSPX_bd_addr_iut", "DEADBEEFDEAD")
    pts.set_pixit("L2CAP", "TSPX_bd_addr_iut_le", "DEADBEEFDEAD")
    pts.set_pixit("L2CAP", "TSPX_client_class_of_device", "100104")
    pts.set_pixit("L2CAP", "TSPX_server_class_of_device", "100104")
    pts.set_pixit("L2CAP", "TSPX_security_enabled", "FALSE")
    pts.set_pixit("L2CAP", "TSPX_delete_link_key", "FALSE")
    pts.set_pixit("L2CAP", "TSPX_pin_code", "0000")
    pts.set_pixit("L2CAP", "TSPX_flushto", "FFFF")
    pts.set_pixit("L2CAP", "TSPX_inmtu", "02A0")
    pts.set_pixit("L2CAP", "TSPX_no_fail_verdicts", "FALSE")
    pts.set_pixit("L2CAP", "TSPX_outmtu", "02A0")
    pts.set_pixit("L2CAP", "TSPX_tester_mps", "0017")
    pts.set_pixit("L2CAP", "TSPX_tester_mtu", "02A0")
    pts.set_pixit("L2CAP", "TSPX_iut_role_initiator", "FALSE")
    pts.set_pixit("L2CAP", "TSPX_le_psm", format(le_psm, '04x'))
    pts.set_pixit("L2CAP", "TSPX_psm", "0001")
    pts.set_pixit("L2CAP", "TSPX_psm_unsupported", "00F1")
    pts.set_pixit("L2CAP", "TSPX_psm_authentication_required", "00F2")
    pts.set_pixit("L2CAP", "TSPX_psm_authorization_required", "00F3")
    pts.set_pixit("L2CAP", "TSPX_psm_encryption_key_size_required", "00F4")
    pts.set_pixit("L2CAP", "TSPX_time_guard", "180000")
    pts.set_pixit("L2CAP", "TSPX_timer_ertx", "120000")
    pts.set_pixit("L2CAP", "TSPX_timer_ertx_max", "300000")
    pts.set_pixit("L2CAP", "TSPX_timer_ertx_min", "60000")
    pts.set_pixit("L2CAP", "TSPX_timer_rtx", "10000")
    pts.set_pixit("L2CAP", "TSPX_timer_rtx_min", "60000")
    pts.set_pixit("L2CAP", "TSPX_timer_rtx_max", "1000")
    pts.set_pixit("L2CAP", "TSPX_rfc_mode_tx_window_size", "08")
    pts.set_pixit("L2CAP", "TSPX_rfc_mode_max_transmit", "03")
    pts.set_pixit("L2CAP", "TSPX_rfc_mode_retransmission_timeout", "07D0")
    pts.set_pixit("L2CAP", "TSPX_rfc_mode_monitor_timeout", "2EE0")
    pts.set_pixit("L2CAP", "TSPX_rfc_mode_maximum_pdu_size", "02A0")
    pts.set_pixit("L2CAP", "TSPX_extended_window_size", "0012")
    pts.set_pixit("L2CAP", "TSPX_use_implicit_send", "TRUE")
    pts.set_pixit("L2CAP", "TSPX_use_dynamic_pin", "FALSE")
    pts.set_pixit("L2CAP", "TSPX_iut_SDU_size_in_bytes", "144")
    pts.set_pixit("L2CAP", "TSPX_secure_simple_pairing_pass_key_confirmation", "FALSE")
    pts.set_pixit("L2CAP", "TSPX_iut_address_type_random", "FALSE")
    pts.set_pixit("L2CAP", "TSPX_tester_adv_interval_min", "0030")
    pts.set_pixit("L2CAP", "TSPX_tester_adv_interval_max", "0050")
    pts.set_pixit("L2CAP", "TSPX_tester_le_scan_interval", "0C80")
    pts.set_pixit("L2CAP", "TSPX_tester_le_scan_window", "0C80")
    pts.set_pixit("L2CAP", "TSPX_tester_conn_interval_min", "0028")
    pts.set_pixit("L2CAP", "TSPX_tester_conn_interval_max", "0050")
    pts.set_pixit("L2CAP", "TSPX_tester_conn_latency", "0000")
    pts.set_pixit("L2CAP", "TSPX_tester_supervision_timeout", "00C8")
    pts.set_pixit("L2CAP", "TSPX_tester_min_CE_length", "0050")
    pts.set_pixit("L2CAP", "TSPX_tester_max_CE_length", "0C80")
    pts.set_pixit("L2CAP", "TSPX_generate_local_busy", "TRUE")


def test_cases(pts):
    """Returns a list of L2CAP test cases
    pts -- Instance of PyPTS"""

    le_psm = 128

    pts.update_pixit_param("L2CAP", "TSPX_le_psm", format(le_psm, '04x'))

    pts_bd_addr = pts.q_bd_addr

    stack = get_stack()

    stack.gap_init()

    pre_conditions = [TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.core_reg_svc_l2cap),
                      TestFunc(btp.gap_read_ctrl_info),
                      TestFunc(lambda: pts.update_pixit_param(
                          "L2CAP", "TSPX_bd_addr_iut",
                          stack.gap.iut_addr_get_str())),
                      TestFunc(lambda: pts.update_pixit_param(
                          "L2CAP", "TSPX_iut_address_type_random",
                          "TRUE" if stack.gap.iut_addr_is_random()
                          else "FALSE"))]

    test_cases = [
        # Connection Parameter Update
        ZTestCase("L2CAP", "L2CAP/LE/CPU/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_conn),
                   TestFunc(btp.gap_set_gendiscov),
                   TestFunc(btp.gap_adv_ind_on)]),
        ZTestCase("L2CAP", "L2CAP/LE/CPU/BV-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn,
                            pts_bd_addr, Addr.le_public, start_wid=51),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=22)]),
        ZTestCase("L2CAP", "L2CAP/LE/CPU/BI-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_conn,
                            pts_bd_addr, Addr.le_public, start_wid=51),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=22)]),
        ZTestCase("L2CAP", "L2CAP/LE/CPU/BI-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_conn),
                   TestFunc(btp.gap_adv_ind_on)]),

        # Command Reject
        ZTestCase("L2CAP", "L2CAP/LE/REJ/BI-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_conn),
                   TestFunc(btp.gap_adv_ind_on)]),
        ZTestCase("L2CAP", "L2CAP/LE/REJ/BI-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_conn),
                   TestFunc(btp.gap_adv_ind_on),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=22)]),

        # LE Credit Based Flow Control Mode
        ZTestCase("L2CAP", "L2CAP/COS/CFC/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.l2cap_le_listen, le_psm),
                   TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15),
                   TestFunc(btp.l2cap_connected_ev, post_wid=15),
                   TestFunc(btp.l2cap_send_data, 0, "FF", 40, start_wid=43)]),
        ZTestCase("L2CAP", "L2CAP/COS/CFC/BV-02-C",
                  pre_conditions +
                  [TestFunc(btp.l2cap_le_listen, le_psm),
                   TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15),
                   TestFunc(btp.l2cap_connected_ev, post_wid=15),
                   TestFunc(btp.l2cap_send_data, 0, "FF", 40, start_wid=43)]),
        ZTestCase("L2CAP", "L2CAP/COS/CFC/BV-03-C",
                  pre_conditions +
                  [TestFunc(btp.l2cap_le_listen, le_psm),
                   TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15),
                   TestFunc(btp.l2cap_connected_ev, post_wid=15),
                   TestFunc(btp.l2cap_data_rcv_ev, 0, True, post_wid=15),
                   TestFunc(btp.l2cap_disconnected_ev, 0, post_wid=40)],
                  verify_wids={40: btp.verify_description}),
        ZTestCase("L2CAP", "L2CAP/COS/CFC/BV-04-C",
                  pre_conditions +
                  [TestFunc(btp.l2cap_le_listen, le_psm),
                   TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15)]),
        ZTestCase("L2CAP", "L2CAP/COS/CFC/BV-05-C",
                  pre_conditions +
                  [TestFunc(btp.l2cap_le_listen, le_psm),
                   TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15),
                   TestFunc(btp.l2cap_conn, pts_bd_addr, Addr.le_public,
                            le_psm, start_wid=41),
                   TestFunc(btp.l2cap_connected_ev, post_wid=41)]),
        ZTestCase("L2CAP", "L2CAP/LE/CFC/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.l2cap_le_listen, le_psm),
                   TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15),
                   TestFunc(btp.l2cap_conn, pts_bd_addr, Addr.le_public,
                            le_psm, start_wid=41),
                   TestFunc(btp.l2cap_disconnected_ev, 0, False,
                            start_wid=39)]),
        ZTestCase("L2CAP", "L2CAP/LE/CFC/BV-02-C",
                  pre_conditions +
                  [TestFunc(btp.l2cap_le_listen, le_psm),
                   TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15),
                   TestFunc(btp.l2cap_conn, pts_bd_addr, Addr.le_public,
                            le_psm, start_wid=41),
                   TestFunc(btp.l2cap_connected_ev, post_wid=41),
                   TestFunc(btp.l2cap_data_rcv_ev, 0, True, post_wid=41)],
                  verify_wids={40: btp.verify_description}),
        ZTestCase("L2CAP", "L2CAP/LE/CFC/BV-03-C",
                  pre_conditions +
                  [TestFunc(btp.l2cap_le_listen, le_psm),
                   TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15),
                   TestFunc(btp.l2cap_connected_ev, post_wid=15),
                   TestFunc(btp.l2cap_send_data, 0, "FF", 60,
                            start_wid=43)],
                  verify_wids={37: "FF" * 60}),
        ZTestCase("L2CAP", "L2CAP/LE/CFC/BV-04-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15),
                   TestFunc(btp.l2cap_conn, pts_bd_addr, Addr.le_public,
                            241, start_wid=41),
                   TestFunc(btp.l2cap_disconnected_ev, 0, False,
                            post_wid=41)]),
        # "LE_PSM not supported" Result expected.
        # Verification is not needed, because if we received
        # disconnected event, that means connection was rejected.
        # verify_wids={42: btp.verify_description}),
        ZTestCase("L2CAP", "L2CAP/LE/CFC/BV-05-C",
                  pre_conditions +
                  [TestFunc(btp.l2cap_le_listen, le_psm),
                   TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15)]),
        ZTestCase("L2CAP", "L2CAP/LE/CFC/BV-06-C",
                  pre_conditions +
                  [TestFunc(btp.l2cap_le_listen, le_psm),
                   TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15),
                   TestFunc(btp.l2cap_connected_ev, post_wid=15),
                   TestFunc(btp.l2cap_send_data, 0, "FF", 10, start_wid=43)]),
        ZTestCase("L2CAP", "L2CAP/LE/CFC/BV-07-C",
                  pre_conditions +
                  [TestFunc(btp.l2cap_le_listen, le_psm),
                   TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15),
                   TestFunc(btp.l2cap_connected_ev, post_wid=15)]),
        ZTestCase("L2CAP", "L2CAP/LE/CFC/BI-01-C",
                  pre_conditions +
                  [TestFunc(btp.l2cap_le_listen, le_psm),
                   TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15),
                   TestFunc(btp.l2cap_connected_ev, post_wid=15),
                   TestFunc(btp.l2cap_send_data, 0, "FF", 40, start_wid=43)]),
        ZTestCase("L2CAP", "L2CAP/LE/CFC/BV-08-C",
                  pre_conditions +
                  [TestFunc(btp.l2cap_le_listen, le_psm),
                   TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15),
                   TestFunc(btp.l2cap_connected_ev, post_wid=15),
                   TestFunc(btp.l2cap_disconn, 0, start_wid=14),
                   TestFunc(btp.l2cap_disconnected_ev, 0, post_wid=14)]),
        ZTestCase("L2CAP", "L2CAP/LE/CFC/BV-09-C",
                  pre_conditions +
                  [TestFunc(btp.l2cap_le_listen, le_psm),
                   TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15)]),
        ZTestCase("L2CAP", "L2CAP/LE/CFC/BV-16-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15),
                   TestFunc(btp.l2cap_conn, pts_bd_addr, Addr.le_public,
                            le_psm, start_wid=41),
                   TestFunc(btp.l2cap_disconnected_ev, 0, False,
                            post_wid=41)]),
        # "LE_PSM not supported" Result expected.
        # Verification is not needed, because if we received
        # disconnected event, that means connection was rejected.
        # verify_wids={48: btp.verify_description}),
        ZTestCase("L2CAP", "L2CAP/LE/CFC/BV-18-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15),
                   TestFunc(btp.l2cap_conn, pts_bd_addr, Addr.le_public,
                            le_psm, start_wid=41),
                   TestFunc(btp.l2cap_disconnected_ev, 0, False,
                            post_wid=41)]),
        ZTestCase("L2CAP", "L2CAP/LE/CFC/BV-19-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15),
                   TestFunc(btp.l2cap_conn, pts_bd_addr, Addr.le_public,
                            le_psm, start_wid=41),
                   TestFunc(btp.l2cap_disconnected_ev, 0, False,
                            post_wid=41)]),
        ZTestCase("L2CAP", "L2CAP/LE/CFC/BV-20-C",
                  pre_conditions +
                  [TestFunc(btp.l2cap_le_listen, le_psm),
                   TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15),
                   TestFunc(btp.l2cap_connected_ev, post_wid=15),
                   TestFunc(btp.gap_disconn, pts_bd_addr,
                            Addr.le_public, start_wid=22),
                   TestFunc(btp.l2cap_disconnected_ev, 0, False,
                            post_wid=22)]),
        ZTestCase("L2CAP", "L2CAP/LE/CFC/BV-21-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_conn, start_wid=15),
                   TestFunc(btp.gap_adv_ind_on, start_wid=15),
                   TestFunc(btp.l2cap_conn, pts_bd_addr, Addr.le_public,
                            le_psm, start_wid=41),
                   TestFunc(btp.l2cap_disconnected_ev, 0, False,
                            post_wid=41)]),
    ]

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
            print "%d) %s" % (index, cmd)


if __name__ == "__main__":
    main()
