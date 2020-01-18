'''
THIS MODULE IS INODE LAYER OF THE FILE SYSTEM. IT INCLUDES THE INODE DEFINITION DECLARATION AND GLOBAL HANDLE OF BLOCK LAYER OF API.
THIS MODULE IS RESPONSIBLE FOR PROVIDING ACTUAL BLOCK NUMBERS SAVED IN INODE ARRAY OF BLOCK NUMBERS TO FETCH DATA FROM BLOCK LAYER.
'''
import datetime, config, BlockLayer, InodeOps

#HANDLE OF BLOCK LAYER
interface = BlockLayer.BlockLayer()

class InodeLayer():

    #RETURNS BLOCK NUMBER FROM RESPECTIVE INODE DIRECTORY
    def INDEX_TO_BLOCK_NUMBER(self, inode, index):
        if index == len(inode.blk_numbers): return -1
        localBlockNum = interface.translate_virtual_blk_numbers(inode.blk_numbers)
        return localBlockNum[index]


    #RETURNS BLOCK DATA FROM INODE
    def INODE_TO_BLOCK(self, inode, offset):
        index = offset // config.BLOCK_SIZE
        block_number = self.INDEX_TO_BLOCK_NUMBER(inode, index)
        if block_number == -1: return ''
        else: return interface.BLOCK_NUMBER_TO_DATA_BLOCK(block_number)


    #MAKES NEW INODE OBJECT
    def new_inode(self, type):
        return InodeOps.Table_Inode(type)


    #FLUSHES ALL THE BLOCKS OF INODES FROM GIVEN INDEX OF MAPPING ARRAY  
    def free_data_block(self, inode, index):
        for i in range(index, len(inode.blk_numbers)):
            interface.free_data_block(inode.blk_numbers[i])
            inode.blk_numbers[i] = -1
        

       #IMPLEMENTS WRITE FUNCTIONALITY
    def write(self, inode, offset, data):
        '''WRITE YOUR CODE HERE '''
        #CALCUALTE THE MAX FILE SIZE
        max_file_size = len(inode.blk_numbers)*config.BLOCK_SIZE
        #print(max_file_size)
        #RETURN AN ERROR WHEN INODE TYPE IS NOT FILE
        if(inode.type!=0):
            print("Error: this is not file!")
            return -1
        #RETURN AN ERROR WHEN OFFSET IS LARGER THAN FILE SIZE
        if(offset > max_file_size):
            print("Error: offset is larger than file size!")
            return -1
        if(offset<0):
            offset = 0
        data_list1 = []
        data_list2 = []
        list1 = []
        list2 = []
        result = {}
        #GET THE INDOE INDEX NUMBER
        index = offset//config.BLOCK_SIZE
        #EXTRACT THE DATA ALREADY IN THE MAPPING
        localBlockNum = interface.translate_virtual_blk_numbers(inode.blk_numbers)
        if localBlockNum != -999:
            for i in range(index, len(localBlockNum)):
                data_list1.append(interface.BLOCK_NUMBER_TO_DATA_BLOCK(localBlockNum[i]))

        #DELETE THE \x00 IN THE LIST WHICH STANDS FOR THE UNUSED SPACE
        new_data= []
        lst = (i.rstrip('\x00') for i in data_list1)
        for j in lst: 
           new_data.append(j)

        #GENERATE THE DATA LIST TO STORE THE NEW DATA
        for i in range(index, len(data),config.BLOCK_SIZE):
            data_list2.append(data[i : i + config.BLOCK_SIZE])
        #GENERATE NEW LIST TO MAKE STRINGS BECOME LETTERS AS ELEMENTS 
        #FOR EXAMPLE, ['HELLLO'] BECOMES ['H','E','L','L','O']
        string1 = ''.join(new_data)
        string2 = ''.join(data_list2)
        list1 = list(string1)   
        list2 = list(string2)
        #print(string1)
        #WHEN OFFSET IS AFTER THE PREVIOUS STRING
        previous_offset = len(string1)+index*config.BLOCK_SIZE

        file = []
        localBlockNum = interface.translate_virtual_blk_numbers(inode.blk_numbers)
        if localBlockNum != -999:
            for i in range(0, len(localBlockNum)):
                file.append(interface.BLOCK_NUMBER_TO_DATA_BLOCK(localBlockNum[i]))

        new= []
        lst = (i.rstrip('\x00') for i in file)
        for j in lst: 
           new.append(j)

        initialstring = ''.join(new)
        
        if(offset > len(initialstring)):
            print("Error: write attempt beyond file size!")
            return -1
        if offset > previous_offset:
            if(offset == 0): 
                list1 = list1 + list2
            else:
                print("Error: write attempt beyond file size!")
                return -1
        else:
            
            #IF THE NEW STRING IS NOT LONGER THAN THE LENGTH OF PREVIOUS STRING AFFTER OFFSET (WRITE IN THE MIDDLE)
            self.free_data_block(inode, index-1)
            new_offset = offset - index*config.BLOCK_SIZE
            if len(data) <= (len(list1) - new_offset):
                #cHANGE THE DIFFERENT PART
                a_list = []
                for i in range(0, new_offset):
                    a_list.append(list1[i])
                for i in range(0, len(data)):
                    a_list.append(list2[i])
                list1 = a_list
            #OTHERWISE, CHANGE THE DIFFERENT PART AND APPEND NEW DATA
            else:
                for i in range(0, len(string1) - new_offset):
                    list1[new_offset+i] = list2[i]
                for i in range(len(string1) - new_offset, len(data)):
                    list1.append(list2[i])
            

        #TRUNCATE THE DATA WHEN DATA LENGTH IS LARGER THAN FILE SIZE
        if((offset + len(data)) > max_file_size):
            list1 = list1[0:max_file_size]
        final_string = ''.join(list1)
        final_list = []
        #PUT THE FINAL STRING INTO THE LIST WITH EVERY BLOCK SIZE
        for i in range(0, len(final_string),config.BLOCK_SIZE):
            final_list.append(final_string[i : i + config.BLOCK_SIZE])
        #FREE DATA BLOCKS AFTER INDEX 
        self.free_data_block(inode, index)      #FREES UP THE BLOCKS ASSOCIATED WITH THE INDEX NUMBER
        #PUT THE FINAL LIST INTO DATA BLOCKS AND RENEW THE MAPPING
        interface.get_first_four_blocks()
        for i in range(len(final_list)):
            valid_block_number = interface.get_valid_data_block() #RETURN A BLCOK NUMBER THAN BE USED TO STORE A BLOCK
            #if (i >= len(inode.blk_numbers)):
                #inode.blk_numbers.append(valid_block_number)
            inode.blk_numbers[index+i] = valid_block_number
        localBlockNum = interface.assign_virtual_blk_numbers(inode.blk_numbers)
        for i in range(len(final_list)):
            interface.update_data_block(localBlockNum[index+i], final_list[i])
        inode.time_accessed
        inode.time_modified
        return inode

    #IMPLEMENTS THE READ FUNCTION 
    def read(self, inode, offset, length): 
        '''WRITE   YOUR CODE HERE '''
        #CALCUALTE THE MAX FILE SIZE
        max_file_size = len(inode.blk_numbers)*config.BLOCK_SIZE
        if(offset<0):
            offset = 0
        #RETURN AN ERROR WHEN INODE TYPE IS NOT FILE
        if(inode.type!=0):
            print("Error: this is not file!")
            return inode, -1
        #RETURN AN ERROR WHEN OFFSET IS LARGER THAN FILE SIZE
        if(offset > max_file_size):
            print("Error: read attempt beyond max file size!")
            return inode, -1
        file = []
        localBlockNum =  interface.translate_virtual_blk_numbers(inode.blk_numbers)
        if localBlockNum != -999:
            for i in range(0, len(localBlockNum)):
                file.append(interface.BLOCK_NUMBER_TO_DATA_BLOCK(localBlockNum[i]))
        new_data= []
        lst = (i.rstrip('\x00') for i in file)
        for j in lst: 
           new_data.append(j)

        initialstring = ''.join(new_data)
        #print("string: " + initialstring)
        if (offset > len(initialstring)):
            print("Error: read attempt beyond max file size!")
            return inode, -1
        if(offset + length > len(initialstring)):
            end = len(initialstring)
        else:
            end = offset+length
        start_index = offset//config.BLOCK_SIZE
        start = offset - start_index*config.BLOCK_SIZE
        end_index = end//config.BLOCK_SIZE + 1 ;
        #EXTARCT THE DATA BLOCKS ASSOCIATED WITH THE INODE INDEX
        s = ""
        for i in range(start_index, end_index):
            string = self.INODE_TO_BLOCK(inode,offset)
            offset = offset+config.BLOCK_SIZE
            s = s + string
        s = s[start:end]
        #PRINT OUT THE FINAL STRING
        inode.time_accessed
        return inode, s


