Instruction:

1. Activate service for auto run program when boot up PI
    Read through main.py file to update and edit path of font or URL of web service, the comments in details.
    Edit line 6 => change to your absoulte path of main.py file
    copy file: "epson_printer.service" into /lib/systemd/system by sudo 
    ex: $ sudo cp epson_printer.service /lib/systemd/system/
2. Tell systemd recognize our service
    $ sudo systemctl daemon-reload
3. Tell systemd that we want our service to start on boot
    $ sudo systemctl enable epson_printer.service
4. Reboot your PI and test
== after reboot and start-up PI===
5. Check status of epson_printer service
   $ sudo systemctl status epson_printer.service

6. Stop epson_printer service if you want
  $ sudo systemctl stop epson_printer.service

Note before running:
Install library needed for running by command:
 $ pin install -r requirements.txt

Contact: Tony Do 
Email: dvhbkhn@gmail.com

