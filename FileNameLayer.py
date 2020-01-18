'''
THIS MODULE ACTS LIKE FILE NAME LAYER AND PATH NAME LAYER (BOTH) ABOVE INODE LAYER.
IT RECIEVES INPUT AS PATH (WITHOUT INITIAL '/'). THE LAYER IMPLEMENTS LOOKUP TO FIND INODE NUMBER OF THE REQUIRED DIRECTORY.
PARENTS INODE NUMBER IS FIRST EXTRACTED BY LOOKUP AND THEN CHILD INODE NUMBER BY RESPECTED FUNCTION AND BOTH OF THEM ARE UPDATED
'''
import InodeNumberLayer

#HANDLE OF INODE NUMBER LAYER
interface = InodeNumberLayer.InodeNumberLayer()

class FileNameLayer():

	#PLEASE DO NOT MODIFY
	#RETURNS THE CHILD INODE NUMBER FROM THE PARENTS INODE NUMBER
	def CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(self, childname, inode_number_of_parent):
		inode = interface.INODE_NUMBER_TO_INODE(inode_number_of_parent)
		if not inode: 
			print("Error1 FileNameLayer: Lookup Failure!")
			return -1
		if inode.type == 0:
			print("Error2 FileNameLayer: Invalid Directory!")
			return -1
		if childname in inode.directory: return inode.directory[childname]
		print("Error3 FileNameLayer: Lookup Failure!")
		return -1

	#PLEASE DO NOT MODIFY
	#RETUNS THE PARENT INODE NUMBER FROM THE PATH GIVEN FOR A FILE/DIRECTORY 
	def LOOKUP(self, path, inode_number_cwd):   
		name_array = path.split('/')
		if len(name_array) == 1: return inode_number_cwd
		else:
			child_inode_number = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(name_array[0], inode_number_cwd)
			if child_inode_number == -1: return -1
			return self.LOOKUP("/".join(name_array[1:]), child_inode_number)

	#PLEASE DO NOT MODIFY
	#MAKES NEW ENTRY OF INODE
	def new_entry(self, path, inode_number_cwd, type):
		if path == '/': #SPECIAL CASE OF INITIALIZING FILE SYSTEM
			interface.new_inode_number(type, inode_number_cwd, "root")
			return True
		parent_inode_number = self.LOOKUP(path, inode_number_cwd)
		parent_inode = interface.INODE_NUMBER_TO_INODE(parent_inode_number) 
		childname = path.split('/')[-1]
		if not parent_inode: return -1
		if childname in parent_inode.directory:
			print("Error FileNameLayer: File already exists!")
			return -1
		child_inode_number = interface.new_inode_number(type, parent_inode_number, childname)  #make new child
		if child_inode_number != -1:
			parent_inode.directory[childname] = child_inode_number
			interface.update_inode_table(parent_inode, parent_inode_number)


	#IMPLEMENTS READ
	def read(self, path, inode_number_cwd, offset, length):
		'''WRITE YOUR CODE HERE'''
		#RETURN THE PARENT INODE NUMBER FROM THE GIVEN 
		parent_inode_number = self.LOOKUP(path, inode_number_cwd)
		#GET THE FILE NAME
		childname = path.split('/')[-1] 
		#FIND THE INODE NUMBER REFERENCE TO THAT FILE
		child_inode_number = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(childname, parent_inode_number) 
		if child_inode_number == -1:
			print("Error FileNameLayer: Wrong Path Given!\n") 
			return -1 
		return interface.read(child_inode_number, offset, length, parent_inode_number)
	
	#IMPLEMENTS WRITE
	def write(self, path, inode_number_cwd, offset, data):
		'''WRITE YOUR CODE HERE'''
		# inode_number_cwd = 0/-1 TO SEE IF THE PATH IS CORRECT OR NOT
		#FIND THE PARENT INODE NUMBER FROM PATH
		parent_inode_number = self.LOOKUP(path, inode_number_cwd)
		#EXTRACT THE FILE NAME FROM PATH
		childname = path.split('/')[-1] 
		#FIND THE INODE NUMBER REFERENCE TO THAT FILE
		child_inode_number = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(childname, parent_inode_number) 
		if child_inode_number != -1:
			interface.write(child_inode_number, offset, data, inode_number_cwd) 
			return True
		else:
			print("Error FileNameLayer: Wrong Path Given!\n")
			return -1
	#HARDLINK
	def link(self, old_path, new_path, inode_number_cwd):
		'''WRITE YOUR CODE HERE'''
		#FIND THE OLD FILE'S PARENT INODE NUMBER
		old_parent_number = self.LOOKUP(old_path, inode_number_cwd)
		#THE FILE NAME OF THE OLD FILE
		old_name = old_path.split('/')[-1]
		#MAKE A NEW PATH WHICH HAS THE SAME FILE NAME AS OLD FILE            
		new_path = new_path + "/" + old_name
		#FIND THE NEW FILE'S PARENT INODE NUMBER 
		new_parent_number = self.LOOKUP(new_path, inode_number_cwd) 
		if old_parent_number == -1 or new_parent_number == -1:
			print("Error FileNameLayer: Incorrect file names!"); 
			return -1
		#FIND THE INODE FROM THE INODE NUMBER
		old_inode = interface.INODE_NUMBER_TO_INODE(old_parent_number)
		new_inode = interface.INODE_NUMBER_TO_INODE(new_parent_number)
		if old_name in new_inode.directory:
			print("Error FileNameLayer: Filename already exists!")
			return -1 	
		#HARDLINK SHOULD USE THE SAME INODE NUMBER
		child_inode_number = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(old_name, old_parent_number)
		if child_inode_number == -1:
			return -1
		#USE THE OLD INODE NUMBER, NEW PARENT NUMBER AND INODE 
		return interface.link(child_inode_number, old_name, new_parent_number) 
 
 

	#REMOVES THE FILE/DIRECTORY
	def unlink(self, path, inode_number_cwd):
		'''WRITE YOUR CODE HERE'''
		if path == "": 
			print("Error FileNameLayer: Cannot delete root directory!")
			return -1
		#FIND THE FILE'S INODE NUMBER
		parent_inode_number = self.LOOKUP(path, inode_number_cwd)
		if(parent_inode_number == -1):
			print("Error FileNameLayer: Incorrect file name!")
			return -1
		#EXTRACT THE FILE NAME
		filename = path.split('/')[-1]
		#GET THE INODE NUMBER OF THE FILE
		child_inode_number = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(filename, parent_inode_number)
		if(child_inode_number == -1):
			return -1
		return interface.unlink(child_inode_number, parent_inode_number, filename)

	#MOVE
	def mv(self, old_path, new_path, inode_number_cwd):
		'''WRITE YOUR CODE HERE'''
		#LINK TO A NEW PATH
		indicator = self.link(old_path, new_path, inode_number_cwd)
		if indicator == -1:
			return -1
		#UNLINK THE OLD FILE
		self.unlink(old_path, inode_number_cwd)