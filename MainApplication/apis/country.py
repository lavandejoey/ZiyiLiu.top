#!/usr/bin/env python
# apis/country.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = "Apache 2.0"
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

# standard library
import json
import logging
import os
from datetime import datetime

# 3rd party packages
from flask import jsonify, send_from_directory, request

# local source
from MainApplication.apis.base import apis_blueprint
from MainApplication.extentions import cache

# static/json
json_folder = "MainApplication/static/json"


@apis_blueprint.route('/countries', methods=['GET'])
@cache.memoize(timeout=7 * 24 * 60 * 60)  # 1 week in seconds
def get_all_countries() -> (jsonify, int):
    """
    Get information about a specific country including its flag URLs.
    :return: A response containing the status, list of countries with flag URLs, count, timestamp, and datetime.
    """
    # Load countries from JSON file
    with open(os.path.join(json_folder, "countries.json"), "r") as f:
        countries = json.load(f)
    with open(os.path.join(json_folder, "phone-code.json"), "r") as f:
        phone_codes = json.load(f)

    # Add flag URLs to the countries
    protocol = "https" if request.is_secure else "http"
    prefix = apis_blueprint.url_prefix
    for country_code in countries.keys():
        countries[country_code] = {
            "name": countries[country_code],
            "phoneCode": phone_codes[country_code],
            "flagUrls": {
                "png100px": f"{protocol}://{request.host}{prefix}/flag/png100px/{country_code.lower()}.png",
                "png250px": f"{protocol}://{request.host}{prefix}/flag/png250px/{country_code.lower()}.png",
                "png1000px": f"{protocol}://{request.host}{prefix}/flag/png1000px/{country_code.lower()}.png",
                "svg": f"{protocol}://{request.host}{prefix}/flag/svg/{country_code.lower()}.svg"
            }
        }

    return jsonify({"status": "success", "countries": countries, "count": len(countries),
                    "timestamp": datetime.utcnow().timestamp(), "datetime": datetime.utcnow().isoformat()}), 200


@apis_blueprint.route('/country/<string:identifier>', methods=['GET'])
def get_country_info(identifier) -> (jsonify, int):
    """
    Get country information based on the provided country code or name.
    :param identifier: The country code or name.
    :return: A response containing the status, country code, country name, flag URLs, timestamp, and datetime.
    """
    # Load countries from JSON file
    with open(os.path.join(json_folder, "countries.json"), "r") as f:
        countries = json.load(f)
    with open(os.path.join(json_folder, "phone-code.json"), "r") as f:
        phone_codes = json.load(f)

    # Check if the identifier is a country abbreviation
    if identifier in countries.keys():
        country_code = identifier
        country_name = countries[identifier]

    # Check if the identifier is a country name
    elif identifier in countries.values():
        country_code = list(countries.keys())[list(countries.values()).index(identifier)]
        country_name = identifier

    # If neither an abbreviation nor a name is found
    else:
        return jsonify({"status": "fail", "message": "Country code or name not found.",
                        "timestamp": datetime.utcnow().timestamp(), "datetime": datetime.utcnow().isoformat()}), 404

    # Generate flag URLs. The URLs are generated based on the current request host and protocol.
    protocol = "https" if request.is_secure else "http"
    prefix = apis_blueprint.url_prefix
    flag_urls = {
        "png100px": f"{protocol}://{request.host}{prefix}/flag/png100px/{country_code.lower()}.png",
        "png250px": f"{protocol}://{request.host}{prefix}/flag/png250px/{country_code.lower()}.png",
        "png1000px": f"{protocol}://{request.host}{prefix}/flag/png1000px/{country_code.lower()}.png",
        "svg": f"{protocol}://{request.host}{prefix}/flag/svg/{country_code.lower()}.svg"
    }

    return jsonify({"status": "success", "countryCode": country_code, "countryName": country_name,
                    "phoneCode": phone_codes[country_code], "flagUrls": flag_urls,
                    "timestamp": datetime.utcnow().timestamp(), "datetime": datetime.utcnow().isoformat()}), 200


@apis_blueprint.route('/flags/<path:image_path>', methods=['GET'])
@apis_blueprint.route('/flag/<path:image_path>', methods=['GET'])
def get_flag_images(image_path) -> (send_from_directory or jsonify, int):
    """
    Get country flag images based on the provided image path.
    :param image_path: The path to the country flag image.
    :return: The country flag image file.
    """
    # Check if the file path does not end with ".png" or ".svg"
    if not image_path.lower().endswith(('.png', '.svg')):
        return jsonify({"status": "fail", "message": "Invalid file format.",
                        "timestamp": datetime.utcnow().timestamp(), "datetime": datetime.utcnow().isoformat()}), 400

    # country flags image folders
    flag_root_folder = os.path.join("static", "node_modules", "svg-country-flags")
    # flag image folder
    flag_image_path = os.path.join("MainApplication", flag_root_folder, image_path)
    # Check if the file exists
    if os.path.isfile(flag_image_path):
        logging.debug(f"Flag image found: {flag_image_path}")
        return send_from_directory(flag_root_folder, image_path), 200
    else:
        logging.warning(f"Flag image not found: {flag_image_path}")
        return jsonify({"status": "fail", "message": "Flag image not found.",
                        "timestamp": datetime.utcnow().timestamp(), "datetime": datetime.utcnow().isoformat()}), 404
