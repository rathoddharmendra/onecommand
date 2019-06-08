# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import paramiko
import pdb
import re
import time


# Create your views here.

def landing(request, template_name='onecommand/index.html'):

    return render(request, template_name)

def inventory(request, template_name='onecommand/inventory.html'):

    return render(request, template_name)


def result(request, template_name='onecommand/card.html'):

    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    hosts = []
    #finaloutput = []

    t1 = time.time()*1000
    if request.method == "POST":

        hosts = request.POST.getlist('nasservers')
        command = request.POST.get('command')
        ####Setting complete command for processing####
        def get_complete_cmd(command):
            foput = []
            oput =[]
            ssh.connect('nasegca2', port=22, username='autoadmin', password='sc7ba49ck35')
            stdin, stdout , stderr = ssh.exec_command(command,timeout=10)
            oput.append(stdout.readlines())
            foput.append('\n'.join(oput[0]))
            return foput[0]
            ssh.close()
        c1 = command.split()[0]
        c2 = 'export NAS_DB=/nas;export PATH=$PATH:/nas/bin:/nas/sbin;which ' + c1
        c2 = get_complete_cmd(c2)
        command = c2.split('\n')[0] + command[len(c1):]
        ########command is ready###########
        #print(hosts)
        Nasoutput = {}
        ##########Actual block of code############
        for host in hosts:

            try:
                finaloutput = []
                output =[]
                ssh.connect(host, port=22, username='autoadmin', password='sc7ba49ck35')

                finalcommand = 'hostname;export NAS_DB=/nas;' + command

                stdin, stdout , stderr = ssh.exec_command(finalcommand,timeout=10)

                output.append(stdout.readlines())

                finaloutput.append('\n'.join(output[0]))

                print(finaloutput[0])
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
