# Vault Structure has been taken from mimikatz
from ctypes.wintypes import *
from ctypes import *

import sys
import os

try:
	import _winreg as winreg
except ImportError:
	import winreg

LPTSTR = LPSTR
LPCTSTR = LPSTR
PHANDLE = POINTER(HANDLE)
HANDLE = LPVOID
LPDWORD = POINTER(DWORD)
PVOID = c_void_p
INVALID_HANDLE_VALUE = c_void_p(-1).value
NTSTATUS = ULONG()
PWSTR = c_wchar_p
LPWSTR = c_wchar_p
PBYTE = POINTER(BYTE)
LPBYTE = POINTER(BYTE)
PSID = PVOID
LONG = c_long
WORD = c_uint16

# #############################- Constants ##############################

# Credential Manager
CRYPTPROTECT_UI_FORBIDDEN = 0x01
CRED_TYPE_GENERIC = 0x1
CRED_TYPE_DOMAIN_VISIBLE_PASSWORD = 0x4

# Regedit
HKEY_CURRENT_USER = -2147483647
HKEY_LOCAL_MACHINE = -2147483646
KEY_READ = 131097
KEY_ENUMERATE_SUB_KEYS = 8
KEY_QUERY_VALUE = 1

# custom key to read registry (not from msdn)
ACCESS_READ = KEY_READ | KEY_ENUMERATE_SUB_KEYS | KEY_QUERY_VALUE

# Token manipulation
PROCESS_QUERY_INFORMATION = 0x0400
STANDARD_RIGHTS_REQUIRED = 0x000F0000
READ_CONTROL = 0x00020000
STANDARD_RIGHTS_READ = READ_CONTROL
TOKEN_ASSIGN_PRIMARY = 0x0001
TOKEN_DUPLICATE = 0x0002
TOKEN_IMPERSONATE = 0x0004
TOKEN_QUERY = 0x0008
TOKEN_QUERY_SOURCE = 0x0010
TOKEN_ADJUST_PRIVILEGES = 0x0020
TOKEN_ADJUST_GROUPS = 0x0040
TOKEN_ADJUST_DEFAULT = 0x0080
TOKEN_ADJUST_SESSIONID = 0x0100
TOKEN_READ = (STANDARD_RIGHTS_READ | TOKEN_QUERY)
tokenprivs = (
		TOKEN_QUERY | TOKEN_READ | TOKEN_IMPERSONATE | TOKEN_QUERY_SOURCE | TOKEN_DUPLICATE | TOKEN_ASSIGN_PRIMARY | (
		131072 | 4))
TOKEN_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED | TOKEN_ASSIGN_PRIMARY |
					TOKEN_DUPLICATE | TOKEN_IMPERSONATE | TOKEN_QUERY | TOKEN_QUERY_SOURCE |
					TOKEN_ADJUST_PRIVILEGES | TOKEN_ADJUST_GROUPS | TOKEN_ADJUST_DEFAULT |
					TOKEN_ADJUST_SESSIONID)

SE_DEBUG_PRIVILEGE = 20


# ############################# Structures ##############################

class CREDENTIAL_ATTRIBUTE(Structure):
	_fields_ = [
		('Keyword', LPSTR),
		('Flags', DWORD),
		('ValueSize', DWORD),
		('Value', LPBYTE)
	]


PCREDENTIAL_ATTRIBUTE = POINTER(CREDENTIAL_ATTRIBUTE)


class CREDENTIAL(Structure):
	_fields_ = [
		('Flags', DWORD),
		('Type', DWORD),
		('TargetName', LPSTR),
		('Comment', LPSTR),
		('LastWritten', FILETIME),
		('CredentialBlobSize', DWORD),
		# ('CredentialBlob', POINTER(BYTE)),
		('CredentialBlob', POINTER(c_char)),
		('Persist', DWORD),
		('AttributeCount', DWORD),
		('Attributes', PCREDENTIAL_ATTRIBUTE),
		('TargetAlias', LPSTR),
		('UserName', LPSTR)
	]


PCREDENTIAL = POINTER(CREDENTIAL)


class DATA_BLOB(Structure):
	_fields_ = [
		('cbData', DWORD),
		('pbData', POINTER(c_char))
	]


class GUID(Structure):
	_fields_ = [
		("data1", DWORD),
		("data2", WORD),
		("data3", WORD),
		("data4", BYTE * 6)
	]


LPGUID = POINTER(GUID)


class VAULT_CREDENTIAL_ATTRIBUTEW(Structure):
	_fields_ = [
		('keyword', LPWSTR),
		('flags', DWORD),
		('badAlign', DWORD),
		('valueSize', DWORD),
		('value', LPBYTE),
	]


PVAULT_CREDENTIAL_ATTRIBUTEW = POINTER(VAULT_CREDENTIAL_ATTRIBUTEW)


class VAULT_BYTE_BUFFER(Structure):
	_fields_ = [
		('length', DWORD),
		('value', PBYTE),
	]


class DATA(Structure):
	_fields_ = [
		# ('boolean',       BOOL),
		# ('short',             SHORT),
		# ('unsignedShort',     WORD),
		# ('int',           LONG),
		# ('unsignedInt',   ULONG),
		# ('double',            DOUBLE),
		('guid', GUID),
		('string', LPWSTR),
		('byteArray', VAULT_BYTE_BUFFER),
		('protectedArray', VAULT_BYTE_BUFFER),
		('attribute', PVAULT_CREDENTIAL_ATTRIBUTEW),
		# ('Sid',           PSID)
		('sid', DWORD)
	]


class Flag(Structure):
	_fields_ = [
		('0x00', DWORD),
		('0x01', DWORD),
		('0x02', DWORD),
		('0x03', DWORD),
		('0x04', DWORD),
		('0x05', DWORD),
		('0x06', DWORD),
		('0x07', DWORD),
		('0x08', DWORD),
		('0x09', DWORD),
		('0x0a', DWORD),
		('0x0b', DWORD),
		('0x0c', DWORD),
		('0x0d', DWORD)
	]


class VAULT_ITEM_DATA(Structure):
	_fields_ = [
		# ('schemaElementId',   DWORD),
		# ('unk0',              DWORD),
		# ('Type',              DWORD),
		# ('unk1',              DWORD),
		('data', DATA),
	]


PVAULT_ITEM_DATA = POINTER(VAULT_ITEM_DATA)


# From https://github.com/gentilkiwi/mimikatz/blob/b008188f9fe5668b5dae80c210290c7efa872ffa/mimikatz/modules/kuhl_m_vault.h#L157
class VAULT_ITEM_WIN8(Structure):
	_fields_ = [
		('id', GUID),
		('pName', PWSTR),
		('pResource', PVAULT_ITEM_DATA),
		('pUsername', PVAULT_ITEM_DATA),
		('pPassword', PVAULT_ITEM_DATA),
		('pPackageSid', PVAULT_ITEM_DATA),
		('LastWritten', FILETIME),
		('Flags', DWORD),
		('cbProperties', DWORD),
		('Properties', PVAULT_ITEM_DATA),
	]


PVAULT_ITEM_WIN8 = POINTER(VAULT_ITEM_WIN8)


# From https://github.com/gentilkiwi/mimikatz/blob/b008188f9fe5668b5dae80c210290c7efa872ffa/mimikatz/modules/kuhl_m_vault.h#L145
class VAULT_ITEM_WIN7(Structure):
	_fields_ = [
		('id', GUID),
		('pName', PWSTR),
		('pResource', PVAULT_ITEM_DATA),
		('pUsername', PVAULT_ITEM_DATA),
		('pPassword', PVAULT_ITEM_DATA),
		('LastWritten', FILETIME),
		('Flags', DWORD),
		('cbProperties', DWORD),
		('Properties', PVAULT_ITEM_DATA),
	]


PVAULT_ITEM_WIN7 = POINTER(VAULT_ITEM_WIN7)


class OSVERSIONINFOEXW(Structure):
	_fields_ = [
		('dwOSVersionInfoSize', c_ulong),
		('dwMajorVersion', c_ulong),
		('dwMinorVersion', c_ulong),
		('dwBuildNumber', c_ulong),
		('dwPlatformId', c_ulong),
		('szCSDVersion', c_wchar * 128),
		('wServicePackMajor', c_ushort),
		('wServicePackMinor', c_ushort),
		('wSuiteMask', c_ushort),
		('wProductType', c_byte),
		('wReserved', c_byte)
	]


class CRYPTPROTECT_PROMPTSTRUCT(Structure):
	_fields_ = [
		('cbSize', DWORD),
		('dwPromptFlags', DWORD),
		('hwndApp', HWND),
		('szPrompt', LPCWSTR),
	]


PCRYPTPROTECT_PROMPTSTRUCT = POINTER(CRYPTPROTECT_PROMPTSTRUCT)


class LUID(Structure):
	_fields_ = [
		("LowPart", DWORD),
		("HighPart", LONG),
	]


PLUID = POINTER(LUID)


class SID_AND_ATTRIBUTES(Structure):
	_fields_ = [
		("Sid", PSID),
		("Attributes", DWORD),
	]


class TOKEN_USER(Structure):
	_fields_ = [
		("User", SID_AND_ATTRIBUTES), ]


class LUID_AND_ATTRIBUTES(Structure):
	_fields_ = [
		("Luid", LUID),
		("Attributes", DWORD),
	]


class TOKEN_PRIVILEGES(Structure):
	_fields_ = [
		("PrivilegeCount", DWORD),
		("Privileges", LUID_AND_ATTRIBUTES),
	]


PTOKEN_PRIVILEGES = POINTER(TOKEN_PRIVILEGES)


class SECURITY_ATTRIBUTES(Structure):
	_fields_ = [
		("nLength", DWORD),
		("lpSecurityDescriptor", LPVOID),
		("bInheritHandle", BOOL),
	]


PSECURITY_ATTRIBUTES = POINTER(SECURITY_ATTRIBUTES)


class SID_NAME_USE(DWORD):
	_sid_types = dict(enumerate('''
        User Group Domain Alias WellKnownGroup DeletedAccount
        Invalid Unknown Computer Label'''.split(), 1))

	def __init__(self, value=None):
		if value is not None:
			if value not in self.sid_types:
				raise ValueError('invalid SID type')
			DWORD.__init__(value)

	def __str__(self):
		if self.value not in self._sid_types:
			raise ValueError('invalid SID type')
		return self._sid_types[self.value]

	def __repr__(self):
		return 'SID_NAME_USE(%s)' % self.value


PSID_NAME_USE = POINTER(SID_NAME_USE)

# ############################# Load dlls ##############################

advapi32 = WinDLL('advapi32', use_last_error=True)
crypt32 = WinDLL('crypt32', use_last_error=True)
kernel32 = WinDLL('kernel32', use_last_error=True)
psapi = WinDLL('psapi', use_last_error=True)
ntdll = WinDLL('ntdll', use_last_error=True)

# ############################# Functions ##############################

RevertToSelf = advapi32.RevertToSelf
RevertToSelf.restype = BOOL
RevertToSelf.argtypes = []

ImpersonateLoggedOnUser = advapi32.ImpersonateLoggedOnUser
ImpersonateLoggedOnUser.restype = BOOL
ImpersonateLoggedOnUser.argtypes = [HANDLE]

DuplicateTokenEx = advapi32.DuplicateTokenEx
DuplicateTokenEx.restype = BOOL
DuplicateTokenEx.argtypes = [HANDLE, DWORD, PSECURITY_ATTRIBUTES, DWORD, DWORD, POINTER(HANDLE)]

AdjustTokenPrivileges = advapi32.AdjustTokenPrivileges
AdjustTokenPrivileges.restype = BOOL
AdjustTokenPrivileges.argtypes = [HANDLE, BOOL, PTOKEN_PRIVILEGES, DWORD, PTOKEN_PRIVILEGES, POINTER(DWORD)]

LookupPrivilegeValueA = advapi32.LookupPrivilegeValueA
LookupPrivilegeValueA.restype = BOOL
LookupPrivilegeValueA.argtypes = [LPCTSTR, LPCTSTR, PLUID]

ConvertSidToStringSid = advapi32.ConvertSidToStringSidW
ConvertSidToStringSid.restype = BOOL
ConvertSidToStringSid.argtypes = [DWORD, POINTER(LPWSTR)]

LookupAccountSid = advapi32.LookupAccountSidW
LookupAccountSid.restype = BOOL
LookupAccountSid.argtypes = [LPCWSTR, PSID, LPCWSTR, LPDWORD, LPCWSTR, LPDWORD, PSID_NAME_USE]

LocalAlloc = kernel32.LocalAlloc
LocalAlloc.restype = HANDLE
LocalAlloc.argtypes = [PSID, DWORD]

GetTokenInformation = advapi32.GetTokenInformation
GetTokenInformation.restype = BOOL
GetTokenInformation.argtypes = [HANDLE, DWORD, LPVOID, DWORD, POINTER(DWORD)]

OpenProcess = kernel32.OpenProcess
OpenProcess.restype = HANDLE
OpenProcess.argtypes = [DWORD, BOOL, DWORD]

OpenProcessToken = advapi32.OpenProcessToken
OpenProcessToken.restype = BOOL
OpenProcessToken.argtypes = [HANDLE, DWORD, POINTER(HANDLE)]

CloseHandle = kernel32.CloseHandle
CloseHandle.restype = BOOL
CloseHandle.argtypes = [HANDLE]

CredEnumerate = advapi32.CredEnumerateA
CredEnumerate.restype = BOOL
CredEnumerate.argtypes = [LPCTSTR, DWORD, POINTER(DWORD), POINTER(POINTER(PCREDENTIAL))]

CredFree = advapi32.CredFree
CredFree.restype = PVOID
CredFree.argtypes = [PVOID]

LocalFree = kernel32.LocalFree
LocalFree.restype = HANDLE
LocalFree.argtypes = [HANDLE]

CryptUnprotectData = crypt32.CryptUnprotectData
CryptUnprotectData.restype = BOOL
CryptUnprotectData.argtypes = [POINTER(DATA_BLOB), POINTER(LPWSTR), POINTER(DATA_BLOB), PVOID,
							   PCRYPTPROTECT_PROMPTSTRUCT, DWORD, POINTER(DATA_BLOB)]

# these functions do not exist on XP workstations
try:
	prototype = WINFUNCTYPE(ULONG, DWORD, LPDWORD, POINTER(LPGUID))
	vaultEnumerateVaults = prototype(("VaultEnumerateVaults", windll.vaultcli))

	prototype = WINFUNCTYPE(ULONG, LPGUID, DWORD, HANDLE)
	vaultOpenVault = prototype(("VaultOpenVault", windll.vaultcli))

	prototype = WINFUNCTYPE(ULONG, HANDLE, DWORD, LPDWORD, POINTER(c_char_p))
	vaultEnumerateItems = prototype(("VaultEnumerateItems", windll.vaultcli))

	prototype = WINFUNCTYPE(ULONG, HANDLE, LPGUID, PVAULT_ITEM_DATA, PVAULT_ITEM_DATA, PVAULT_ITEM_DATA, HWND, DWORD,
							POINTER(PVAULT_ITEM_WIN8))
	vaultGetItem8 = prototype(("VaultGetItem", windll.vaultcli))

	prototype = WINFUNCTYPE(ULONG, HANDLE, LPGUID, PVAULT_ITEM_DATA, PVAULT_ITEM_DATA, HWND, DWORD,
							POINTER(PVAULT_ITEM_WIN7))
	vaultGetItem7 = prototype(("VaultGetItem", windll.vaultcli))

	prototype = WINFUNCTYPE(ULONG, LPVOID)
	vaultFree = prototype(("VaultFree", windll.vaultcli))

	prototype = WINFUNCTYPE(ULONG, PHANDLE)
	vaultCloseVault = prototype(("VaultCloseVault", windll.vaultcli))


except Exception:
	pass

GetModuleFileNameEx = psapi.GetModuleFileNameExW
GetModuleFileNameEx.restype = DWORD
GetModuleFileNameEx.argtypes = [HANDLE, HMODULE, LPWSTR, DWORD]

# ############################# Custom functions ##############################


python_version = 2
if sys.version_info[0]:
	python_version = sys.version_info[0]


def isx64machine():
	archi = os.environ.get("PROCESSOR_ARCHITEW6432", '')
	if '64' in archi:
		return True

	archi = os.environ.get("PROCESSOR_ARCHITECTURE", '')
	if '64' in archi:
		return True

	return False


def OpenKey(key, path, index=0, access=KEY_READ):
	if isx64:
		return winreg.OpenKey(key, path, index, access | winreg.KEY_WOW64_64KEY)
	else:
		return winreg.OpenKey(key, path, index, access)


isx64 = isx64machine()


def getData(blobOut):
	cbData = blobOut.cbData
	pbData = blobOut.pbData
	buffer = create_string_buffer(cbData)
	memmove(buffer, pbData, sizeof(buffer))
	LocalFree(pbData);
	return buffer.raw


def Win32CryptUnprotectData(cipherText, entropy=False, is_current_user=True, user_dpapi=False):
	decrypted = None

	if is_current_user:
		bufferIn = c_buffer(cipherText, len(cipherText))
		blobIn = DATA_BLOB(len(cipherText), bufferIn)
		blobOut = DATA_BLOB()

		if entropy:
			bufferEntropy = c_buffer(entropy, len(entropy))
			blobEntropy = DATA_BLOB(len(entropy), bufferEntropy)

			if CryptUnprotectData(byref(blobIn), None, byref(blobEntropy), None, None, 0, byref(blobOut)):
				decrypted = getData(blobOut)

		else:
			if CryptUnprotectData(byref(blobIn), None, None, None, None, 0, byref(blobOut)):
				decrypted = getData(blobOut)

	if not decrypted:
		can_decrypt = True
		if not (user_dpapi and user_dpapi.unlocked):
			from libs.windows.dpapi_structure import are_masterkeys_retrieved
			can_decrypt = are_masterkeys_retrieved()

		if can_decrypt:
			try:
				decrypted = user_dpapi.decrypt_encrypted_blob(cipherText)
			except:
				# The encrypted blob cannot be parsed - weird (could happen with chrome v80)
				return None
			if decrypted is False:
				decrypted = None
		else:
			# raise ValueError('MasterKeys not found')
			pass

	if not decrypted:
		if not user_dpapi:
			# raise ValueError('DPApi unavailable')
			pass
		elif not user_dpapi.unlocked:
			# raise ValueError('DPApi locked')
			pass

	return decrypted


def get_os_version():
	"""
    return major anr minor version
    https://msdn.microsoft.com/en-us/library/windows/desktop/ms724832(v=vs.85).aspx
    """
	os_version = OSVERSIONINFOEXW()
	os_version.dwOSVersionInfoSize = sizeof(os_version)
	retcode = windll.Ntdll.RtlGetVersion(byref(os_version))
	if retcode != 0:
		return False

	return '%s.%s' % (str(os_version.dwMajorVersion.real), str(os_version.dwMinorVersion.real))


def get_vault_objects_for_this_version_of_windows():
	"""
        @return: Tuple[
                        Type of vault item,
                        Pointer to type of vault item,
                        VaultGetItem function as Callable[[vault_handle, vault_item_prt, password_vault_item_ptr], int]
                       ]
        """
	os_version_float = float(get_os_version())
	if os_version_float == 6.1:
		#  Windows 7
		return (
			VAULT_ITEM_WIN7,
			PVAULT_ITEM_WIN7,
			lambda hVault, pVaultItem, pPasswordVaultItem:
			vaultGetItem7(hVault, byref(pVaultItem.id), pVaultItem.pResource, pVaultItem.pUsername,
						  None, 0, byref(pPasswordVaultItem))
		)
	elif os_version_float > 6.1:
		#  Later than Windows7
		return (
			VAULT_ITEM_WIN8,
			PVAULT_ITEM_WIN8,
			lambda hVault, pVaultItem, pPasswordVaultItem:
			vaultGetItem8(hVault, byref(pVaultItem.id), pVaultItem.pResource, pVaultItem.pUsername,
						  pVaultItem.pPackageSid,  # additional parameter compared to Windows 7
						  None, 0, byref(pPasswordVaultItem))
		)

	raise Exception("Vault is not supported for this version of OS")
