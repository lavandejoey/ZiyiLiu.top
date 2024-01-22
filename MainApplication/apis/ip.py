#!/usr/bin/env python
# apis/ip.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = "Apache 2.0"
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

# standard library
import logging

# 3rd party packages
from flask import blueprints, request, current_app, redirect

# Define a language mapping or fallback mechanism
LANGUAGE_MAPPING = {
    "zh_Hans": ["zh", "zh_Hans_HK", "zh_Hans_MO", "zh_Hans_SG"],
    "yue": ["yue_Hant", "yue_Hant_HK", "yue_Hantyue_MO", "zh_Hant", "zh_Hant_HK", "zh_Hant_MO", "zh_Hant_TW", "zh_HK"],
    "fr": ["fr_BE", "fr_BF", "fr_BI", "fr_BJ", "fr_BL", "fr_CA", "fr_CD", "fr_CF", "fr_CG", "fr_CH", "fr_CI", "fr_CM",
           "fr_DJ", "fr_DZ", "fr_FR", "fr_GA", "fr_GF", "fr_GN", "fr_GP", "fr_GQ", "fr_HT", "fr_KM", "fr_LU", "fr_MA",
           "fr_MC", "fr_MF", "fr_MG", "fr_ML", "fr_MQ", "fr_MR", "fr_MU", "fr_NC", "fr_NE", "fr_PF", "fr_PM", "fr_RE",
           "fr_RW", "fr_SC", "fr_SN", "fr_SY", "fr_TD", "fr_TG", "fr_TN", "fr_VU", "fr_WF", "fr_YT"],
    "en": ["en_001", "en_150", "en_AG", "en_AI", "en_AS", "en_AT", "en_AU", "en_BB", "en_BE", "en_BI", "en_BM",
           "en_BS", "en_BW", "en_BZ", "en_CA", "en_CC", "en_CH", "en_CK", "en_CM", "en_CX", "en_CY", "en_DE", "en_DG",
           "en_DK", "en_DM", "en_ER", "en_FI", "en_FJ", "en_FK", "en_FM", "en_GB", "en_GD", "en_GG", "en_GH", "en_GI",
           "en_GM", "en_GU", "en_GY", "en_HK", "en_IE", "en_IL", "en_IM", "en_IN", "en_IO", "en_JE", "en_JM", "en_KE",
           "en_KI", "en_KN", "en_KY", "en_LC", "en_LR", "en_LS", "en_MG", "en_MH", "en_MO", "en_MP", "en_MS", "en_MT",
           "en_MU", "en_MW", "en_MY", "en_NA", "en_NF", "en_NG", "en_NL", "en_NR", "en_NU", "en_NZ", "en_PG", "en_PH",
           "en_PK", "en_PN", "en_PR", "en_PW", "en_RW", "en_SB", "en_SC", "en_SD", "en_SE", "en_SG", "en_SH", "en_SI",
           "en_SL", "en_SS", "en_SX", "en_SZ", "en_TC", "en_TK", "en_TO", "en_TT", "en_TV", "en_TZ", "en_UG", "en_UM",
           "en_US", "en_USyue_POSIX", "en_VC", "en_VG", "en_VI", "en_VU", "en_WS", "en_ZA", "en_ZM", "en_ZW"],
}

ip_blueprint = blueprints.Blueprint(name="ip", import_name=__name__, static_folder="static", static_url_path="/static",
                                    template_folder="templates", url_prefix="/", subdomain=None, url_defaults=None,
                                    cli_group=None)


def get_client_ip() -> str:
    """
    Get the client's IP address, considering proxy headers.
    :return: client's IP address
    """
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_ip = request.remote_addr
    return client_ip


def get_client_timezone() -> str:
    """
    Get the client's timezone.
    :return: client's timezone
    """
    return request.headers.get("Time-Zone")


def get_client_locale() -> str:
    """
    Get the client's locale.
    :return: client's locale
    """
    locale = request.cookies.get('locale')
    logging.debug("The current locale is: %s" % locale)

    # Check if the provided locale is in the list of supported languages
    if locale in current_app.config.get('LANGUAGES'):
        return locale

    # Check if the provided locale is in the language mapping
    for main_language, related_languages in LANGUAGE_MAPPING.items():
        if locale in related_languages:
            return main_language

    # If no matching language is found, use the default locale
    return request.accept_languages.best_match(current_app.config.get('BABEL_DEFAULT_LOCALE')) or 'en'


@ip_blueprint.route('/set-locale/<language>')
def set_client_locale(language):
    """
    Set the client's preferred language by storing it in a cookie.
    Redirect the user back to the previous page.
    :param language: the language to set
    :return: redirect to the previous page
    """
    response = redirect(request.referrer)
    if language:
        # Store the language in a cookie that is valid for 30 days
        response.set_cookie('locale', language, max_age=30 * 24 * 60 * 60)
    return response
