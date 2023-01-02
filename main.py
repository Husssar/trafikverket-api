import argparse
import time
import requests
import keys
import logging

# keys.py should include
# KEY=yourkey
# TBSECRET=yourkey
# Else just proved the key via arguments


def xml_body_builder(key):
    xmlRequest = f"<REQUEST>" \
                 f"<LOGIN authenticationkey='{key}'/>" \
                 f"<QUERY objecttype='WeatherStation' schemaversion='1'>" \
                 f"<FILTER>" \
                 f"<AND>" \
                 f"<EQ name='CountyNo' value='13' />" \
                 f"<OR>" \
                 f"<EQ name='Name' value='Vrangelsro' />" \
                 f"</OR>" \
                 f"</AND>" \
                 f"</FILTER>" \
                 f"<INCLUDE>Active</INCLUDE>" \
                 f"<INCLUDE>CountyNo</INCLUDE>" \
                 f"<INCLUDE>Geometry.SWEREF99TM</INCLUDE>" \
                 f"<INCLUDE>Measurement</INCLUDE>" \
                 f"<INCLUDE>Name</INCLUDE>" \
                 f"<INCLUDE>RoadNumberNumeric</INCLUDE>" \
                 f"</QUERY>" \
                 f"</REQUEST>"

    return xmlRequest.replace('    ', '')


def get_data(key, url):
    logging.info(f"Collecting data from {url}")
    headers = {
        "Content-Type": "application/xml",
        'Accept': 'application/json',
    }
    data = xml_body_builder(key)

    try:
        response = requests.post(url=url, headers=headers, data=data)
        if response.status_code >= 300:
            raise Exception()
    except:
        logging.warning(f"Something went wrong in the post-reqeust to {url}, response was {response.status_code}")

    return response.json()


def push_tb(url, secret, data):
    logging.info(f"Pushing {data} to {url}")
    headers = {
        "Content-Type": "application/json",
        "Secret": secret,
        "Charset": "UTF-8"
    }
    try:
        response = requests.post(url=url,headers=headers, json=data)
        if response.status_code >= 300:
            raise Exception()
    except:
        logging.warning(f"Something went wrong in the post-reqeust to {url}, response was {response.status_code}")

def time_to_sleep(sleep_time):
    logging.info(f"Sleeping for {sleep_time}")
    time.sleep(sleep_time)


def run():
    logging.basicConfig(level=logging.INFO)
    logging.info('Started')

    parser = argparse.ArgumentParser()
    parser.add_argument("--key", required=False,
                        help="Need to have a key from trafikverket to use this script")
    parser.add_argument("--interval", default=500, type=int, required=False,
                        help="Interval on how often (s) it should push to Thingsboard, default 500s")
    parser.add_argument("--tburl", help="Thingsboard url", required=True)
    parser.add_argument("--tbsecret", help="Thingsboard url", required=False)
    parser.add_argument("--tvurl", default="https://api.trafikinfo.trafikverket.se/v2/data.json",
                        required=False,
                        help="Thingsboard url")

    args=parser.parse_args()
    measure_time_old = ''
    measure_time = 'empty'
    tbsecret = keys.TB
    key = keys.KEY
    
    if not key or not tbsecret:
        logging.warning("Missing keys for trafikverket or for thingsboard secret")

    logging.info("Starting application ...")

    if args.tbsecret:
        tbsecret = args.tbsecret
    if args.key:
        key = args.key

    while True:
        tv_data = get_data(key, args.tvurl)
        if 'MeasureTime' in tv_data:
            measure_time =tv_data['RESPONSE']['RESULT'][0]['WeatherStation'][0]['Measurement']['MeasureTime']

        # Only push if data is updated
        if measure_time != measure_time_old:
            push_tb(args.tburl, tbsecret, tv_data)
            measure_time_old = measure_time
        
        time_to_sleep(args.interval)

if __name__ == '__main__':
    run()
