''' IPv4 subnet calculator app for classroom demonstrations.'''
''' Using the cool nicegui python framework.'''
''' Version 1   11/13/2026 '''
from nicegui import ui


# IP_State holds the state info for the subnet calculator app.  
class IP_State:
    def __init__(self, address_class='C', default_subnet_mask='255.255.255.0'):
        self.address_class = address_class
        self.default_subnet_mask = default_subnet_mask
        self.octet1 = '192'
        self.octet2 = '168'
        self.octet3 = '1'
        self.octet4 = '0'
        self.cidr = '24'
        self.subnet_bits = ''
        self.host_bits = ''
        self.max_subnets = ''
        self.max_hosts = ''
        self.usable_hosts = ''
        self.new_subnet_mask = ''
        self.subnet_table = ''

    @property
    def default_subnet_mask(self):
        """Getter method."""
        return self._default_subnet_mask
        
    @default_subnet_mask.setter
    def default_subnet_mask(self, value):
        self._default_subnet_mask = value
        
        
    @property
    def address_class(self):
        return self._address_class
        
              
    @address_class.setter
    def address_class(self, value):
        #print(f"Initial value: {value}")
        if value not in ['A', 'B', 'C', 'D', 'E']:
            raise ValueError("Invalid IPv4 address class.")
        #return compute_address_class(self.octet1)
        self._address_class = value
        
    



def is_valid_octet(octet: str) -> bool:
    ''' Determines if an IPv4 octet is valid. '''
    try:
        int(octet)
    except ValueError:
        return False
        
    return bool(int(octet) >= 0 and int(octet) <= 255)
	
	
def is_valid_cidr(cidr: str) -> bool:
    ''' Determines if a CIDR value is valid. '''
    # Make sure it's an integer
    try:
	    int(cidr)
    except ValueError:
	    return False
	    
    # Make sure it's in the valid range
    '''
    if (int(cidr) >= 0) and (int(cidr) <= 32):
	    return True
    else:
	    return False
    '''
    return bool(int(cidr) >= 0 and int(cidr) <= 32)


def compute_cidr_string(cidr: str) -> str:
    ''' Compute the CIDR address as a binary string (string of 1's and 0's) '''
    cidr_int = int(cidr)
    bytes_left = 32 - cidr_int

    cidr_string = (cidr_int * '1') + (bytes_left * '0')
    return cidr_string
	

def compute_address_class(octet1: str) -> str:
    ''' Compute and return the address class based off of the first octet. '''
    octet_int = int(octet1)
    address_class = ''

    # python range is inclusive of the start value, but stops before the stop value
    if octet_int in range(1, 127):
	    address_class = 'A'
    elif octet_int in range(128, 192):
	    address_class = 'B'
    elif octet_int in range(192, 224):
	    address_class = 'C'
    elif octet_int in range(224, 240):
	    address_class = 'D'
    elif octet_int in range(240, 256):
	    address_class = 'E'
    else:
	    return ''

    return address_class
	
	

       
       
def get_default_subnet_mask(address_class: str) -> str:
        ''' Returns the default subnet mask for a given address class. '''
        #print(f"Value: {address_class}")
        
        if address_class == 'A':
                return '255.0.0.0'
        elif address_class == 'B':
                return '255.255.0.0'
        elif address_class == 'C':
                return '255.255.255.0'
        else:
                return ''
       


def octets_to_string(octet1: str, octet2: str, octet3: str, octet4: str) -> str:
    octet1_binary_str = f"{int(octet1):08b}" 
    octet2_binary_str = f"{int(octet2):08b}"
    octet3_binary_str = f"{int(octet3):08b}"
    octet4_binary_str = f"{int(octet4):08b}"
	
    binary_str = octet1_binary_str + octet2_binary_str + octet3_binary_str + octet4_binary_str

    #print(f"{binary_str}")

    return binary_str
	
	        


def compute_subnet_mask():
    ''' Computes a new subnet mask when values on the application change. '''
    address_class = compute_address_class(state.octet1)
    cidr = state.cidr
    
    if (address_class == 'A') and (cidr == '8') or (address_class == 'B') and (cidr == '16') or (address_class == 'C') and (cidr == '24'):
        state.new_subnet_mask = get_default_subnet_mask(state.address_class) #same as the default subnet mask
    else: #not a default
        network_bits = int(cidr)
        host_bits = 32 - int(network_bits)
        mask_string =  (network_bits * '1') + (host_bits * '0')
        
        #octets = [mask_string[i: i+8] for i in range(0, len(mask_string), 8)]    #getting groups of 8  
        octets = []
        octets.append(mask_string[0:8:1])
        octets.append(mask_string[8:16:1])
        octets.append(mask_string[16:24:1])
        octets.append(mask_string[24:])
        
        #print(f"Octets: {octets}")
        
        
        new_mask = ''
        for i in octets:
            new_mask = new_mask + str(int(i,2)) + '.'
        new_mask = new_mask.removesuffix('.')          
        
        #print(f"new_mask: {new_mask}")
        state.new_subnet_mask = new_mask
    



def add_rows_to_subnet_table(subnet_list:list):
    ''' Take a list of subnets and get the network address, ip range and broadcast address. Then add the info to the subnet_table. '''
    
    for subnet in subnet_list:
        ip_part, prefix_str = subnet.split("/")
        mytuple = calculate(ip_part, int(prefix_str))
        #print(f"MyTuple: {mytuple}")
        #tuple format (address, network, firsthost, lasthost, broadcast)
        
        network_address = make_ip_str(mytuple[1])
        first_ip = make_ip_str(mytuple[2])
        last_ip = make_ip_str(mytuple[3])
        broadcast = make_ip_str(mytuple[4])
        #print(f"Broadcast: {broadcast}")
        ip_range = first_ip + ' - ' + last_ip
        
        state.subnet_table.rows.append({'Network Address': network_address, 'Usable IP Range': ip_range, 'Broadcast Address': broadcast})
    
 


    
def make_ip_str(ip_int: int) -> str:
    """
    Takes and IPv4 address as an integer and returns a string in dotted
    decimal notation.
    Returns the following tuple of information: ip_address string
    
    Args:
        ip_int (integer): The IPv4 address as an integer.

    Returns:
        ip_str (string) IPv4 dotted decimal notation
    """
    
    #print("In make_ip_str.")
    ip_bin_str = format(ip_int, '032b')
    #print(ip_bin_str)
    
    
    octet_list = [None] * 4 #empty list of 4 items
    
    start_slice = 0
    end_slice = 8
    
    for index, octet in enumerate(octet_list):
        octet_list[index] = str(int(ip_bin_str[start_slice:end_slice],2))
        start_slice += 8
        end_slice += 8
        
    ip_str = '.'.join(octet_list)
    
    return ip_str



def make_ip_num(ip_str: str) -> int:
    """
    Takes and IPv4 address string in dotted decimal notation.
    Coverts and returns an integer representation of that address.

    Args:
        ip_str (string): The IPv4 address string.

    Returns:
        int: The IPv4 address as an integer.
    """
            
    ip_list = ip_str.split('.')  #split into parts
    #print(ip_list)

    # make each element in the list an integer
    '''
    #old way
    ip_list[0] = int(ip_list[0]) 
    ip_list[1] = int(ip_list[1])
    ip_list[2] = int(ip_list[2])
    ip_list[3] = int(ip_list[3])
    '''
    
    for index, item in enumerate(ip_list):
        ip_list[index] = int(ip_list[index])
        
    #print(ip_list)

    # shift each item appropriately
    ip_list[0] = ip_list[0] << 24
    ip_list[1] = ip_list[1] << 16
    ip_list[2] = ip_list[2] << 8
    # print(ip_list)


    #ip_integer = ip_list[0] + ip_list[1] + ip_list[2] + ip_list[3]
    ip_integer = 0
    for index, item in enumerate(ip_list):
        ip_integer += item

    #print("IP int = ", str(ip_integer))
    
    return ip_integer
    

def calculate(ip_str, CIDR_int) -> tuple:
    """
    Takes and IPv4 address string in dotted decimal notation and a
    CIDR value as an integer.
    Returns the following tuple of information - all integers:
    (address, network, firsthost, lasthost, broadcast)


    Args:
        ip_str (string): The IPv4 address string.
        cidr (int): The CIDR value as an integer.

    Returns:
        tuple of integers: (address, network, firsthost, lasthost, broadcast)
    """
              
    ip_int = make_ip_num(ip_str)
    
    #convert string to integer giving network bits
    host_int = 32 - CIDR_int  #find the host bits

    # Get networkID (masking method)
    network_part = '1' * CIDR_int   #give me a bunch of 1's
    host_part = '0' * (host_int)  #give me a bunch of 0's
    subnet_mask_string = network_part + host_part  #put the mask together
    #print("Subnet mask string: " + subnet_mask_string)

    subnet_mask_int = int(subnet_mask_string,2)  #convert binary string to integer
    #print("Subnet Mask Integer: " + str(subnet_mask_int))

    network_ID = (ip_int & subnet_mask_int) # logical AND ip address and subnet mask
    #print("Network ID: " + str(network_ID))

    first_host = network_ID + 1  #just add 1 to get the first host IP
    #print("First Host: " + str(first_host))


    # 2b: get broadcast (shifting method) (page 58)
    broadcast = (ip_int >> host_int) #shift right by num of host bits
    broadcast = broadcast + 1 #add 1
    broadcast = (broadcast << host_int) #shift left by num of host bits
    broadcast = broadcast - 1 #subtract 1
    #print("Broadcast: " + str(broadcast))

    last_host = broadcast -1
    #print("Last host: " + str(last_host))
    
    my_tuple = (ip_int, network_ID, first_host, last_host, broadcast) 
    return my_tuple
    


def ip_to_int(ip_str: str) -> int:
    """Converts a dotted-decimal IP string to a 32-bit integer."""
    octets = [int(o) for o in ip_str.split(".")]
    return (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]


def int_to_ip(ip_int: int) -> str:
    """Converts a 32-bit integer back to a dotted-decimal IP string."""
    return ".".join(str((ip_int >> shift) & 0xFF) for shift in (24, 16, 8, 0))
    
    
def get_subnets(octet1: str, octet2: str, octet3: str, octet4: str, new_prefix: str) -> list[str]:
    """Splits a given CIDR block into all possible subnets of size `new_prefix`."""
    #ip_part, prefix_str = cidr.split("/")
    ip_part = octet1 + '.' + octet2 + '.' + octet3 + '.' +  octet4
    new_prefix = int(new_prefix)
    #old_prefix = int(prefix_str)
    old_prefix = int(get_original_cidr(state.address_class))

    if not (0 <= old_prefix <= new_prefix <= 32):
        raise ValueError("Invalid prefix lengths.")

    # 1. Create the original subnet mask and ensure we start at the true network address
    old_mask = (0xFFFFFFFF << (32 - old_prefix)) & 0xFFFFFFFF
    base_network_int = ip_to_int(ip_part) & old_mask

    # 2. Calculate how many subnets to create and the IP jump (step size) between them
    num_subnets = 1 << (new_prefix - old_prefix)  # Equivalent to 2 ** (new_prefix - old_prefix)
    step_size = 1 << (32 - new_prefix)            # Number of IPs per new subnet

    # 3. Generate each subnet
    subnets = []
    for i in range(num_subnets):
        subnet_int = base_network_int + (i * step_size)
        subnets.append(f"{int_to_ip(subnet_int)}/{new_prefix}")

    #print(subnets)
    
    add_rows_to_subnet_table(subnets)
    
    state.subnet_table.set_visibility(True)
    
    return subnets


def get_original_cidr(address_class: str) -> str:
    ''' Returns the CIDR value for a given IPv4 network class. '''
    if state.address_class == 'A':
        return '8'
    elif state.address_class == 'B':
        return '16'
    elif state.address_class == 'C':
        return '24'


def recompute_everything():
    ''' Recomputes all of the application values after a user changes something.  Keeps the IP_State current.'''
    cidr = state.cidr
    state.host_bits = str(32 - int(cidr))
    state.max_hosts = str(2 **int(state.host_bits))
    state.usable_hosts = str(int(state.max_hosts) - 2)
    state.address_class = compute_address_class(state.octet1)
    
    #print(f"state_octet1 = {state.octet1}")
    #print(f"state_address_class = {state.address_class}")
    
    state.default_subnet_mask = get_default_subnet_mask(state.address_class)
    compute_subnet_mask()
    
    state.subnet_bits = int(cidr) - int(get_original_cidr(state.address_class))
       
    state.max_subnets = str(2 **int(state.subnet_bits))
    

    
    
    
def get_subnet_ips(octet1: str, octet2: str, octet3: str, octet4: str, cidr: str, usable_only=False) -> list:
    #ip_str, prefix_str = cidr.split('/')
    ip_str = octet1 + '.' + octet2 + '.' + octet3 + '.' +  octet4
    prefix = int(cidr)
    
    # Convert dotted-decimal IP to a single 32-bit integer
    octets = [int(o) for o in ip_str.split('.')]
    ip_int = (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]
    
    # Create the 32-bit subnet mask and find network & broadcast bounds
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF if prefix > 0 else 0
    network_int = ip_int & mask
    broadcast_int = network_int | (~mask & 0xFFFFFFFF)
    
    # Determine range (exclude network/broadcast if usable_only is True)
    start = network_int + 1 if (usable_only and prefix < 31) else network_int
    end = broadcast_int - 1 if (usable_only and prefix < 31) else broadcast_int
    
    # Convert each 32-bit integer back into dotted-decimal format
    print(f"Start: {start}    End: {end}")
    
    ips = []
    for addr in range(start, end + 1):
        b1 = (addr >> 24) & 0xFF
        b2 = (addr >> 16) & 0xFF
        b3 = (addr >> 8) & 0xFF
        b4 = addr & 0xFF
        ips.append(f"{b1}.{b2}.{b3}.{b4}")
        
    #print(ips)
    return ips


    
def update_octet1(octet1: str):
    state.octet1 = octet1
    recompute_everything()
    
 
def update_octet2(octet2):
    state.octet2 = octet2
    recompute_everything()
    
    
def update_octet3(octet3):
    state.octet3 = octet3
    recompute_everything()
    
    
def update_octet4(octet4):
    state.octet4 = octet4
    recompute_everything()
    
    
def update_cidr(cidr):
    state.cidr = cidr
    recompute_everything()
   
    
   
    

############################################################	
# allow for multiprocessing in main
if __name__ in {"__main__", "__mp_main__"}:

    state = IP_State()


    ui.label('Subnet Calculator')


    with ui.row(align_items='bottom').classes('items-center'):
	    ui.label('Enter the 4 octets and a CIDR value.')


    with ui.row(align_items='bottom').classes('items-center'):
	    octet1 = ui.input(label="Octet 1", value='192', placeholder='192', validation={'Must be integer from 0-255': lambda value: is_valid_octet(value)}, on_change=lambda e: update_octet1(octet1.value)).classes('w-20').props('debounce=1000')

	    ui.html('<strong>.</strong>', sanitize=False)
	    
	    octet2 = ui.input(label="Octet 2", value='168', placeholder='168', validation={'Must be integer from 0-255': lambda value: is_valid_octet(value)}, on_change=lambda e: update_octet2(octet2.value)).classes('w-20').props('debounce=1000')

	    ui.html('<strong>.</strong>', sanitize=False)
	    
	    octet3 = ui.input(label="Octet 3", value='1', placeholder='1', validation={'Must be integer from 0-255': lambda value: is_valid_octet(value)}, on_change=lambda e: update_octet3(octet3.value)).classes('w-20').props('debounce=1000')
	    
	    ui.html('<strong>.</strong>', sanitize=False)
	    
	    octet4 = ui.input(label="Octet 4", value='0', placeholder='0', validation={'Must be integer from 0-255': lambda value: is_valid_octet(value)}, on_change=lambda e: update_octet4(octet4.value)).classes('w-20').props('debounce=1000')
	    #result = ui.label()

	    ui.html('<strong>/</strong>', sanitize=False)

	    cidr = ui.input(label="CIDR", value='24', placeholder='24', validation={'Must be integer from 0-32': lambda value: is_valid_cidr(value)}, on_change=lambda e: update_cidr(cidr.value)).classes('w-20').props('debounce=1000')


	    #address_class = compute_address_class(octet1.value)
	    ui.label('Class: ')
	    #address_class = ui.label().bind_text_from(octet1, 'value', lambda value: compute_address_class(value))
	    address_class = ui.label().bind_text_from(state, 'address_class')
        

    with ui.row(align_items='bottom').classes('items-center'):
        ui.label('Default subnet mask:')
        #default_subnet_mask = ui.label().bind_text_from(address_class, 'text', lambda text: get_default_subnet_mask(text))
        default_subnet_mask = ui.label().bind_text_from(state, 'default_subnet_mask')
        #print(f"{default_subnet_mask.text}")
        ui.label('Subnet bits: ')
        subnet_bits = ui.label().bind_text_from(state, 'subnet_bits')
        ui.label('Host bits: ')
        host_bits = ui.label().bind_text_from(state, 'host_bits')
        ui.label('Max subnets: ')
        max_subnets = ui.label().bind_text_from(state, 'max_subnets')
        ui.label('Max hosts: ')
        max_hosts = ui.label().bind_text_from(state, 'max_hosts')
        ui.label('Usable hosts: ')
        max_hosts = ui.label().bind_text_from(state, 'usable_hosts')
	    #print(f"{address_class.text}")
	    
	    
    with ui.row(align_items='bottom').classes('items-center'):
        ui.label('New subnet mask:')
        new_subnet_mask = ui.label().bind_text_from(state, 'new_subnet_mask')

    with ui.row(align_items='bottom').classes('items-center'):
	    ui.html('<hr />').classes('w-full')
	    ui.button('Compute Subnets', on_click=lambda: get_subnets(octet1.value, octet2.value, octet3.value, octet4.value, cidr.value))
	    
#    with ui.row(align_items='bottom').classes('items-center'):    
#        ui.label('Subnet Table')
	    
    with ui.row(align_items='bottom').classes('items-center'):
        
        columns = [
            {'name': 'Network Address', 'label': 'Network Address', 'field': 'Network Address'},
            {'name': 'Usable IP Range', 'label': 'Usable IP Range', 'field': 'Usable IP Range'},
            {'name': 'Broadcast Address', 'label': 'Broadcast Address', 'field': 'Broadcast Address'},
        ]

        rows = []
            
        state.subnet_table = ui.table(columns=columns, rows=rows, row_key='name').props('no-data-label="No rows in the table."')
        state.subnet_table.set_visibility(False)
        
    ui.run()

