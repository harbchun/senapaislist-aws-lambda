import xmltodict
import requests
from typing import Dict

def get_jp_title_tid_dict() -> Dict[str : str]:
    xml_url = 'http://cal.syoboi.jp/db.php?Command=TitleLookup&TID=*&Fields=TID,Title'
    xml_response = requests.get(xml_url)
    xml_data = xmltodict.parse(xml_response.content)
    return { item['Title'] : item['TID'] for item in xml_data['TitleLookupResponse']['TitleItems']['TitleItem'] }