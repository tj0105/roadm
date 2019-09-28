import requests,json
import ssl
import urllib
import urllib3
from socket import *
import socketserver
import time

context = ssl._create_unverified_context()

# auth username and password
postData = {
    "username": "admin",
    "password": "admin",
}
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}
HOST = "192.168.109.229"
PORT =20191
BUFSIZ = 1024
ADDR = (HOST, PORT)
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

#post a config for the pod  return the "org-openroadm-service:service-create" : { }
def postconfig(url,headers,data):
    '''
    the methos is post the request about the configuration to the pod ,then pod receive the data
    to configuration the roadm

    :param url: the post url
    :param headers: headers
    :param data: configuration information
    :return: request return
    '''
    requests.packages.urllib3.disable_warnings()
    r=requests.post(url=url,headers=headers,data=json.dumps(data),verify=False)
    return r.text

# first post a request to get a id_token
def login():
    '''
    the method is get the JSON WEB TOKEN,if you do not have the id_token,you can not post/get
    the request to the pod.
    :return:
     '''
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    requests.packages.urllib3.disable_warnings()
    r = requests.post('http://pod-cluster.example.com/operation/auth/authenticate',
                headers=headers, data=json.dumps(postData),verify=False)
    return r.json()["id_token"]

# this is a single node
def process_json__data_single(json_data,receive_data):
    '''
    the method ist process the file of the signle_create_optical_service,change the release the value
    to configuration the roadm

    :param json_data: the file of single_create_optical_service
    :param receive_data: the socket_data
    :return:
    '''
    json_data['org-openroadm-service:service-create']['service-name']='W'+receive_data[0]+'-'+receive_data[1]+'@'+receive_data[2]
    json_data['org-openroadm-service:service-create']['service-a-end']['node-id']=receive_data[2]
    json_data['org-openroadm-service:service-create']['service-a-end']['user-label']=receive_data[3]
    json_data['org-openroadm-service:service-create']['service-z-end']['user-label'] = receive_data[3]
    json_data['org-openroadm-service:service-create']['net-juniper-service-create:topology']['aToZ'][0]['device']['node-id']=receive_data[2]
    json_data['org-openroadm-service:service-create']['net-juniper-service-create:topology']['aToZ'][1]['device']['node-id']=receive_data[2]
    json_data['org-openroadm-service:service-create']['net-juniper-service-create:topology']['aToZ'][2]['device']['node-id']=receive_data[2]
    json_data['org-openroadm-service:service-create']['net-juniper-service-create:topology']['aToZ'][0]['resource']['port']['port-name']=receive_data[1]
    json_data['org-openroadm-service:service-create']['net-juniper-service-create:topology']['aToZ'][2]['resource']['port']['port-name'] = receive_data[1]
    json_data['org-openroadm-service:service-create']['net-juniper-service-create:topology']['aToZ'][1]['resource']['connection-number']= receive_data[0]
    with open("config.json", 'w')as f:
        f.write(str(json_data))
    print(json_data)

#this is a both node
def process_json__data_both(json_data,receive_data,user_label):
    '''
        the method ist process the file of the both_create_optical_service,change the release the value
        to configuration the roadm

        :param json_data: the file of both_create_optical_service
        :param receive_data: the socket_data
        :return:
        '''
    node_1=receive_data[0]
    node_1_port=receive_data[1]
    node_2=receive_data[3]
    node_2_port=receive_data[4]
    connection_number=receive_data[2]
    print(node_1,node_1_port,node_2,node_2_port,connection_number)
    json_data['org-openroadm-service:service-create']['service-name']=\
        'W'+connection_number+'-'+node_1_port+'@'+node_1+'-'+node_2_port+'@'+node_2
    json_data['org-openroadm-service:service-create']['service-a-end']['node-id'] = node_1
    json_data['org-openroadm-service:service-create']['service-a-end']['user-label'] = user_label
    json_data['org-openroadm-service:service-create']['service-z-end']['node-id'] = node_2
    json_data['org-openroadm-service:service-create']['service-z-end']['user-label'] = user_label
    json_data['org-openroadm-service:service-create']['net-juniper-service-create:topology']['aToZ'][0]['device']['node-id']=node_1
    json_data['org-openroadm-service:service-create']['net-juniper-service-create:topology']['aToZ'][1]['device']['node-id']=node_1
    json_data['org-openroadm-service:service-create']['net-juniper-service-create:topology']['aToZ'][2]['device']['node-id']=node_1
    json_data['org-openroadm-service:service-create']['net-juniper-service-create:topology']['aToZ'][3]['device']['node-id']=node_2
    json_data['org-openroadm-service:service-create']['net-juniper-service-create:topology']['aToZ'][4]['device']['node-id']=node_2
    json_data['org-openroadm-service:service-create']['net-juniper-service-create:topology']['aToZ'][5]['device']['node-id']=node_2
    json_data['org-openroadm-service:service-create']['net-juniper-service-create:topology']['aToZ'][0]['resource']['port']['port-name']=node_1_port
    json_data['org-openroadm-service:service-create']['net-juniper-service-create:topology']['aToZ'][5]['resource']['port']['port-name']=node_2_port
    json_data['org-openroadm-service:service-create']['net-juniper-service-create:topology']['aToZ'][1]['resource']['connection-number']= connection_number
    json_data['org-openroadm-service:service-create']['net-juniper-service-create:topology']['aToZ'][4]['resource']['connection-number'] = connection_number

def socket_receive_data(data):
    '''
    the method is convet the socket_receive_data to the ROADM IPaddress,ROADM wave length ROADM port
    :param data: socket_receive_data
    :return: list of ipaddress,wavelength,port
    '''
    process_data=[]
    process_data=data.split()
    if process_data[0]=='0':
        process_data[0]="192.168.108.168"
    else:
        process_data[0]="192.168.108.169"
    process_data[2]=str(97-int(process_data[2]))
    process_data[1]="port:1_1_U"+process_data[1]
    return process_data

def get_config(URL):
    '''
    the method is get the config through the different URL
    :return:
    '''
    # print(login())
    headers["Authorization"] = 'Bearer ' + login()
    # print(headers)
    r = requests.get(URL, headers=headers, verify=False)
    return r

def get_service_list():
    '''
    the method is get the all of the service by the pod
    :return:
    '''
    get_service_lsit = 'http://pod-cluster.example.com/network/restconf/data/org-openroadm-service:service-list'
    data=get_config(get_service_lsit)
    return data.json()
receive_list = []

if __name__ == '__main__':
    before_services_list_number=len(get_service_list()["org-openroadm-service:service-list"]["services"])
    # print(now_services_list)
    with open("configuration_json/both_creat_optical_service",'r') as load_f:
        data=json.load(load_f)
    print(data)
    headers["Authorization"] = 'Bearer ' + login()
    print(headers)
    url = "http://pod-cluster.example.com/network/restconf/operations/org-openroadm-service:service-create"
    print(postconfig(url, headers, data))
    for i in range(100):
        service_list_data=get_service_list()
        now_service_list_number=len(service_list_data["org-openroadm-service:service-list"]["services"])
        if now_service_list_number==before_services_list_number+1:
            print(service_list_data["org-openroadm-service:service-list"]["services"][before_services_list_number])
            marjor_alarm_number=service_list_data["org-openroadm-service:service-list"]["services"][before_services_list_number]["net-juniper-service-ext:alarm-counts-details"]["major"]
            critical_alarm_number=service_list_data["org-openroadm-service:service-list"]["services"][before_services_list_number]["net-juniper-service-ext:alarm-counts-details"]["critical"]
            print(marjor_alarm_number,critical_alarm_number)
            if marjor_alarm_number==0 and critical_alarm_number==0:
                print("there have no major and critical alarm")
                break
        time.sleep(1)

    # while True:
    #     print("waiting for connection...")
    #     tcpCliSock, addr = tcpSerSock.accept()
    #     print("connected from :", addr)
    #     while True:
    #         receive_data = str(tcpCliSock.recv(BUFSIZ), encoding="utf-8")
    #         if not receive_data:
    #             break
    #         print(receive_data)
    #         print(type(receive_data))
    #         receive_list = receive_list + socket_receive_data(receive_data)
    #         print(len(receive_list))
    #         print(receive_list)
    #         # if len(receive_list)==6:
    #         #     user_label="CH"+receive_list[2]
    #         #     receive_list=receive_list
    #         #     process_json__data_both(data,receive_list,user_label)
    #         #     headers["Authorization"] = 'Bearer ' + login()
    #         #     print(headers)
    #         #     url = "http://pod-cluster.example.com/network/restconf/operations/org-openroadm-service:service-create"
    #         #     print(postconfig(url, headers, data))
    #         #     receive_list=[]
    #     tcpCliSock.close()
    # tcpSerSock.close()

