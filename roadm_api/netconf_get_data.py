from ncclient import manager
from ncclient.xml_ import *
import os
import xml.dom.minidom as xmldom
import xml.etree.ElementTree as ET
import logging
import time

doc = xmldom.Document

if __name__ == "__main__":
    # LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
    # logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)
    with manager.connect(host="192.168.108.168", port=830, username="superuser",
                         password="Sup%9User",look_for_keys=False,hostkey_verify=False) as m:

        """ This will return all of the PM intervals for a 10ge: Entity """

        # stats_filter = """
        #                         <telemetry-subscriptions xmlns="http://www.lumentum.com/lumentum-telemetry-subscription">
        #                           <telemetry-subscription>
        #
        #                          </telemetry-subscription>
        #                         </telemetry-subscriptions>
        #                 """

        stats_filter = """
                         <active-alarm-list xmlns="http://www.lumentum.com/lumentum-alarms" xmlns:luma="http://www.lumentum.com/lumentum-alarms" xmlns:lotee="http://www.lumentum.com/lumentum-ote-edfa" xmlns:loteq="http://www.lumentum.com/lumentum-ote-equipment" xmlns:lotep="http://www.lumentum.com/lumentum-ote-port" xmlns:lotepopt="http://www.lumentum.com/lumentum-ote-port-optical" xmlns:loteeth="http://www.lumentum.com/lumentum-ote-port-ethernet" xmlns:lotepp="http://www.lumentum.com/lumentum-ote-port-pluggable" xmlns:loteps="http://www.lumentum.com/lumentum-ote-prot-switch" xmlns:lotefru="http://www.lumentum.com/lumentum-ote-fru" xmlns:lotefpm="http://www.lumentum.com/lumentum-ote-fru-power-module">
                        <number-of-alarms>
                        </number-of-alarms>
                        <last-changed></last-changed>
                            <alarm>
        
                         </alarm>
                           </active-alarm-list> 
                        """
        for i in range(15):
            result1 = m.get_config(filter = ('subtree', stats_filter),source="running")
            logging.info(result1)
            result = m.get(('subtree',stats_filter)).data_xml
            fp = open("ldy_%d.xml"%i, 'w+')
            fp.write(result)
            fp.close()
            time.sleep(5)
            # print(result1)

