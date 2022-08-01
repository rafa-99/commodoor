from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

from libs.io import write_to_file


def genkeys(bits=2048, private_key_path="private.pem", public_key_path="public.pem"):
	# Generating and exporting keys
	key = RSA.generate(bits)
	private = key.exportKey()
	public = key.public_key().exportKey()

	# Writing keys into a file
	write_to_file(private, private_key_path, 'wb')
	write_to_file(public, public_key_path, 'wb')


def encrypt_hybrid(text, public_pem, mode=AES.MODE_GCM, encoding="utf-8", block_size=16):
	# Importing public key
	public_key = RSA.import_key(open(public_pem).read())
	cipher_rsa = PKCS1_OAEP.new(public_key)

	# Generating AES Key and AES Encrypted Key
	aes_key = get_random_bytes(block_size)
	encrypted_aes_key = cipher_rsa.encrypt(aes_key)

	# Encrypting data with AES Key
	cipher_aes = AES.new(aes_key, mode)
	ciphertext, tag = cipher_aes.encrypt_and_digest(text.encode(encoding))

	return [encrypted_aes_key, cipher_aes.nonce, tag, ciphertext]


def encrypt(string, path, public_key, encoding="utf-8", block_size=16):
	data = encrypt_hybrid(string, public_key, encoding=encoding, block_size=block_size)

	for byte in data:
		write_to_file(byte, path, 'ab')


def decrypt_hybrid(encrypted, private_pem, mode=AES.MODE_GCM, encoding="utf-8"):
	# Importing private key
	private_key = RSA.import_key(open(private_pem).read())
	cipher_rsa = PKCS1_OAEP.new(private_key)

	# Loading AES Session Key information
	encrypted_aes_key, nonce, tag, ciphertext = [byte for byte in encrypted]

	# Importing decrypted AES Session key
	aes_key = cipher_rsa.decrypt(encrypted_aes_key)
	cipher_aes = AES.new(aes_key, mode, nonce)

	return cipher_aes.decrypt_and_verify(ciphertext, tag).decode(encoding)


def decrypt(path, private_pem, encoding="utf-8", block_size=16):

	data = []
	private_key = RSA.import_key(open(private_pem).read())

	file = open(path, "rb")

	for byte in (private_key.size_in_bytes(), block_size, block_size, -1):
		data.append(file.read(byte))

	file.close()

	return decrypt_hybrid(data, private_pem, encoding=encoding)
