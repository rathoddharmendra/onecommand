# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import paramiko
import pdb


# Create your views here.

def landing(request, template_name='onecommand/index.html'):

    return render(request, template_name)


def result(request, template_name='onecommand/card.html'):

    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    hosts = []
    #finaloutput = []


    if request.method == "POST":

        hosts = request.POST.getlist('nasservers')
        command = request.POST.get('command')
        #print(hosts)
        Nasoutput = {}

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

                ####Creating Dictionaries

                Nasoutput.update({ host: finaloutput[0] })

            except Exception as error:

                print('We faced some issue with ' + host + '.You may need to login manually to this array')
                print(error)
                Nasoutput.update({ host: "Error with ssh connection" })
            ssh.close()

    return render(request,template_name,{'Nasoutput' : Nasoutput})
