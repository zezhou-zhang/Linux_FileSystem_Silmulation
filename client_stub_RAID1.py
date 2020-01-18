# SKELETON CODE FOR CLIENT STUB HW4
#import xmlrpc.client, config, pickle
# SKELETON CODE FOR CLIENT STUB HW4
import xmlrpclib, config, pickle
import binascii,time
class client_stub():

	def __init__(self):
		self.proxy1 = xmlrpclib.ServerProxy("http://localhost:8000/")
		self.proxy2 = xmlrpclib.ServerProxy("http://localhost:8001/")
		self.counter_get_first_four_blocks = 0
		self.block_number_for_server_1 = []
		self.block_number_for_server_2 = []
		self.serverNum = []
		self.server1_pointer = 0
		self.server2_pointer = 0

		self.server1_first_block = 0
		self.server2_first_block = 0

		self.server1_first_parity = 0
		self.server2_first_parity = 0

		self.parity_block_list = []
		self.server1_error_mask = 0
		self.server2_error_mask = 0

		self.server1_requests = 0
		self.server2_requests = 0
		self.occupied_blocks = []

	# DEFINE FUNCTIONS HERE

	# example provided for initialize
	def Initialize(self):
		try :
			retVal = pickle.loads(self.proxy1.Initialize())
			self.server1_requests += 1
		except Exception as err :
			# print error message
			print("Error1: Initialization failed!")
		try :
			retVal = pickle.loads(self.proxy2.Initialize())
			self.server2_requests += 1
		except Exception as err :
			# print error message
			print("Error1: Initialization failed!")


		

	def inode_number_to_inode(self, inode_number):
		
		inode_number = pickle.dumps(inode_number)
		if self.server1_error_mask == 0:
			try:
				retVal1 = self.proxy1.inode_number_to_inode(inode_number)
				retVal1 = pickle.loads(retVal1)
				self.server1_requests += 1
			except Exception as err :
				retVal1 = -999
				# print error message
				self.server1_error_mask = 1
				print("Error2: Server1 connection failed!")
				retVal2 = self.proxy2.inode_number_to_inode(inode_number)
				retVal2 = pickle.loads(retVal2)
				self.server2_requests += 1
		else:	
			retVal1 = -999
			try:
				retVal2 = self.proxy2.inode_number_to_inode(inode_number)
				retVal2 = pickle.loads(retVal2)
				self.server2_requests += 1
			except Exception as err :
				retVal2 = -999
				# print error message
				self.server2_error_mask = 1
				print("Error2: Server2 connection failed!")

			
				
		if retVal1 != -999:
			return retVal1
		if retVal2 != -999:
			return retVal2

	

	def get_data_block(self, block_number):

		for i in self.block_number_list_for_server_1:
			if (i == block_number):
				block_number = pickle.dumps(block_number)
				if self.server1_error_mask == 0:
					try:
						retVal1 = ''.join(self.proxy1.get_data_block(block_number))
						retVal1 = pickle.loads(retVal1)
						self.server1_requests += 1
						if retVal1 == -999:
							retVal2 = ''.join(self.proxy2.get_data_block(block_number))
							retVal2 = pickle.loads(retVal2)
							self.server2_requests += 1
					except Exception as err :
						self.server1_error_mask = 1
						# print error message
						print("Error3: Server1 connection failed!")
						print("Trying to use Server2 to get data...")
						retVal2 = ''.join(self.proxy2.get_data_block(block_number))
						retVal2 = pickle.loads(retVal2)
						self.server2_requests += 1
				else:
					retVal2 = ''.join(self.proxy2.get_data_block(block_number))
					retVal2 = pickle.loads(retVal2)
					self.server2_requests += 1

				block_number = pickle.loads(block_number)

				if self.server1_error_mask == 0:
					if(retVal1 != -999):
						print("The data resides in server1.")
						time.sleep(2.5)
						return retVal1
					else:
						print("Data in this server1 is corrupted!")
						print("Trying to recover the data...")
						return retVal2
				else:
					if(retVal2 != -999):
						print("The data now resides in server2.")
						time.sleep(2.5)
						return retVal2
					
		for i in self.block_number_list_for_server_2:
			if (i == block_number): 
				block_number = pickle.dumps(block_number)
				if self.server2_error_mask == 0:
					try:
						retVal2 = ''.join(self.proxy2.get_data_block(block_number))
						retVal2 = pickle.loads(retVal2)
						self.server2_requests += 1
					except Exception as err :
						self.server2_error_mask = 1
						# print error message
						print("Error3: Server2 connection failed!")
						print("Trying to use Server3 to get data...")
	


	def get_valid_data_block(self):
		retVal1 = -999
		retVal2 = -999

		if self.server1_error_mask == 0:
			try:
				retVal1 = self.proxy1.get_valid_data_block()
				retVal1 = pickle.loads(retVal1)
				self.server1_requests += 1
			except:
				self.server1_error_mask = 1
				retVal1 = -999
				print("Error4: Server1 connection failed!")
		if self.server2_error_mask == 0:
			try:
				retVal2 = self.proxy2.get_valid_data_block()
				retVal2 = pickle.loads(retVal2)
				self.server2_requests += 1
				
			except:
				self.server2_error_mask = 1
				retVal2 = -999
				print("Error4: Server2 connection failed!")
	

		if retVal1 != -999:
			return retVal1
		if retVal2 != -999:
			return retVal2

		
		

	def free_data_block(self, block_number):
		
		block_number = pickle.dumps(block_number)
		if self.server1_error_mask == 0:
			try:
				self.proxy1.free_data_block(block_number)
				self.server1_requests += 1	
			except Exception as err :
				# print error message
				self.server1_error_mask = 1
				print("Error5: Server1 connection failed!")
		if self.server2_error_mask == 0:
			try:
				self.proxy2.free_data_block(block_number)
				self.server2_requests += 1	
			except Exception as err :
				self.server2_error_mask = 1
				# print error message
				print("Error5: Server2 connection failed!")


		
		
	def update_data_block(self, block_number, block_data):
		self.block_number_list_for_server_1 = []
		for i in self.block_number_for_server_1:
			if i not in self.block_number_list_for_server_1:
				self.block_number_list_for_server_1.append(i)
		self.block_number_list_for_server_2 = []
		for i in self.block_number_for_server_2:
			if i not in self.block_number_list_for_server_2:
				self.block_number_list_for_server_2.append(i)

		
		block_number_2 = block_number + 1
		block_number_2 = pickle.dumps(block_number_2)
		block_number = pickle.dumps(block_number)
		block_data = pickle.dumps(block_data)
		if self.server1_error_mask == 0:
			try:
				retVal1 = self.proxy1.update_data_block(block_number, block_data)
				retVal1 = pickle.loads(retVal1)
				self.server1_requests += 1
			except:
				self.server1_error_mask = 1
				print("Error6: Server1 connection failed!")
		if self.server2_error_mask == 0:
			try:
				retVal2 = self.proxy2.update_data_block(block_number, block_data)
				retVal2 = pickle.loads(retVal2)
				self.server2_requests += 1
			except:
				self.server2_error_mask = 1
				print("Error6: Server2 connection failed!")

				print("Error6: Server4 connection failed!")

		if self.server1_error_mask == 0:
			try:
				retVal1 = self.proxy1.update_data_block(block_number_2, block_data)
				retVal1 = pickle.loads(retVal1)
				self.server1_requests += 1
			except:
				self.server1_error_mask = 1
				print("Error6: Server1 connection failed!")
		if self.server2_error_mask == 0:
			try:
				retVal2 = self.proxy2.update_data_block(block_number_2, block_data)
				retVal2 = pickle.loads(retVal2)
				self.server2_requests += 1
			except:
				self.server2_error_mask = 1
				print("Error6: Server2 connection failed!")

		block_number = pickle.loads(block_number)
		block_data = pickle.loads(block_data)
		block_number_2 = pickle.loads(block_number_2)
		
		for i in self.block_number_for_server_1:
			if (i == block_number):
				if self.server1_error_mask == 1:
					print("Block number " + str(block_number) + " is updated by server 2")
					print("Block number " + str(block_number_2) + " is updated by server 2")
					return retVal2
				else:
					print("Block number " + str(block_number) + " is updated by server 1")
					print("Block number " + str(block_number_2) + " is updated by server 2")
					return retVal1

		for i in self.block_number_for_server_2:
			if (i == block_number):
				if self.server2_error_mask == 1:
					print("Block number " + str(block_number) + " is updated by server 1")
				else:
					print("Block number " + str(block_number) + " is updated by server 2")
					return retVal2

		
							
		
	def update_inode_table(self, inode, inode_number):
		inode = pickle.dumps(inode)
		inode_number = pickle.dumps(inode_number)
		if self.server1_error_mask == 0:
			try:
				retVal1 = self.proxy1.update_inode_table(inode, inode_number)
				retVal1 = pickle.loads(retVal1)
				self.server1_requests += 1
			except Exception as err :
				self.server1_error_mask = 1
				# print error message
				print("Error7: Server1 connection failed!")
				print("Trying to update inode table by server2")
		if self.server2_error_mask == 0:
			try:
				retVal2 = self.proxy2.update_inode_table(inode, inode_number)
				retVal2 = pickle.loads(retVal2)
				self.server2_requests += 1
			except Exception as err :
				self.server2_error_mask = 1
				# print error message
				print("Error7: Server2 connection failed!")
				print("Trying to update inode table by server3")



	def status(self):
		try:
			retVal1 = pickle.loads(self.proxy1.status())
			self.server1_requests += 1
			return retVal1
		except Exception as err :
			# print error message
			print("Error8: Server1 connection failed!")
			try:
				retVal2 = pickle.loads(self.proxy2.status())
				self.server2_requests += 1
				return retVal2
			except Exception as err :
				# print error message
				print("Error8: Server2 connection failed!")

		finally:
			if (self.server1_error_mask == 0 and self.server2_error_mask == 0):
				print("Number of Requests handled by Server1 without failure: " + str(self.server1_requests))
				print("Number of Requests handled by Server2 without failure: " + str(self.server2_requests))

			else:
				print("Number of Requests handled by Server1 with 1 fail-stop server: " + str(self.server1_requests))
				print("Number of Requests handled by Server2 with 1 fail-stop server: " + str(self.server2_requests))



		

	def assign_virtual_blk_numbers(self, blk_number_list):
		blk_number_list = [x for x in blk_number_list if x != -1]
		if len(blk_number_list) == 0:
			return -999
		try:

			for i in range(len(blk_number_list)):
				self.free_data_block(blk_number_list[i])

			localBlockNum = self.translate_virtual_blk_numbers(blk_number_list)

			if localBlockNum != -999:
				return localBlockNum
		finally:
			local = []
			local = localBlockNum
			local.append(localBlockNum[-1]+1)

			self.free_data_block(local[-1])
			valid_block_number = []
			while True:
				valid_block_number.append(self.get_valid_data_block())
				if(local[-1] == valid_block_number[-1]):
					break;

			serverBlockNum = self.convert_to_server_blk_numbers(blk_number_list)
			if (len(self.block_number_for_server_1) == 0):
				self.server1_first_block = blk_number_list[0]
				self.block_number_for_server_1 = self.block_number_for_server_1 + serverBlockNum
				self.server1_pointer = self.block_number_for_server_1[-1]
			else:
				if(localBlockNum[0] == self.server1_pointer + 2):
					self.block_number_for_server_1 = self.block_number_for_server_1 + serverBlockNum
					self.server1_pointer = self.block_number_for_server_1[-1]

			if (len(self.block_number_for_server_2) == 0 and blk_number_list[0] == self.server1_first_block + 1):
				self.server2_first_block = blk_number_list[0]
				self.block_number_for_server_2 = self.block_number_for_server_2 + serverBlockNum
				self.server2_pointer = self.block_number_for_server_2[-1]
			else:
				if(localBlockNum[0] == self.server2_pointer + 2):
					self.block_number_for_server_2 = self.block_number_for_server_2 + serverBlockNum
					self.server2_pointer = self.block_number_for_server_2[-1]


	def translate_virtual_blk_numbers(self, blk_number_list):
		blk_number_list = [x for x in blk_number_list if x != -1]
		if len(blk_number_list) == 0:
			return -999
		localBlockNum = []
		
		#In Disk 1
		if((blk_number_list[0] - self.server1_first_block) % 2 == 0):
			i = 0
			length = len(blk_number_list)
			while i < length:
				localBlockNum.append(blk_number_list[0] + 2*i)
				i = i + 1

		if((blk_number_list[0] - self.server2_first_block) % 2 == 0):
			i = 0
			length = len(blk_number_list)
			while i < length:
				localBlockNum.append(blk_number_list[0] + 2*i)
				i = i + 1

		return localBlockNum



	def get_first_four_blocks(self):
		self.counter_get_first_four_blocks += 1
		if self.counter_get_first_four_blocks == 1:
			self.server1_first_block = self.get_valid_data_block()
			self.server2_first_block = self.get_valid_data_block()

			self.free_data_block(self.server1_first_block)
			self.free_data_block(self.server2_first_block)


	def convert_to_server_blk_numbers(self, blk_number_list):
		blk_number_list = [x for x in blk_number_list if x != -1]
		if len(blk_number_list) == 0:
			return -999
		localBlockNum = []

		#In Disk 1
		if((blk_number_list[0] - self.server1_first_block) % 2 == 0):
			i = 0
			length = len(blk_number_list)
			while i < length:
				localBlockNum.append(blk_number_list[0] + 2*i)
				i = i + 1

		if((blk_number_list[0] - self.server2_first_block) % 2 == 0):
			i = 0
			length = len(blk_number_list)
			while i < length:
				localBlockNum.append(blk_number_list[0] + 2*i)
				i = i + 1
		return localBlockNum

			
