import os
import time
import json
import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding


def _replace_unsupported_chars(some_str):
    """Replace unsupported chars: '+=/' with '-_~'"""
    return some_str.replace("+", "-") \
        .replace("=", "_") \
        .replace("/", "~")


def _in_an_hour():
    """Returns a UTC POSIX timestamp for one hour in the future"""
    return int(time.time()) + (60000*60)


def rsa_signer(message, key):
    """
    Based on https://boto3.readthedocs.io/en/latest/reference/services/cloudfront.html#examples
    """
    private_key = serialization.load_pem_private_key(
        key,
        password=None,
        backend=default_backend()
    )
    signer = private_key.signer(padding.PKCS1v15(), hashes.SHA1())
    signer.update(message)
    return signer.finalize()


def generate_policy_cookie(url):
    """Returns a tuple: (policy json, policy base64)"""

    policy_dict = {
        "Statement": [
            {
                "Resource": url,
                "Condition": {
                    "DateLessThan": {
                        "AWS:EpochTime": _in_an_hour()
                    }
                }
            }
        ]
    }

    # Using separators=(',', ':') removes seperator whitespace
    policy_json = json.dumps(policy_dict, separators=(",", ":"))

    policy_64 = str(base64.b64encode(policy_json.encode("utf-8")), "utf-8")
    policy_64 = _replace_unsupported_chars(policy_64)
    return policy_json, policy_64


def generate_signature(policy, key):
    """Creates a signature for the policy from the key, returning a string"""
    sig_bytes = rsa_signer(policy.encode("utf-8"), key)
    sig_64 = _replace_unsupported_chars(str(base64.b64encode(sig_bytes), "utf-8"))
    return sig_64


def generate_cookies(policy, signature, cloudfront_id):
    """Returns a dictionary for cookie values in the form 'COOKIE NAME': 'COOKIE VALUE'"""
    return {
        "CloudFront-Policy": policy,
        "CloudFront-Signature": signature,
        "CloudFront-Key-Pair-Id": cloudfront_id
    }


def generate_curl_cmd(url, cookies):
    """Generates a cURL command (use for testing)"""
    curl_cmd = "curl -v"
    for k, v in cookies.items():
        curl_cmd += " -H 'Cookie: {}={}'".format(k, v)
    curl_cmd += " {}".format(url)
    return curl_cmd


def generate_signed_cookies(url, cloudfront_id, key):
    policy_json, policy_64 = generate_policy_cookie(url)
    signature = generate_signature(policy_json, key)
    return generate_cookies(policy_64, signature, cloudfront_id)


def get_signed_cookie(url_folder, url_exact):
    if url_folder:
        url_folder = os.getenv("CF_BUCKET_URL") + url_folder
        url_exact = os.getenv("CF_BUCKET_URL") + url_exact
        cookies = generate_signed_cookies(url_folder, os.getenv("CF_KEY_PAIR"), os.getenv("CF_PEM_FILE").replace("\\n", "\n").encode())
        return generate_curl_cmd(url_exact, cookies)
