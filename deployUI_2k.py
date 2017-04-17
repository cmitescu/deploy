#!/usr/bin/python

import argparse
import time
import os, sys
import win32serviceutil
import urllib, zipfile
import pywintypes
import ssl, socket
import logging


from ConfigParser import SafeConfigParser
from classes.SmtEnv import *
from classes.CarolinaServer import *


_DEFAULT_CONTAINER_NAME = 'summit-ui-container'
_DEFAULT_UI_PRODUCT_NAME = 'summit-product-ui'
_DEFAULT_CARGO_PORT = '8282'
_DEFAULT_NODE_PORT = '3001'


def get_path(path_to_create):
    if _platform == 'Windows':
        path = '\\'.join(path_to_create)
        logging.debug(path)
    elif _platform == 'Unix':
        path = '/'.join(path_to_create)
        logging.debug(path)
    else:
        logging.critical('OS cannot be recognisable. Program will now exit... ')
        exit(2)
    return path

# def switch_product(summit_ui_version, product_zip_name, summit_ui_path):
#     product_build_name = _DEFAULT_UI_PRODUCT_NAME + "-" + summit_ui_version
#     target_path = summit_ui_path + "\\builds\\" + product_build_name
#     working_link = summit_ui_path + "\\" + _DEFAULT_UI_PRODUCT_NAME
#     zip_file_path = download_ui_package(summit_ui_version, product_zip_name)
#
#     if os.path.exists(target_path):
#         print product_build_name + " already exists. Build will not be switched ... "
#         return 0
#     else:
#         print "Extracting " + product_zip_name + " in " + summit_ui_path + "\\builds"
#         path_length_limit_prefix = "\\\\?\\"  # increases windows path length limit from 260 to 32000
#         with zipfile.ZipFile(zip_file_path, 'r') as handler:
#             handler.extractall(path_length_limit_prefix + target_path)
#         print "Copying the user folder from old to new build"
#         print os.popen("xcopy {0}\\data\\users {1}\\data\\users /e /i".format(working_link, target_path)).read()
#         print "Removing old link: {0}".format(working_link)
#         print os.popen("rd {0}".format(working_link)).read()
#         print os.popen("mklink /j {0} {1}".format(working_link, target_path)).read()
#
#
# def configure_product(summit_ui_path):
#     print "Summit UI product will be configured"
#
#     with open(summit_ui_path + "\\" + _DEFAULT_UI_PRODUCT_NAME + "\\mb-package.json") as mbpackage, \
#             open(summit_ui_path + "\\" + _DEFAULT_UI_PRODUCT_NAME + "\\addons\\services\\common.json") as common, \
#             open(summit_ui_path + "\\" + _DEFAULT_UI_PRODUCT_NAME + "\\addons\\services\\fcc.json") as fcc, \
#             open(summit_ui_path + "\\" + _DEFAULT_UI_PRODUCT_NAME + "\\addons\\services\\summitUI.json") as summitUI, \
#             open(summit_ui_path + "\\" + _DEFAULT_UI_PRODUCT_NAME + "\\addons\\services\\pricing-engine.json") as pricing_engine, \
#             open(summit_ui_path + "\\" + _DEFAULT_UI_PRODUCT_NAME + "\\addons\\services\\risk-pl.json") as risk:
#
#             newmbpackage = mbpackage.read().replace('localhost', _DEFAULT_HOSTNAME).replace('8181', _DEFAULT_CARGO_PORT)
#             newcommon = common.read().replace('localhost', _DEFAULT_HOSTNAME).replace('8181', _DEFAULT_CARGO_PORT)
#             newfcc = fcc.read().replace('localhost', _DEFAULT_HOSTNAME).replace('8181', _DEFAULT_CARGO_PORT)
#             newsummitui = summitUI.read().replace('localhost', _DEFAULT_HOSTNAME).replace('8181', _DEFAULT_CARGO_PORT)
#             newpricing_engine = pricing_engine.read().replace('localhost', _DEFAULT_HOSTNAME).replace('8181', _DEFAULT_CARGO_PORT)
#             newrisk = risk.read().replace('localhost', _DEFAULT_HOSTNAME).replace('8181', _DEFAULT_CARGO_PORT)
#
#     with open(summit_ui_path + "\\" + _DEFAULT_UI_PRODUCT_NAME + "\\mb-package.json", 'w') as mbpackage, \
#             open(summit_ui_path + "\\" + _DEFAULT_UI_PRODUCT_NAME + "\\addons\\services\\common.json", 'w') as common,\
#             open(summit_ui_path + "\\" + _DEFAULT_UI_PRODUCT_NAME + "\\addons\\services\\fcc.json", 'w') as fcc, \
#             open(summit_ui_path + "\\" + _DEFAULT_UI_PRODUCT_NAME + "\\addons\\services\\summitUI.json", 'w') as summitUI, \
#             open(summit_ui_path + "\\" + _DEFAULT_UI_PRODUCT_NAME + "\\addons\\services\\pricing-engine.json", 'w') as pricing_engine, \
#             open(summit_ui_path + "\\" + _DEFAULT_UI_PRODUCT_NAME + "\\addons\\services\\risk-pl.json", 'w') as risk:
#
#             mbpackage.write(newmbpackage)
#             common.write(newcommon)
#             fcc.write(newfcc)
#             summitUI.write(newsummitui)
#             pricing_engine.write(newpricing_engine)
#             risk.write(newrisk)
#
#     print "Summit UI product has been configured"
#
#
# def download_container_package(ui_container_version, container_zip_name, download_path):
#     file_path = download_path + "\\" + container_zip_name
#     url = 'https://bm-ci.misys.global.ad/jenkins/view/pipelines/job/bitbucket-projects/job/Summit/job/{0}/job/develop' \
#           '/{1}/artifact/container/target/{2}'.format(_DEFAULT_CONTAINER_NAME, ui_container_version, container_zip_name)
#     print "Downloading " + _DEFAULT_CONTAINER_NAME + " " + ui_container_version + "..."
#     print url
#     context = ssl._create_unverified_context()
#     urllib.urlretrieve(url, file_path, context=context)
#     return file_path
#
#
# def switch_container(ui_container_version, container_zip_name, summit_ui_path):
#     container_build_name = _DEFAULT_CONTAINER_NAME + "-" + ui_container_version
#     target_path = summit_ui_path + "\\builds\\" + container_build_name
#     zip_file_path = download_container_package(ui_container_version, container_zip_name)
#     working_link = summit_ui_path + "\\" + _DEFAULT_CONTAINER_NAME
#
#     if os.path.exists(target_path):
#         print container_build_name + " already exists. Build will not be switched ... "
#         return 0
#     else:
#         print "Extracting " + container_zip_name + " in " + summit_ui_path + "\\builds"
#         path_length_limit_prefix = "\\\\?\\"  # increases windows path length limit from 260 to 32000
#         with zipfile.ZipFile(zip_file_path, 'r') as handler:
#             handler.extractall(path_length_limit_prefix + target_path)
#     print "Removing old link: {0}".format(working_link)
#     print os.popen("rd {0}".format(working_link)).read()
#     print os.popen("mklink /j {0} {1}".format(working_link, target_path)).read()
#
#
# def configure_container(summit_ui_path):
#     print "Summit UI container will be configured"
#
#     javahome = "set JAVA_HOME=C:\SummitApps\SummitUI\jdk1.8.0_60"
#     javaopts = "set JAVA_OPTS=-Dcom.trmsys.cargo.web.httpPort=" + _DEFAULT_CARGO_PORT
#     setenv_bat = summit_ui_path + "\\" + _DEFAULT_CONTAINER_NAME + "\\bin\\setenv.bat"
#     stop_bat = summit_ui_path + "\\" + _DEFAULT_CONTAINER_NAME + "\\bin\\stop.bat"
#     server_conf = summit_ui_path + "\\" + _DEFAULT_CONTAINER_NAME + "\\etc\\server.conf"
#     repository = summit_ui_path + "\\repository\\" + _DEFAULT_CONTAINER_NAME + "\\etc\\server.conf"
#
#     # \bin folder
#     insert_variable(setenv_bat, 10, javahome + "\n")
#     insert_variable(setenv_bat, 11, javaopts + " -d64 -Xms2g -Xmx4g\n")
#     insert_variable(stop_bat, 6, "call " + setenv_bat + "\n")
#
#     # \etc folder - copy the server.conf from repository
#     os.popen("xcopy {0} {1} /e /Y /s".format(repository, server_conf)).read()
#     print "Summit UI container has been configured"
#
#
# def stop(summit_ui_path):
#     print "Stopping UI services... "
#     summit_container_path = summit_ui_path + "\\" + _DEFAULT_CONTAINER_NAME
#     summit_product_path = summit_ui_path + "\\" + _DEFAULT_UI_PRODUCT_NAME
#
#     try:
#         win32serviceutil.StopService(_DEFAULT_CONTAINER_NAME)
#         win32serviceutil.StopService(_DEFAULT_UI_PRODUCT_NAME)
#     except pywintypes.error as e:
#         print "Error stopping services "
#         print e
#
#     if os.path.isdir(summit_product_path):
#         os.chdir(summit_product_path)
#         print os.popen('stop.bat').read()
#     else:
#         print summit_product_path + " couldn't be found"
#
#     if os.path.isdir(summit_container_path):
#         os.chdir(summit_container_path)
#         print os.popen('stop.bat').read()
#     else:
#         print summit_container_path + " couldn't be found"
#
#     os.chdir(_SUMMIT_UI_PATH_WIN)
#
#
# def start():
#     print "Starting UI services..."
#
#     try:
#         win32serviceutil.StartService(_DEFAULT_CONTAINER_NAME)
#         win32serviceutil.StartService(_DEFAULT_UI_PRODUCT_NAME)
#     except pywintypes.error as e:
#         print "Error stopping services "
#         print e
#
#     time.sleep(5)
#
#     try:
#         win32serviceutil.StopService(_DEFAULT_CONTAINER_NAME)
#         win32serviceutil.StopService(_DEFAULT_UI_PRODUCT_NAME)
#     except pywintypes.error as e:
#         print "Error stopping services "
#         print e
#
#     # summit_container_path = _SUMMIT_UI_PATH + "\\" + _DEFAULT_CONTAINER_NAME
#     # summit_product_path = _SUMMIT_UI_PATH + "\\" + _DEFAULT_UI_PRODUCT_NAME
#
#     # if os.path.isdir(summit_product_path):
#     #     os.chdir(summit_product_path)
#     #     print os.popen('start.bat').read()
#     # else:
#     #     print summit_product_path + " couldn't be found"
#     #
#     # if os.path.isdir(summit_container_path):
#     #     os.chdir(summit_container_path)
#     #     print os.popen('start.bat').read()
#     # else:
#     #     print summit_container_path + " couldn't be found"
#     # os.chdir(_SUMMIT_UI_PATH)
#
#
# def insert_variable(filename, row, variable):
#     f = open(filename, 'r')
#     contents = f.readlines()
#     f.close()
#     contents.insert(row, variable)
#     f = open(filename, 'w')
#     f.writelines(contents)
#     f.close()


def conformity_check():
    logging.info('System will be checked if it can run summit insight package')
    for item in os.listdir(base_path):
        if os.path.isdir('SummitUI') and os.path.isdir('nodeJS'):
            logging.info(item + ' is available.')
        else:
            logging.critical('SummitUI folder cannot be found in path')
            exit(2)


def download_package(zip_name, version, download_path):
    logging.info(zip_name + ' will be downloaded.')
    file_path = get_path([download_path, zip_name])
    logging.debug(file_path)
    url = ''

    if 'container' in zip_name:
        url = 'https://bm-ci.misys.global.ad/jenkins/view/pipelines/job/bitbucket-projects/job/Summit/job/{0}/job/develop' \
              '/{1}/artifact/container/target/{2}'.format(_DEFAULT_CONTAINER_NAME, version, zip_name)
        logging.info("Downloading " + _DEFAULT_CONTAINER_NAME + " " + version + "...")
    elif 'product' in zip_name:
        url = "https://bm-ci.misys.global.ad/jenkins/view/Summit/job/{0}/{1}/artifact/app/target/{2}".format(
            _DEFAULT_UI_PRODUCT_NAME, version, zip_name)
        logging.info("Downloading " + _DEFAULT_UI_PRODUCT_NAME + " " + version + "...")
    else:
        logging.critical('Package is not recognisable. Program will now exit...')
        exit(2)

    context = ssl._create_unverified_context()
    urllib.urlretrieve(url, file_path, context=context)
    return file_path


def configure_package():
    print ''


def switch_package(zip_name, version, summit_ui_path, _platform, download_path):
    logging.info(zip_name + ' will be switched.')

    if 'container' in zip_name:
        print ''
    elif 'product' in zip_name:
        product_build_name = _DEFAULT_UI_PRODUCT_NAME + '-' + version + '_' + options.e
        target_path = get_path([summit_ui_path, 'builds', product_build_name])
        working_link = get_path([summit_ui_path, _DEFAULT_UI_PRODUCT_NAME + '_' + options.e])


        # zip_file_path = download_package(zip_name, version, download_path, _platform)
        #
        # if os.path.exists(target_path):
        #     print product_build_name + " already exists. Build will not be switched ... "
        #     return 0
        # else:
        #     print "Extracting " + product_zip_name + " in " + summit_ui_path + "\\builds"
        #     path_length_limit_prefix = "\\\\?\\"  # increases windows path length limit from 260 to 32000
        #     with zipfile.ZipFile(zip_file_path, 'r') as handler:
        #         handler.extractall(path_length_limit_prefix + target_path)
        #     print "Copying the user folder from old to new build"
        #     print os.popen("xcopy {0}\\data\\users {1}\\data\\users /e /i".format(working_link, target_path)).read()
        #     print "Removing old link: {0}".format(working_link)
        #     print os.popen("rd {0}".format(working_link)).read()
        #     print os.popen("mklink /j {0} {1}".format(working_link, target_path)).read()
    else:
        logging.critical('Package is not recognisable. Program will now exit...')
        exit(2)


def do_action(package, action):
    logging.info('Program will now ' + action + ' ' + package)
    action = [base_path, 'SummitUI', package + '_' + options.e, action + '.bat']
    remote_object.do_run(action)


def main():
    # initialization of a few global variables needed in other functions
    global options
    global _platform
    global base_path
    global remote_object

    parser = argparse.ArgumentParser(description="This script is used to make the UI switch / deployment. ")

    parser.add_argument('-cz', metavar='container zip', action='store', default=_DEFAULT_CONTAINER_NAME + '-1.1.0-SNAPSHOT.zip', help='container_ui zip name.')
    parser.add_argument('-pz', metavar='product zip', action='store', default=_DEFAULT_UI_PRODUCT_NAME + '-1.1.0-SNAPSHOT.zip', help='product_ui zip name.')
    parser.add_argument('-debug', action='store_true', help='Turn DEBUG output ON')

    # adding another category - required arguments
    required = parser.add_argument_group('required arguments')
    required.add_argument('-c', metavar='container version', action='store', help='container-ui build number')
    required.add_argument('-p', metavar='product version', action='store', help='product-ui build number')
    required.add_argument('-m', metavar='hostname', action='store', help='machine where switch is needed.')
    required.add_argument('-e', metavar='env_name', action='store', help='environment name.')
    required.add_argument('-switch', action='store_true', help='Switch the package(s). Default is False.')
    required.add_argument('-restart', action='store_true', help='Restart the packages. Default is False.')

    options = parser.parse_args()

    if len(sys.argv) < 4 or options.c == options.p == '' or options.switch == options.restart or options.m == '':
        parser.print_help()
        exit(2)

    if options.debug is True:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    if 'csw' in options.m:
        _platform = 'Windows'
        base_path = 'C:\\SummitApps'
    else:
        _platform = 'Unix'
        base_path = '/localhome/SummitApps'

    conformity_check()
    remote_object = CarolinaServer(options.m, username='', password='', platform=_platform)

    download_path = [base_path, 'SummitUI', 'archive']

    try:
        if options.switch:
            if options.c != '':
                do_action(_DEFAULT_CONTAINER_NAME, 'stop')
                download_package(options.cz, options.c, get_path(download_path))

                do_action(_DEFAULT_CONTAINER_NAME, 'start')
            elif options.p != '':
                do_action(_DEFAULT_UI_PRODUCT_NAME, 'stop')
                download_package(options.pz, options.p, get_path(download_path))

                do_action(_DEFAULT_UI_PRODUCT_NAME, 'start')
            else:
                logging.critical('Options is not recognized. Program will now exit...')
                exit(2)

        elif options.restart:
            logging.info('Program will only restart ui-container and product-ui')
            do_action(_DEFAULT_CONTAINER_NAME, 'stop')
            do_action(_DEFAULT_UI_PRODUCT_NAME, 'stop')
            time.sleep(5)
            do_action(_DEFAULT_CONTAINER_NAME, 'start')
            do_action(_DEFAULT_UI_PRODUCT_NAME, 'start')

        else:
            logging.critical('Options is ot recognized. Program will now exit...')
            exit(2)

    except Exception as e:
        logging.info(e)


if __name__ == "__main__":
    main()
