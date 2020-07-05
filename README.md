# blackraven
Ransomware prevention tool for Linux

## Prerequisites
To run this tool make sure you have **python3** and auditd:<br />
```apt-get install auditd audispd-plugins```

To generate random files and folders within the path use following command:<br />
```dummy_files_generator.py <path>```

## Usage
```sudo python3 blackraven.py /home```<br />

To monitor multiple folders use following command:<br />
```sudo python3 blackraven.py /boot,/usr/bin,/home```
