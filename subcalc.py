
from nicegui import ui

ui.label('Subnet Calculator')

'''
ui.input(label='Text', placeholder='start typing',
         on_change=lambda e: result.set_text('you typed: ' + e.value),
         validation={'Input too long': lambda value: len(value) < 20})
result = ui.label()
'''

def is_valid_octet(item):
	#print(item)
	
	try:
		int(item)
		#return True
	except ValueError:
		return False
		
	if (int(item) >= 0) and (int(item) <= 255):
		return True
	else:
		return False 
	
	
def is_valid_cidr(item):
	print(item)
	
	try:
		int(item)
		#return True
	except ValueError:
		return False
		
	if (int(item) >= 0) and (int(item) <= 32):
		return True
	else:
		return False
		


def compute_cidr_string(cidr):
	cidr_int = int(cidr)
	bytes_left = 32 - cidr_int
	
	cidr_string = (cidr_int * '1') + (bytes_left * '0')
	return cidr_string
	

def compute_address_class(octet1):
	octet_int = int(octet1)
	
	# python range is inclusive of the start value, but stops before the stop value
	if octet_int in range(1, 127):
		return 'A'
	elif octet_int in range(128, 192):
		return 'B'
	elif octet_int in range(192, 224):
		return 'C'
	elif octet_int in range(224, 240):
		return 'D'
	elif octet_int in range(240, 256):
		return 'E'
	else:
		return False
	
	
def compute_subnets(octet1, octet2, octet3, octet4, cidr):
	octet1_binary_str = f"{int(octet1):08b}" 
	octet2_binary_str = f"{int(octet2):08b}"
	octet3_binary_str = f"{int(octet3):08b}"
	octet4_binary_str = f"{int(octet4):08b}"
	
	#print(f"{octet1_binary_str} {octet2_binary_str} {octet3_binary_str} {octet4_binary_str}")
	
	binary_str = octet1_binary_str + octet2_binary_str + octet3_binary_str + octet4_binary_str
	
	print(f"{binary_str}")
	
	decimal_num = int(binary_str, 2)
	
	cidr_str = compute_cidr_string(cidr)
	print(f"{cidr_str}")
	
	return 0
	
	
	

with ui.row(align_items='bottom').classes('items-center'):
	ui.label('Enter the 4 octets and a CIDR value.')


with ui.row(align_items='bottom').classes('items-center'):
	octet1 = ui.input(label="Octet 1", value='192', placeholder='192', validation={'Must be integer from 0-255': lambda value: is_valid_octet(value)}).classes('w-20').props('debounce=1000')

	ui.html('<strong>.</strong>', sanitize=False)
	
	octet2 = ui.input(label="Octet 2", value='168', placeholder='168', validation={'Must be integer from 0-255': lambda value: is_valid_octet(value)}).classes('w-20').props('debounce=1000')

	ui.html('<strong>.</strong>', sanitize=False)
	
	octet3 = ui.input(label="Octet 3", value='1', placeholder='1', validation={'Must be integer from 0-255': lambda value: is_valid_octet(value)}).classes('w-20').props('debounce=1000')
	
	ui.html('<strong>.</strong>', sanitize=False)
	
	octet4 = ui.input(label="Octet 4", value='0', placeholder='0', validation={'Must be integer from 0-255': lambda value: is_valid_octet(value)}).classes('w-20').props('debounce=1000')
	#result = ui.label()

	ui.html('<strong>/</strong>', sanitize=False)

	cidr = ui.input(label="CIDR", value='24', placeholder='24', validation={'Must be integer from 0-32': lambda value: is_valid_cidr(value)}).classes('w-20').props('debounce=1000')


	#address_class = compute_address_class(octet1.value)
	ui.label('Class: ')
	ui.label().bind_text_from(octet1, 'value', lambda value: compute_address_class(value))


with ui.row(align_items='bottom').classes('items-center'):
	ui.label('Default subnet mask: ')
	ui.label('Subnet bits: ')
	ui.label('Host bits: ')
	ui.label('Max subnets: ')
	ui.label('Max hosts: ')
	
with ui.row(align_items='bottom').classes('items-center'):
	ui.html('<hr />').classes('w-full')
	ui.button('Compute Subnets', on_click=lambda: compute_subnets(octet1.value, octet2.value, octet3.value, octet4.value, cidr.value))
	
	
ui.run()

