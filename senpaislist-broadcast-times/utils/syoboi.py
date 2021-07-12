import xmltodict
import requests
from datetime import datetime

from typing import Dict, List

def get_jp_title_tid_dict() -> Dict[str, str]:
    xml_url = 'http://cal.syoboi.jp/db.php?Command=TitleLookup&TID=*&Fields=TID,Title'
    xml_response = requests.get(xml_url)
    xml_data = xmltodict.parse(xml_response.content)
    return { 
        item['Title'] : item['TID'] \
            for item in xml_data['TitleLookupResponse']['TitleItems']['TitleItem']
    }

def get_broadcast_times(tid: str) -> List[float]:
    prog_info_xml_url = 'http://cal.syoboi.jp/db.php?Command=ProgLookup&TID=' + tid
    prog_info_response = requests.get(prog_info_xml_url)
    prog_info = xmltodict.parse(prog_info_response.content)
    try:
        return [
            datetime.strptime(time['StTime'], '%Y-%m-%d %H:%M:%S').timestamp() \
                for time in prog_info['ProgLookupResponse']['ProgItems']['ProgItem']
        ]
    except:
        return []

# TODO: change the key to TID from MAL_ID
def get_season_broadcast_times(tid_malid_dict: List[str]) -> Dict[str, List[str]]:
    return {
        malid : get_broadcast_times(tid) \
            for tid, malid in tid_malid_dict.items() 
    }
