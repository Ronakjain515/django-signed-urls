import os
from datetime import datetime, timedelta
from botocore.signers import CloudFrontSigner
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding


class ResponseInfo(object):
    """
    Class for setting how API should send response.
    """
    def __init__(self, **args):
        self.response = {
            "status_code": args.get('status', 200),
            "error": args.get('error', None),
            "data": args.get('data', []),
            "message": [args.get('message', 'Success')]
        }


def rsa_signer(message):
    key_data = os.getenv("CF_PEM_FILE").replace("\\n", "\n").encode()
    private_key = serialization.load_pem_private_key(
        key_data,
        password=None,
        backend=default_backend()
    )
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())


def get_pre_signed_url(object_name):
    if object_name:
        key_id = os.getenv("CF_KEY_PAIR")
        print(key_id)
        url = os.getenv("CF_BUCKET_URL") + object_name
        expire_date = datetime.now() + timedelta(minutes=5)

        cloud_front_signer = CloudFrontSigner(key_id, rsa_signer)

        # Create a signed url that will be valid until the specific expiry date
        # provided using a canned policy.
        # noinspection PyTypeChecker
        signed_url = cloud_front_signer.generate_presigned_url(url, date_less_than=expire_date)
        return signed_url
    return None
