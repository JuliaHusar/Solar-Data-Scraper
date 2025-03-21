import os
import sys
import argparse
import logging
import requests
from dotenv import load_dotenv

load_dotenv('api_keys.env')

param_values = {
    "system_size": "system_capacity",
    "module_type": "module_type",
    "array_type": "array_type",
    "system_losses": "losses",
    "azimuth": "azimuth",
    "tilt": "tilt",
}

array_type = [
    "Fixed_Open_Rack",
    "Fixed_Roof_Mount",
    "1-Axis_Tracking",
    "1-Axis_Backtracking",
    "2-Axis_Tracking"
]

module_type =[
    "Standard",
    "Premium",
    "Thin_Film"
]

api_key = os.getenv("API_KEY")


def main():
    args = parse_args()
    get_data(args)


def get_data(args):
    base_url = "https://developer.nrel.gov/api/pvwatts/v8.json?api_key=" + str(api_key)
    for arg, value in vars(args).items():

        match arg:
            case "latlot":
                base_url += f"&lat={value[0]}&lon={value[1]}"
            case "array_type":
                index = array_type.index(value)
                base_url += f"&array_type={index}"
            case "module_type":
                index = module_type.index(value)
                base_url += f"&module_type={index}"
            case _:
                param = param_values.get(arg)
                if param:
                    base_url += f"&{param}={value}"
    print(base_url)


def parse_args():
    parser = argparse.ArgumentParser(description="Use to retrieve solar data based on specific parameters")
    parser.add_argument(
        "--debug",
        help="Display debugging information.",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )
    parser.add_argument(
        "--system_size",
        "-ss",
        type=int,
        help="Select System Size in KW",
        default=4
    ),
    parser.add_argument(
        "--module_type",
        "-m",
        type=str,
        help="Standard, Premium, or Thin_Film",
        default="Standard"
    ),
    parser.add_argument(
        "--array_type",
        "-a",
        type=str,
        help="Fixed_Open_Rack, Fixed_Roof_Mount, 1-Axis_Tracking, 1-Axis_Backtracking, 2-Axis_Tracking",
        default="Fixed_Open_Rack"
    ),
    parser.add_argument(
        "--system_losses",
        "-sl",
        type=float,
        help="Enter Decimal Value",
        default=14.08
    ),
    parser.add_argument(
        "--tilt",
        "-t",
        type=int,
        help="Tilt in degrees, whole integers",
        default=20
    ),
    parser.add_argument(
        "--azimuth",
        "-z",
        help="Azimuth in degrees, whole integers",
        type=int,
        default=180
    ),
    parser.add_argument(
        "--latlot",
        "-l",
        type=str,
        help="Location as latitude and longitude",
        nargs=2,
        default=["35.2271", "-80.8431"]  # Example default values for Charlotte, NC
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    return args


if __name__ == "__main__":
    main()
