import os
import requests
from dotenv import load_dotenv
from dataclasses import dataclass, asdict
from tabulate import tabulate

load_dotenv()

TOKEN = os.getenv("TOKEN")

class IPData:
    def __init__(self, ip_address: str, token: str) -> None: 
        self.ip_address:str = ip_address
        self._token:str = token
        self.data:dict = {}

    def get_data_from_ip_address(self) -> None:
        try:
            response = requests.get(f"https://ipinfo.io/{self.ip_address}?token={self._token}")
            response.raise_for_status()
            self.data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while getting IP information: {e}")

@dataclass(frozen=True)
class ParseIpInfo:
    city: str
    region: str
    country: str
    org: str
    loc: str

def main():
    ip_data = IPData(ip_address="8.8.8.8",token=TOKEN)
    ip_data.get_data_from_ip_address()

    relevant_fields = {key: value for key, value in ip_data.data.items() if key in ParseIpInfo.__annotations__}
    ip_info = ParseIpInfo(**relevant_fields)
    ip_info_dict = asdict(ip_info)
    ip_info_table = tabulate(ip_info_dict.items(), headers=["Column Name", "Value"], tablefmt="pipe")
    print(ip_info_table)

if __name__ == "__main__":
    main()
