# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import paramiko
import pdb
import re
import time


# Create your views here.

def landing(request, template_name='isilon/isi_index.html'):

    return render(request, template_name)

def inventory(request, template_name='isilon/isi_inventory.html'):

    return render(request, template_name)


def result(request, template_name='isilon/isi_card.html'):

    import paramiko

    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def run_cmd(command):
        foput = []
        oput =[]
        ssh.connect('sondur1-1', port=22, username='root', password='1FSIsHer3!')
        stdin, stdout , stderr = ssh.exec_command(command,timeout=10)
        oput.append(stdout.readlines())
        foput.append('\n'.join(oput[0]))
        print(foput[0])
        ssh.close()
        
    hosts = []
    t1 = time.time()*1000
    if request.method == "POST":
        #hosts = request.POST.getlist('nasservers')
        hosts = ['sondur1-1']
        command = request.POST.get('command')        
        Nasoutput = {}
        ##########Actual block of code############
        for host in hosts:

            try:
                finaloutput = []
                output =[]
                ssh.connect(host, port=22, username='root', password='1FSIsHer3!!')

                finalcommand = 'hostname;' + command

                stdin, stdout , stderr = ssh.exec_command(finalcommand,timeout=10)

                output.append(stdout.readlines())

                finaloutput.append('\n'.join(output[0]))

                return finaloutput[0]
                finaloutput[0].split('\n')[0]

                ####Creating Dictionaries

                Nasoutput.update({ finaloutput[0].split('\n')[0]: finaloutput[0] })

            except Exception as error:

                print('We faced some issue with ' + host + '.You may need to login manually to this array')
                print(error)
                Nasoutput.update({ host: [host, error] })
            finally:
                ssh.close()
        t2 = time.time()*1000
        print("Total time taken: ", t2 - t1, " ms")

    return render(request,template_name,{'Nasoutput' : Nasoutput})

