import random
import sys
import os
import glob

DIRS = ["mint", "thing", "cannon", "quince", "nation", "crack", "use", "aunt", "swim", "class", "sail", "fact"]

FILE_EXT = ['.DOC','.DOCX','.XLS','.XLSX','.PPT','.PPTX','.PST','.OST','.MSG','.EML','.VSD','.VSDX','.TXT','.CSV','.RTF','.WKS','.WK1','.PDF','.DWG','.ONETOC2','.SNT', '.JPEG','.JPG','.DOCB','.DOCM','.DOT','.DOTM','.DOTX','.XLSM','.XLSB','.XLW''.XLT','.XLM','.XLC','.XLTX','.XLTM','.PPTM','.POT','.PPS','.PPSM','.PPSX','.PPAM','.POTX','.POTM','.EDB','.HWP','.602','.SXI','.STI','.SLDX','.SLDM','.VDI', '.VMDK','.VMX','.GPG','.AES','.ARC','.PAQ','.BZ2','.TBK','.BAK','.TAR','.TGZ','.GZ','.7Z','.RAR','.ZIP','.BACKUP','.ISO','.VCD','.BMP','.PNG','.GIF','.RAW','.CGM','.TIF','.TIFF','.NEF','.PSD','.AI','.SVG','.DJVU','.M4U','.M3U','.MID','.WMA','.FLV','.3G2','.MKV','.3GP','.MP4','.MOV','.AVI','.ASF','.MPEG', '.VOB','.MPG','.WMV','.FLA','.SWF','.WAV','.MP3','.SH','.CLASS','.JAR','.JAVA','.RB','.ASP','.PHP','.JSP','.BRD','.SCH','.DCH','.DIP','.PL','.VB','.VBS','.PS1','.BAT','.CMD','.JS','.ASM','.H','.PAS','.CPP','.C','.CS','.SUO', '.SLN','.LDF','.MDF','.IBD','.MYI','.MYD','.FRM','.ODB','.DBF','.DB','.MDB', '.ACCDB','.SQL','.SQLITEDB','.SQLITE3','.ASC','.LAY6','.LAY','.MML','.SXM','.OTG','.ODG','.UOP','.STD','.SXD','.OTP','.ODP','.WB2','.SLK','.DIF','.STC','.SXC','.OTS','.ODS','.3DM','.MAX','.3DS','.UOT','.STW','.SXW','.OTT','.ODT''.PEM','.P12','.CSR','.CRT','.KEY','.PFX','.DER']

FILE_NAMES = ['college', 'wife', 'insurance', 'awareness', 'night', 'honey', 'engine', 'length', 'opinion', 'guidance', 'concept', 'dealer', 'enthusiasm', 'warning', 'beer', 'resource', 'flight', 'disaster', 'excitement', 'user', 'politics', 'revenue', 'possession', 'discussion', 'quality', 'tennis', 'poem', 'inflation', 'basis', 'connection', 'customer', 'secretary', 'diamond', 'lab', 'death', 'proposavl', 'engineering', 'goal', 'government', 'director', 'heart', 'art', 'restaurant', 'comparison', 'initiative', 'food', 'expression', 'member', 'psychology', 'priority']

SIZE = [1024, 1024*1024, 1024*1024*4 ]

DEPTH = random.randint(2,4)


def create_dir_structure(dir_path, depth):
    depth += 1
    if depth > DEPTH:
        return
    dir_num = random.randint(3,5)
    for dir_name in random.sample(DIRS, dir_num):
        new_dir = os.path.join(dir_path, dir_name)
        try:
            os.makedirs(new_dir)
        except FileExistsError:
            print("Directory already exists!")
        create_dir_structure(new_dir, depth)

def create_dummy_files(dir_path):
    files = []
    for item in glob.glob(dir_path + '/**', recursive=True):
        if os.path.isdir(item):
            for file_num in range(random.randint(1,6)):
                for file_name in random.sample(FILE_NAMES, file_num):
                    target = os.path.join(item,
                        "{}{}".format(file_name, random.sample(FILE_EXT, 1)[0]))
                    with open(target, "w") as f:
                        f.write("A"*random.sample(SIZE, 1)[0])
                    files.append(target)
        else:
            files.append(item)
    return files
    


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("[+]You need to provide path!")
        exit()

    create_dir_structure(sys.argv[1], 0)
    files = create_dummy_files(sys.argv[1])
    while True:
        try:
            print("Do you want to check create files?\nEnter 'y' to check or 'n' to exit:")
            answer = input()
            if "y" in answer:
                i = 0
                for f in files:
                    if not os.path.exists(f):
                        i += 1
                if i == 0:
                    print("All files are in place!")
                else:
                    print("Didn't found {} out from {}".format(i, len(files)))
            if "n" in answer:
                exit()
        except KeyboardInterrupt:
            break
