import exifread
from datetime import datetime

DT_TAGS = ["Image DateTime", "EXIF DateTimeOriginal", "EXIF DateTimeDigitized", "DateTime"]

def degree_to_int(degree):
    degree = str(degree)
    deg, min, sec = degree.split(',')
    deg = int(deg)
    min = int(min)
    sec1, sec2 = sec.split('/')

    sec = float(float(sec1)/float(sec2))

    return float(deg + float(min/60) + float(sec/3600))

def get_metadata(images_url):
    f = open(str(images_url),'rb')
    ret = {}
    dt_value = None
    ret['processed'] = False
    try:
        tags = exifread.process_file(f)
        ret['processed'] = True

        # for dt_tag in DT_TAGS:
        #     try:
        #         dt_value = '%s'%tags[dt_tag]
        #     except:
        #         continue

        latitude = '%s'%tags['GPS GPSLatitude']
        latitude = latitude.strip('[]')
        latitude = degree_to_int(latitude)
        # print(latitude)
        ret['lintang'] = latitude

        longitude = '%s'%tags['GPS GPSLongitude']
        longitude = longitude.strip('[]')
        longitude = degree_to_int(longitude)
        # print(longitude)
        ret['bujur'] = longitude
    except:
        return False
    finally:
        f.close()

    return ret