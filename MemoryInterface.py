'''
THIS MODULE INTERACTS WITH THE MEMORY
''' 
import time, client_stub,client_stub_RAID1

#HANDLE FOR MEMORY OPERATIONS
client_stub = client_stub.client_stub()
client_stub_RAID1 = client_stub_RAID1.client_stub()

def RAID_1():
    RAID_1.has_been_called = True
def RAID_5():
    RAID_5.has_been_called = True

#REQUEST TO BOOT THE FILE SYSTEM
def Initialize_My_FileSystem():
    print("File System Initializing......")
    time.sleep(2)
    if(RAID_5.has_been_called == True):
        state = client_stub.Initialize()
    if(RAID_1.has_been_called == True):
        state = client_stub_RAID1.Initialize()
    print("File System Initialized!")


#REQUEST TO FETCH THE INODE FROM INODE NUMBER FROM SERVER
def inode_number_to_inode(inode_number):
    if(RAID_5.has_been_called == True):
        return client_stub.inode_number_to_inode(inode_number)
    if(RAID_1.has_been_called == True):
        return client_stub_RAID1.inode_number_to_inode(inode_number)


#REQUEST THE DATA FROM THE SERVER
def get_data_block(block_number):
    if(RAID_5.has_been_called == True):
        return ''.join(client_stub.get_data_block(block_number))
    if(RAID_1.has_been_called == True):
        return ''.join(client_stub_RAID1.get_data_block(block_number))

#REQUESTS THE VALID BLOCK NUMBER FROM THE SERVER 
def get_valid_data_block():
    if(RAID_5.has_been_called == True):
        return ( client_stub.get_valid_data_block() )
    if(RAID_1.has_been_called == True):
        return ( client_stub_RAID1.get_valid_data_block() )


#REQUEST TO MAKE BLOCKS RESUABLE AGAIN FROM SERVER
def free_data_block(block_number):
    if(RAID_5.has_been_called == True):
        client_stub.free_data_block((block_number))
    if(RAID_1.has_been_called == True):
        client_stub_RAID1.free_data_block((block_number))

#REQUEST TO WRITE DATA ON THE THE SERVER
def update_data_block(block_number, block_data):
    if(RAID_5.has_been_called == True):
        client_stub.update_data_block(block_number, block_data)
    if(RAID_1.has_been_called == True):
        client_stub_RAID1.update_data_block(block_number, block_data)

#REQUEST TO UPDATE THE UPDATED INODE IN THE INODE TABLE FROM SERVER
def update_inode_table(inode, inode_number):
    if(RAID_5.has_been_called == True):
        client_stub.update_inode_table(inode, inode_number)
    if(RAID_1.has_been_called == True):
        client_stub_RAID1.update_inode_table(inode, inode_number)  

def translate_virtual_blk_numbers(blk_number_list):
    if(RAID_5.has_been_called == True):
        return client_stub.translate_virtual_blk_numbers(blk_number_list)
    if(RAID_1.has_been_called == True):
        return client_stub_RAID1.translate_virtual_blk_numbers(blk_number_list)

def assign_virtual_blk_numbers(blk_number_list):
    if(RAID_5.has_been_called == True):
        return client_stub.assign_virtual_blk_numbers(blk_number_list)
    if(RAID_1.has_been_called == True):
        return client_stub_RAID1.assign_virtual_blk_numbers(blk_number_list)

def get_first_four_blocks():
    if(RAID_5.has_been_called == True):
        return client_stub.get_first_four_blocks()
    if(RAID_1.has_been_called == True):
        return client_stub_RAID1.get_first_four_blocks()

#REQUEST FOR THE STATUS OF FILE SYSTEM FROM SERVER
def status():
    if(RAID_5.has_been_called == True):
        return client_stub.status()
    if(RAID_1.has_been_called == True):
        return client_stub_RAID1.status()


RAID_1.has_been_called = False
RAID_5.has_been_called = False
