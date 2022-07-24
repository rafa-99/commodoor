from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

from libs.io import write_to_file


def genkeys(bits=4096, private_key_path="private.pem", public_key_path="public.pem"):
	key = RSA.generate(bits)
	private = key.exportKey()
	public = key.public_key().exportKey()

	write_to_file(private, private_key_path, 'wb')
	write_to_file(public, public_key_path, 'wb')


def encrypt(text, public_pem, encoding="utf-8", block_size=16):
	# Importing public key
	public_key = RSA.import_key(open(public_pem).read())
	cipher_rsa = PKCS1_OAEP.new(public_key)

	# Generating AES Key and AES Encrypted Key
	aes_key = get_random_bytes(block_size)
	encrypted_aes_key = cipher_rsa.encrypt(aes_key)

	# Encrypting data with AES Key
	cipher_aes = AES.new(aes_key, AES.MODE_EAX)
	ciphertext, tag = cipher_aes.encrypt_and_digest(text.encode(encoding))

	return [encrypted_aes_key, cipher_aes.nonce, tag, ciphertext]


def decrypt(encrypted, private_pem, encoding="utf-8"):
	# Importing private key
	private_key = RSA.import_key(open(private_pem).read())
	cipher_rsa = PKCS1_OAEP.new(private_key)

	# Loading AES Session Key information
	encrypted_aes_key = encrypted[0]
	nonce = encrypted[1]
	tag = encrypted[2]
	ciphertext = encrypted[3]

	# Importing decrypted AES Session key
	aes_key = cipher_rsa.decrypt(encrypted_aes_key)
	cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce)

	return cipher_aes.decrypt_and_verify(ciphertext, tag).decode(encoding)
