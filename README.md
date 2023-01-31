# install on a raspberry pi
> sudo apt update -y  
> sudo apt-get upgrade -y  
> sudo apt-get install python3-pip -y  
> pip3 install poetry  
> PATH=$PATH:/home/pi/.local/bin  
> poetry install  
> sudo cp /home/pi/hyperdeck-timeremaining/*.service /lib/systemd/system/  
> sudo systemctl daemon-reload  
> pip3 install --upgrade requests  
> sudo systemctl enable hyperdeck-timeremaining.service  
> sudo systemctl start hyperdeck-timeremaining.service  
> sudo systemctl enable hyperdeck-telnetclient.service  
> sudo systemctl start hyperdeck-telnetclient.service  
  
> *consider enable overlay file system in raspi-config afterwards*
