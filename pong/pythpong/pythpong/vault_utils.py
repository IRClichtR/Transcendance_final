import os
import hvac
from django.conf import settings

def get_secret_from_vault(secret_path):
	client = hvac.Client(
		url=settings.VAULT_ADDR,
		token=settings.VAULT_TOKEN
	)
	secret = client.secrets.kv.v2.read_secret_version(
		path=secret_path
	)
	return secret['data']['data']