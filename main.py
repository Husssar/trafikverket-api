import argparse
import sys
import time
import requests


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


def get_data(arguments):
    headers = {
        "Content-Type": "application/xml",
        'Accept': 'application/json',
    }
    data = xml_body_builder(arguments.key)

    try:
        response = requests.post(url=arguments.tvurl, headers=headers, data=data)
    except:
        print(f"Something went wrong in the post-reqeust to {arguments.tvurl}, response was {response.status_code}")

    return response.json()


def push_tb(url, secret, data):
    headers = {
        "Content-Type": "application/json",
        "Secret": secret,
        "Charset": "UTF-8"
    }
    try:
        response = requests.post(url=url,headers=headers, json=data)
    except:
        print(f"Something went wrong in the post-reqeust to {url}, response was {response.status_code}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", required=True,
                        help="Need to have a key from trafikverket to use this script")
    parser.add_argument("--interval", default=500, type=int, required=True,
                        help="Interval on how often (s) it should push to Thingsboard, default 500s")
    parser.add_argument("--tburl", help="Thingsboard url", required=True)
    parser.add_argument("--tbsecret", help="Thingsboard url", required=True)
    parser.add_argument("--tvurl", default="https://api.trafikinfo.trafikverket.se/v2/data.json",
                        required=False,
                        help="Thingsboard url")

    args=parser.parse_args()
    measure_time_old = ''

    print("Starting application. Args was supplied to application.")
    print("")
    while True:
        tv_data = get_data(args)
        measure_time =tv_data['RESPONSE']['RESULT'][0]['WeatherStation'][0]['Measurement']['MeasureTime']

        # Only push if data us updated
        if measure_time != measure_time_old:
            push_tb(args.tburl, args.tbsecret, tv_data)
            measure_time_old = measure_time

        time.sleep(args.interval)

main()
