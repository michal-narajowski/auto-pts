#!/usr/bin/env python

#
# auto-pts - The Bluetooth PTS Automation Framework
#
# Copyright (c) 2018, Intel Corporation.
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

import logging
import os
import re
import subprocess
import sys
import time

import autoptsclient_common as autoptsclient
import ptsprojects.mynewt as autoprojects
import ptsprojects.stack as stack
from pybtp import btp
from ptsprojects.mynewt.iutctl import get_iut

import bot.common


def check_call(cmd, env=None, cwd=None, shell=True):
    """Run command with arguments.  Wait for command to complete.
    :param cmd: command to run
    :param env: environment variables for the new process
    :param cwd: sets current directory before execution
    :param shell: if true, the command will be executed through the shell
    :return: returncode
    """
    cmd = subprocess.list2cmdline(cmd)

    return subprocess.check_call(cmd, env=env, cwd=cwd, shell=shell)


def _validate_pair(ob):
    try:
        if not (len(ob) == 2):
            raise ValueError
    except:
        return False

    return True


def build_and_flash(project_path, board, overlay=None):
    """Build and flash Mynewt binary
    :param project_path: Mynewt source path
    :param board: IUT
    :param overlay: configuration map to be used
    :return: None
    """
    logging.debug("{}: {} {} {}".format(build_and_flash.__name__, project_path,
                                        board, overlay))

    check_call('rm -rf bin/'.split(), cwd=project_path)
    check_call('rm -rf targets/{}_boot/'.format(board).split(),
               cwd=project_path)
    check_call('rm -rf targets/bttester/'.split(), cwd=project_path)

    check_call('newt target create {}_boot'.format(board).split(),
               cwd=project_path)
    check_call('newt target create bttester'.split(), cwd=project_path)

    check_call(
        'newt target set {}_boot bsp=@apache-mynewt-core/hw/bsp/{}'.format(
            board, board).split(), cwd=project_path)
    check_call(
        'newt target set {}_boot app=@apache-mynewt-core/apps/boot'.format(
            board).split(), cwd=project_path)

    check_call(
        'newt target set bttester bsp=@apache-mynewt-core/hw/bsp/{}'.format(
            board).split(), cwd=project_path)
    check_call(
        'newt target set bttester app=@apache-mynewt-nimble/apps/bttester'.split(),
        cwd=project_path)

    if overlay is not None:
        config = ':'.join(['{}={}'.format(k, v) for k, v in overlay.items()])
        check_call('newt target set bttester syscfg={}'.format(config).split(),
                   cwd=project_path)

    check_call('newt build {}_boot'.format(board).split(), cwd=project_path)
    check_call('newt build bttester'.split(), cwd=project_path)

    check_call('newt create-image {}_boot 0.0.0'.format(board).split(),
               cwd=project_path)
    check_call('newt create-image bttester 0.0.0'.split(), cwd=project_path)

    check_call('newt load {}_boot'.format(board).split(), cwd=project_path)
    check_call('newt load bttester'.split(), cwd=project_path)


autopts2board = {
    None: None,
    'nrf52': 'nordic_pca10056'
}


def get_test_cases(ptses):
    """Get all test cases
    :param pts: PTS proxy instance
    :return: ZTestCase list
    """
    test_cases = autoprojects.gap.test_cases(ptses[0])
    test_cases += autoprojects.gatt.test_cases(ptses[0])
    test_cases += autoprojects.sm.test_cases(ptses[0])
    test_cases += autoprojects.l2cap.test_cases(ptses[0])
    mesh_test_cases, additional_mesh_test_cases = \
        autoprojects.mesh.test_cases(ptses)
    test_cases += mesh_test_cases
    additional_test_cases = additional_mesh_test_cases

    return test_cases, additional_test_cases


def run_tests(args, iut_config):
    """Run test cases
    :param args: AutoPTS arguments
    :param iut_config: IUT configuration
    :return: tuple of (status, results) dictionaries
    """
    results = {}
    status = {}
    descriptions = {}

    tty = './auto-pts-tester'
    callback_thread = autoptsclient.init_core()
    test_db_name = "mynewt_" + str(args["board"])

    ptses = []
    for ip in args["server_ip"]:
        ptses.append(autoptsclient.init_pts(ip, args["workspace"],
                                            args["bd_addr"],
                                            args["enable_max_logs"],
                                            callback_thread,
                                            test_db_name,
                                            args.get("local_ip", None)))

    btp.init(get_iut)
    # Main instance of PTS
    pts = ptses[0]

    stack.init_stack()
    stack_inst = stack.get_stack()
    stack_inst.synch_init(callback_thread.set_pending_response,
                          callback_thread.clear_pending_responses)
    cache = autoptsclient.cache_workspace(pts)

    default_to_omit = []

    for config, value in iut_config.items():
        if 'overlay' not in value:
            continue
        for test_case in value.get('test_cases', []):
            default_to_omit.append(test_case)

    for config, value in iut_config.items():
        overlay = None

        if 'overlay' in value:
            # TODO:
            overlay = value['overlay']
            to_run = value['test_cases']
            to_omit = None
        else:
            to_run = value['test_cases']
            to_omit = default_to_omit

        build_and_flash(args["project_path"], autopts2board[args["board"]],
                        overlay)
        time.sleep(1)

        autoprojects.iutctl.init(args["kernel_image"], tty, args["board"])

        test_cases, additional_test_cases = get_test_cases(ptses)
        if to_run or to_omit:
            test_cases = autoptsclient.get_test_cases_subset(test_cases,
                                                             to_run, to_omit)

        status_count, results_dict, regressions = \
            autoptsclient.run_test_cases(ptses, test_cases,
                                         additional_test_cases,
                                         int(args["retry"]))

        for k, v in status_count.items():
            if k in status.keys():
                status[k] += v
            else:
                status[k] = v

        results.update(results_dict)
        autoprojects.iutctl.cleanup()

    for test_case_name in results.keys():
        descriptions[test_case_name] = \
            autoptsclient.get_test_case_description(cache, test_case_name)

    autoptsclient.cache_cleanup(cache)

    pts.unregister_xmlrpc_ptscallback()

    return status, results, descriptions, regressions


def main(cfg):
    print("Mynewt bot start!")

    args = cfg['auto_pts']
    args['kernel_image'] = os.path.join(args['project_path'], 'bin',
                                        'targets', 'bttester', 'app', 'apps',
                                        'bttester', 'bttester.elf')

    core_path = os.path.join(os.path.abspath(args['project_path']), 'repos',
                             'apache-mynewt-core')
    nimble_path = os.path.join(os.path.abspath(args['project_path']), 'repos',
                               'apache-mynewt-nimble')

    core_hash = \
        bot.common.update_sources(core_path)

    nimble_hash = \
        bot.common.update_sources(nimble_path)

    mynewt_hash_status = 'Mynewt HEAD is on: core={}, nimble={}'.format(
        core_hash, nimble_hash)

    summary, results, descriptions, regressions = \
        run_tests(args, cfg.get('iut_config', {}))

    report_file = bot.common.make_report_xlsx(results, summary, regressions,
                                              descriptions)
    logs_file = bot.common.archive_recursive("logs")

    if 'gdrive' in cfg:
        drive = bot.common.Drive(cfg['gdrive'])
        url = drive.new_workdir(args['board'])
        drive.upload(report_file)
        drive.upload(logs_file)
        drive.upload("TestCase.db")

    if 'mail' in cfg:
        summary_html = bot.common.status_dict2summary_html(summary)
        url_html = bot.common.url2html(url, "Results on Google Drive")

        # Provide test case description
        _regressions = []
        for name in regressions:
            _regressions.append(
                name + " - " + descriptions.get(name, "no description"))

        reg_html = bot.common.regressions2html(_regressions)
        bot.common.send_mail(cfg['mail'], None, mynewt_hash_status,
                             args["board"], [summary_html, reg_html, url_html])

    bot.common.cleanup()

    print("\nBye!")
    sys.stdout.flush()
    return 0
