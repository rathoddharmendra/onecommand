# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import paramiko
import pdb

# Create your views here.

def landing(request, template_name='onecommand/index.html'):

    return render(request, template_name)


def result(request, template_name='onecommand/result.html'):



    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #[Campus]:
    #hosts = [ 'nasegca2', 'nascrk3', 'nasishz1', 'nascncd2', 'nassisi1', 'nasinba1','nasbavdi1', 'nasgefr1', 'nasjpto1', 'nasukbr1', 	'nasfrpa1', 'nasCNBE1', 'nasRUSP1','nasCNSH1','nasAUSY1','nashapp2','nashvdi2','nasheng1', 'nashpra1', 'nasheng2',
             #'nashsap1', 'nashprd1','nashcrm1', 'nashsap2','nasheng3','nashepas1',
            #'enashsap1', 'nasdprb1', 'nasdprd1',  'nasdprc1', 'nasdpra1', 'nasdsap1',
             #'nasdeng2','nasdcrm1', 'nasdvdi','nasdeng2','nasdsas1', 'nasdepas1', 'nasdprb2','nasdeng3','enasdsap1',
             # 'nask','nasl','corpnash1','corpnasapp1','nash','nashapp2','nashsap1']

    #[issue]
    #hosts = ['nash','nashapp2','nashsap1']

    #[international]:
    #[issue]
    #hosts = ['nasCNSH1','nasAUSY1']

    j = 1
    hosts = []

    if request.method == "POST":
        hosts = request.POST.getlist('nasservers')
        command = request.POST.get('command')
        print(hosts)


        for host in hosts:

            try:

                ssh.connect(host, port=22, username='nasadmin', password='Dev0p#Emc1')

                finalcommand = 'hostname;export NAS_DB=/nas;' + command

                stdin, stdout , stderr = ssh.exec_command(finalcommand)

                output = stdout.readlines()
                #pdb.set_trace()

                finaloutput = ('\n'.join(output))
                print(finaloutput)
                c = 0
            except Exception as error:

                try:
                    ssh.connect(host, port=22, username='nasadmin', password='nasadmin')

                    stdin, stdout , stderr = ssh.exec_command('hostname;export NAS_DB=/nas;' + command)

                    output = stdout.readlines()

                    print('\n'.join(output))
                except Exception as error:
                    print('We faced some issue with ' + hosts[i] + '.You may need to login manually to this array')
                    print(error)


        ssh.close()
        """if c:
            print('Successfully completed')
        else:
            print('Some of the connections failed. Please login manually to those arrays') """

    return HttpResponse(finaloutput)
