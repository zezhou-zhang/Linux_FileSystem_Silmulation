# SKELETON CODE FOR CLIENT STUB HW4
#import xmlrpc.client, config, pickle
# SKELETON CODE FOR CLIENT STUB HW4
import xmlrpclib, config, pickle
import binascii,time
class client_stub():

	def __init__(self):
		self.proxy1 = xmlrpclib.ServerProxy("http://localhost:8000/")
		self.proxy2 = xmlrpclib.ServerProxy("http://localhost:8001/")
		self.proxy3 = xmlrpclib.ServerProxy("http://localhost:8002/")
		self.proxy4 = xmlrpclib.ServerProxy("http://localhost:8003/")
		self.counter_get_first_four_blocks = 0
		self.block_number_for_server_1 = []
		self.block_number_for_server_2 = []
		self.block_number_for_server_3 = []
		self.block_number_for_server_4 = []
		self.serverNum = []
		self.server1_pointer = 0
		self.server2_pointer = 0
		self.server3_pointer = 0
		self.server4_pointer = 0
		self.server1_first_block = 0
		self.server2_first_block = 0
		self.server3_first_block = 0
		self.server4_first_block = 0
		self.server1_first_parity = 0
		self.server2_first_parity = 0
		self.server3_first_parity = 0
		self.server4_first_parity = 0
		self.parity_block_list = []
		self.server1_error_mask = 0
		self.server2_error_mask = 0
		self.server3_error_mask = 0
		self.server4_error_mask = 0
		self.server1_requests = 0
		self.server2_requests = 0
		self.server3_requests = 0
		self.server4_requests = 0

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
		try :
			retVal = pickle.loads(self.proxy3.Initialize())
			self.server3_requests += 1
		except Exception as err :
			# print error message
			print("Error1: Initialization failed!")
		try :
			retVal = pickle.loads(self.proxy4.Initialize())
			self.server4_requests += 1
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

			try:
				retVal3 = self.proxy3.inode_number_to_inode(inode_number)
				retVal3 = pickle.loads(retVal3)
				self.server3_requests += 1
			except Exception as err :
				retVal3 = -999
				# print error message
				self.server3_error_mask == 1
				print("Error2: Server3 connection failed!")
			try:
				retVal4 = self.proxy4.inode_number_to_inode(inode_number)
				retVal4 = pickle.loads(retVal4)
				self.server4_requests += 1
			except Exception as err :
				retVal4 = -999
				self.server4_error_mask == 1
				# print error message
				print("Error2: Server4 connection failed!")
			
				
		if retVal1 != -999:
			return retVal1
		if retVal2 != -999:
			return retVal2
		if retVal3 != -999:
			return retVal3
		if retVal4 != -999:
			return retVal4
	

	def get_data_block(self, block_number):
		#IF DATA BLOCK IN DISK ONE
		for i in self.block_number_list_for_server_1:
			if (i == block_number):
				block_number = pickle.dumps(block_number)
				#IF SERVER1 NOT FAIL
				if self.server1_error_mask == 0:
					try:
						retVal1 = ''.join(self.proxy1.get_data_block(block_number))
						retVal1 = pickle.loads(retVal1)
						self.server1_requests += 1
					except Exception as err :
						#IF SERVER1 FAIL, USE SERVER2 TO GET DATA
						self.server1_error_mask = 1
						# print error message
						print("Error3: Server1 connection failed!")
						print("Trying to use Server2 to get data...")
						retVal2 = ''.join(self.proxy2.get_data_block(block_number))
						retVal2 = pickle.loads(retVal2)
						self.server2_requests += 1
				#KEEP USING SERVER2 WHEN SERVER1 IS DOWN
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
					#IF DATA IS CORRUPTED IN SERVER1
					else:
						print("Data in this server1 is corrupted!")
						print("Trying to recover the data...")
						return self.recover_from_parity(block_number,self.server1_first_parity)
				else:
					if(retVal2 != -999):
						print("The data now resides in server2.")
						time.sleep(2.5)
						return retVal2
					else:
						print("Data in server1 is corrupted!")
						print("Trying to recover the data...")
						return self.recover_from_parity(block_number,self.server1_first_parity)
					
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
						retVal3 = ''.join(self.proxy3.get_data_block(block_number))
						retVal3 = pickle.loads(retVal3)
						self.server3_requests += 1
				else:
					retVal3 = ''.join(self.proxy3.get_data_block(block_number))
					retVal3 = pickle.loads(retVal3)
					self.server3_requests += 1
				block_number = pickle.loads(block_number)

				if self.server2_error_mask == 0:
					if(retVal2 != -999):
						time.sleep(2.5)
						print("The data resides in server2.")
						return retVal2
					else:
						print("Data in this server2 is corrupted!")
						print("Trying to recover the data...")
						time.sleep(5)
						return self.recover_from_parity(block_number,self.server2_first_parity)	
				else:
					if(retVal3 != -999):
						time.sleep(2.5)
						print("The data now resides in server3.")
						return retVal3
					else:
						print("Data in server2 is corrupted!")
						print("Trying to recover the data...")
						time.sleep(2.5)
						return self.recover_from_parity(block_number,self.server2_first_parity)

		for i in self.block_number_list_for_server_3:
			if (i == block_number):
				block_number = pickle.dumps(block_number)
				if self.server3_error_mask == 0:
					try:
						retVal3 = ''.join(self.proxy3.get_data_block(block_number))
						retVal3 = pickle.loads(retVal3)
						self.server3_requests += 1
					except Exception as err :
						self.server3_error_mask = 1
						# print error message
						print("Error3: Server3 connection failed!")
						print("Trying to use Server4 to get data...")
						retVal4 = ''.join(self.proxy4.get_data_block(block_number))
						retVal4= pickle.loads(retVal4)
						self.server4_requests += 1
				else:
					retVal4 = ''.join(self.proxy4.get_data_block(block_number))
					retVal4= pickle.loads(retVal4)
					self.server4_requests += 1

				block_number = pickle.loads(block_number)

				if self.server3_error_mask == 0:
					if(retVal3 != -999):
						print("The data resides in server3.")
						time.sleep(2.5)
						return retVal3
					else:
						print("Data in this server3 is corrupted!")
						print("Trying to recover the data...")
						time.sleep(2.5)
						return self.recover_from_parity(block_number,self.server3_first_parity)
				else:	
					if(retVal4 != -999):
						print("The data now resides in server4.")
						time.sleep(2.5)
						return retVal4
					else:
						
						print("Data in server3 is corrupted!")
						print("Trying to recover the data...")
						time.sleep(2.5)
						return self.recover_from_parity(block_number,self.server3_first_parity)

		for i in self.block_number_list_for_server_4:
			if (i == block_number):
				block_number = pickle.dumps(block_number)
				if self.server4_error_mask == 0:
					try:
						retVal4 = ''.join(self.proxy4.get_data_block(block_number))
						retVal4 = pickle.loads(retVal4)
						self.server4_requests += 1
					except Exception as err :
						self.server4_error_mask = 1
						# print error message
						print("Error3: Server4 connection failed!")
						print("Trying to use Server1 to get data...")
						retVal1 = ''.join(self.proxy1.get_data_block(block_number))
						retVal1= pickle.loads(retVal1)
						self.server1_requests += 1
				else:
					retVal1 = ''.join(self.proxy1.get_data_block(block_number))
					retVal1= pickle.loads(retVal1)
					self.server1_requests += 1

				block_number = pickle.loads(block_number)

				if self.server4_error_mask == 0:
					if(retVal4 != -999):
						print("The data resides in server4.")
						time.sleep(2.5)
						return retVal4
					else:
						print("Data in this server4 is corrupted!")
						print("Trying to recover the data...")
						time.sleep(2.5)
						return self.recover_from_parity(block_number,self.server4_first_parity)	
				else:
					if(retVal1 != -999):
						print("The data now resides in server1.")
						time.sleep(2.5)
						return retVal1
					else:
						print("Data in server4 is corrupted!")
						print("Trying to recover the data...")
						time.sleep(2.5)
						return self.recover_from_parity(block_number,self.server4_first_parity)	


	def get_valid_data_block(self):
		retVal1 = -999
		retVal2 = -999
		retVal3 = -999
		retVal4 = -999
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
		if self.server3_error_mask == 0:
			try:
				retVal3 = self.proxy3.get_valid_data_block()
				retVal3 = pickle.loads(retVal3)
				self.server3_requests += 1
				
			except:
				self.server3_error_mask = 1
				retVal3 = -999
				print("Error4: Server3 connection failed!")
		if self.server4_error_mask == 0:
			try:
				retVal4 = self.proxy4.get_valid_data_block()
				retVal4 = pickle.loads(retVal4)
				self.server4_requests += 1
			
			except:
				self.server4_error_mask = 1
				retVal4 = -999
				print("Error4: Server4 connection failed!")

		if retVal1 != -999:
			return retVal1
		if retVal2 != -999:
			return retVal2
		if retVal3 != -999:
			return retVal3
		if retVal4 != -999:
			return retVal4

		
		

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
		if self.server3_error_mask == 0:
			try:
				self.proxy3.free_data_block(block_number)
				self.server3_requests += 1	
			except Exception as err :
				self.server3_error_mask = 1
				# print error message
				print("Error5: Server3 connection failed!")
		if self.server4_error_mask == 0:
			try:
				self.proxy4.free_data_block(block_number)
				self.server4_requests += 1	
			except Exception as err :
				self.server4_error_mask = 1
				# print error message
				print("Error5: Server4 connection failed!")

		
		
	def update_data_block(self, block_number, block_data):
		self.block_number_list_for_server_1 = []
		for i in self.block_number_for_server_1:
			if i not in self.block_number_list_for_server_1:
				self.block_number_list_for_server_1.append(i)
		self.block_number_list_for_server_2 = []
		for i in self.block_number_for_server_2:
			if i not in self.block_number_list_for_server_2:
				self.block_number_list_for_server_2.append(i)
		self.block_number_list_for_server_3 = []
		for i in self.block_number_for_server_3:
			if i not in self.block_number_list_for_server_3:
				self.block_number_list_for_server_3.append(i)
		self.block_number_list_for_server_4 = []
		for i in self.block_number_for_server_4:
			if i not in self.block_number_list_for_server_4:
				self.block_number_list_for_server_4.append(i)
		
		#BEFORE UPDATING THE BLOCK, UPDATE THE PARITY BLOCK FIRSTf
		for i in self.block_number_for_server_1:
			if (i == block_number):
				self.attempt_to_update_parity_block(block_number,self.server1_first_parity,block_data)
		for i in self.block_number_for_server_2:
			if (i == block_number):
				self.attempt_to_update_parity_block(block_number,self.server2_first_parity,block_data)
		for i in self.block_number_for_server_3:
			if (i == block_number):
				self.attempt_to_update_parity_block(block_number,self.server3_first_parity,block_data)
		for i in self.block_number_for_server_4:
			if (i == block_number):
				self.attempt_to_update_parity_block(block_number,self.server4_first_parity,block_data)
		
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
		if self.server3_error_mask == 0:
			try:
				retVal3 = self.proxy3.update_data_block(block_number, block_data)
				retVal3 = pickle.loads(retVal3)
				self.server3_requests += 1
			except:
				self.server3_error_mask = 1
				print("Error6: Server3 connection failed!")
		if self.server4_error_mask == 0:
			try:
				retVal4 = self.proxy4.update_data_block(block_number, block_data)
				retVal4 = pickle.loads(retVal4)
				self.server4_requests += 1
			except:
				self.server4_error_mask = 1
				print("Error6: Server4 connection failed!")

		block_number = pickle.loads(block_number)
		block_data = pickle.loads(block_data)

		#UPDATE DATA BLOCK TAHT IS IN DISK ONE BY USING SERVER1
		for i in self.block_number_for_server_1:
			if (i == block_number):
				if self.server1_error_mask == 1:
					print("Block number " + str(block_number) + " is updated by server 2")
					#UPDATE PARITY BLOCK BY USING SERVER2 WHEN SERVER1 IS DOWN
					self.update_parity_block(block_number,self.server1_first_parity)
					return retVal2
				else:
					print("Block number " + str(block_number) + " is updated by server 1")
					self.update_parity_block(block_number,self.server1_first_parity)
					return retVal1

					
		for i in self.block_number_for_server_2:
			if (i == block_number):
				if self.server2_error_mask == 1:
					print("Block number " + str(block_number) + " is updated by server 3")
					self.update_parity_block(block_number,self.server2_first_parity)
					return retVal3
				else:
					print("Block number " + str(block_number) + " is updated by server 2")
					self.update_parity_block(block_number,self.server2_first_parity)
					return retVal2

		for i in self.block_number_for_server_3:
			if (i == block_number):
				if self.server3_error_mask == 1:
					print("Block number " + str(block_number) + " is updated by server 4")
					self.update_parity_block(block_number,self.server3_first_parity)
					return retVal4
				else:
					print("Block number " + str(block_number) + " is updated by server 3")
					self.update_parity_block(block_number,self.server3_first_parity)
					return retVal3

						
		for i in self.block_number_for_server_4:
			if (i == block_number):
				if self.server4_error_mask == 1:
					print("Block number " + str(block_number) + " is updated by server 1")
					self.update_parity_block(block_number,self.server4_first_parity)
					return retVal1
				else:
					print("Block number " + str(block_number) + " is updated by server 4")
					self.update_parity_block(block_number,self.server4_first_parity)
					return retVal4
							
		
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
		if self.server3_error_mask == 0:
			try:
				retVal3 = self.proxy3.update_inode_table(inode, inode_number)
				retVal3 = pickle.loads(retVal3)
				self.server3_requests += 1
			except Exception as err :
				self.server3_error_mask = 1
				# print error message
				print("Error7: Server3 connection failed!")
				print("Trying to update inode table by server4")
		if self.server4_error_mask == 0:
			try:
				retVal4 = self.proxy4.update_inode_table(inode, inode_number)
				retVal4 = pickle.loads(retVal4)
				self.server4_requests += 1
			except Exception as err :
				self.server4_error_mask = 1
				# print error message
				print("Error7: Server4 connection failed!")
				print("Trying to update inode table by server1")


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
				try:
					retVal3 = pickle.loads(self.proxy3.status())
					self.server3_requests += 1
					return retVal3
				except Exception as err :
					# print error message
					print("Error8: Server3 connection failed!")
					try:
						retVal4 = pickle.loads(self.proxy4.status())
						self.server4_requests += 1
						return retVal4
					except Exception as err :
						# print error message
						print("Error8: Server4 connection failed!")
		finally:
			if (self.server1_error_mask == 0 and self.server2_error_mask == 0 
					and self.server3_error_mask == 0 and self.server4_error_mask == 0):
				print("Number of Requests handled by Server1 without failure: " + str(self.server1_requests))
				print("Number of Requests handled by Server2 without failure: " + str(self.server2_requests))
				print("Number of Requests handled by Server3 without failure: " + str(self.server3_requests))
				print("Number of Requests handled by Server4 without failure: " + str(self.server4_requests))
			else:
				print("Number of Requests handled by Server1 with 1 fail-stop server: " + str(self.server1_requests))
				print("Number of Requests handled by Server2 with 1 fail-stop server: " + str(self.server2_requests))
				print("Number of Requests handled by Server3 with 1 fail-stop server: " + str(self.server3_requests))
				print("Number of Requests handled by Server4 with 1 fail-stop server: " + str(self.server4_requests))


		

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
			for i in range(len(localBlockNum)):
				valid_block_number = []
				while True:
					valid_block_number.append(self.get_valid_data_block())
					if(localBlockNum[i] == valid_block_number[-1]):
						for i in range(len(valid_block_number) - 1):
							self.free_data_block(valid_block_number[i])
						break;
			serverBlockNum = self.convert_to_server_blk_numbers(blk_number_list)
			if (len(self.block_number_for_server_1) == 0):
				self.server1_first_block = blk_number_list[0]
				self.block_number_for_server_1 = self.block_number_for_server_1 + serverBlockNum
				self.server1_pointer = self.block_number_for_server_1[-1]
			else:
				if(localBlockNum[0] == self.server1_pointer + 4 or localBlockNum[0] == self.server1_pointer + 8):
					self.block_number_for_server_1 = self.block_number_for_server_1 + serverBlockNum
					self.server1_pointer = self.block_number_for_server_1[-1]

			if (len(self.block_number_for_server_2) == 0 and blk_number_list[0] == self.server1_first_block + 1):
				self.server2_first_block = blk_number_list[0]
				self.block_number_for_server_2 = self.block_number_for_server_2 + serverBlockNum
				self.server2_pointer = self.block_number_for_server_2[-1]
			else:
				if(localBlockNum[0] == self.server2_pointer + 4 or localBlockNum[0] == self.server2_pointer + 8):
					self.block_number_for_server_2 = self.block_number_for_server_2 + serverBlockNum
					self.server2_pointer = self.block_number_for_server_2[-1]

			if (len(self.block_number_for_server_3) == 0 and blk_number_list[0] == self.server1_first_block + 2):
				self.server3_first_block = blk_number_list[0]
				self.block_number_for_server_3 = self.block_number_for_server_3 + serverBlockNum
				self.server3_pointer = self.block_number_for_server_3[-1]
			else:
				if(localBlockNum[0] == self.server3_pointer + 4 or localBlockNum[0] == self.server3_pointer + 8):
					self.block_number_for_server_3 = self.block_number_for_server_3 + serverBlockNum
					self.server3_pointer = self.block_number_for_server_3[-1]

			if (len(self.block_number_for_server_4) == 0 and blk_number_list[0] == self.server1_first_block + 3):
				self.server4_first_block = blk_number_list[0]
				self.block_number_for_server_4 = self.block_number_for_server_4 + serverBlockNum
				self.server4_pointer = self.block_number_for_server_4[-1]
			else:
				if(localBlockNum[0] == self.server4_pointer + 4 or localBlockNum[0] == self.server4_pointer + 8):
					self.block_number_for_server_4.append(blk_number_list[0])
					self.block_number_for_server_4 = self.block_number_for_server_4 + serverBlockNum
					self.server4_pointer = self.block_number_for_server_2[-1]
	#TRANSLATE THE VIRTUAL BLOCK TO PYHSICAL BLOCK
	def translate_virtual_blk_numbers(self, blk_number_list):
		blk_number_list = [x for x in blk_number_list if x != -1]
		if len(blk_number_list) == 0:
			return -999
		localBlockNum = []
		
		self.server1_first_parity = self.server1_first_block + 12
		self.server2_first_parity = self.server2_first_block + 8
		self.server3_first_parity = self.server3_first_block + 4
		self.server4_first_parity = self.server4_first_block

		#In Disk 1
		if((blk_number_list[0] - self.server1_first_block) % 4 == 0):
			if(blk_number_list[0] == self.server1_first_parity):
				blk_number_list[0] = self.server1_first_parity + 4
			i = 0
			length = len(blk_number_list)
			while i < length:
				if((blk_number_list[0]+4*i - self.server1_first_parity)%16 == 0):
						localBlockNum.append(blk_number_list[0] + 4*(i+1))
						i = i+1
						length = length + 1
				else:
					localBlockNum.append(blk_number_list[0] + 4*i)
				i = i + 1

		if((blk_number_list[0] - self.server2_first_block) % 4 == 0):
			if(blk_number_list[0] == self.server2_first_parity):
				blk_number_list[0] = self.server2_first_parity + 4
			i = 0
			length = len(blk_number_list)
			while i < length:
				if((blk_number_list[0]+4*i - self.server2_first_parity)%16 == 0):
						localBlockNum.append(blk_number_list[0] + 4*(i+1))
						i = i+1
						length = length + 1
				else:
					localBlockNum.append(blk_number_list[0] + 4*i)
				i = i + 1

		if((blk_number_list[0] - self.server3_first_block) % 4 == 0):
			if(blk_number_list[0] == self.server3_first_parity):
				blk_number_list[0] = self.server3_first_parity + 4
			i = 0
			length = len(blk_number_list)
			while i < length:
				if((blk_number_list[0]+4*i - self.server3_first_parity)%16 == 0):
						localBlockNum.append(blk_number_list[0] + 4*(i+1))
						i = i+1
						length = length + 1
				else:
					localBlockNum.append(blk_number_list[0] + 4*i)
				i = i + 1

		if((blk_number_list[0] - self.server4_first_block) % 4 == 0):
			if(blk_number_list[0] == self.server4_first_parity):
				blk_number_list[0] = self.server4_first_parity + 4
			i = 0
			length = len(blk_number_list)
			while i < length:
				if((blk_number_list[0]+4*i - self.server4_first_parity)%16 == 0):
						localBlockNum.append(blk_number_list[0] + 4*(i+1))
						i = i+1
						length = length + 1
				else:
					localBlockNum.append(blk_number_list[0] + 4*i)
				i = i + 1

		return localBlockNum



	def get_first_four_blocks(self):
		self.counter_get_first_four_blocks += 1
		if self.counter_get_first_four_blocks == 1:
			self.server1_first_block = self.get_valid_data_block()
			self.server2_first_block = self.get_valid_data_block()
			self.server3_first_block = self.get_valid_data_block()
			self.server4_first_block = self.get_valid_data_block()
			self.free_data_block(self.server1_first_block)
			self.free_data_block(self.server2_first_block)
			self.free_data_block(self.server3_first_block)
			self.free_data_block(self.server4_first_block)

	def convert_to_server_blk_numbers(self, blk_number_list):
		blk_number_list = [x for x in blk_number_list if x != -1]
		if len(blk_number_list) == 0:
			return -999
		localBlockNum = []
		self.server1_first_parity = self.server1_first_block + 12
		self.server2_first_parity = self.server2_first_block + 8
		self.server3_first_parity = self.server3_first_block + 4
		self.server4_first_parity = self.server4_first_block

		#In Disk 1
		if((blk_number_list[0] - self.server1_first_block) % 4 == 0):
			i = 0
			length = len(blk_number_list)
			while i < length:
				if((blk_number_list[0]+4*i - self.server1_first_parity)%16 == 0):
						localBlockNum.append(blk_number_list[0] + 4*(i))
						localBlockNum.append(blk_number_list[0] + 4*(i+1))
						i = i+1
						length = length + 1
				else:
					localBlockNum.append(blk_number_list[0] + 4*i)
				i = i + 1

		if((blk_number_list[0] - self.server2_first_block) % 4 == 0):
			i = 0
			length = len(blk_number_list)
			while i < length:
				if((blk_number_list[0]+4*i - self.server2_first_parity)%16 == 0):
						localBlockNum.append(blk_number_list[0] + 4*(i))
						localBlockNum.append(blk_number_list[0] + 4*(i+1))
						i = i+1
						length = length + 1
				else:
					localBlockNum.append(blk_number_list[0] + 4*i)
				i = i + 1

		if((blk_number_list[0] - self.server3_first_block) % 4 == 0):
			i = 0
			length = len(blk_number_list)
			while i < length:
				if((blk_number_list[0]+4*i - self.server3_first_parity)%16 == 0):
						localBlockNum.append(blk_number_list[0] + 4*(i))
						localBlockNum.append(blk_number_list[0] + 4*(i+1))
						i = i+1
						length = length + 1
				else:
					localBlockNum.append(blk_number_list[0] + 4*i)
				i = i + 1

		if((blk_number_list[0] - self.server4_first_block) % 4 == 0):
			i = 0
			length = len(blk_number_list)
			while i < length:
				if((blk_number_list[0]+4*i - self.server4_first_parity)%16 == 0):
						localBlockNum.append(blk_number_list[0] + 4*(i))
						localBlockNum.append(blk_number_list[0] + 4*(i+1))
						i = i+1
						length = length + 1
				else:
					localBlockNum.append(blk_number_list[0] + 4*i)
				i = i + 1

		return localBlockNum

	def update_parity_block(self,block_number,server_first_parity):

		if ((block_number - 4 - server_first_parity)%16 == 0) and (block_number - 4 >= self.server1_first_block):
			parity_block_number = block_number - 4 
			valid_block_number = []
			if parity_block_number not in self.parity_block_list:
				while True:
					valid_block_number.append(self.get_valid_data_block())
					if(parity_block_number == valid_block_number[-1]):
						self.parity_block_list.append(parity_block_number)
						for i in range(len(valid_block_number) - 1):
							self.free_data_block(valid_block_number[i])
						break;
			print("Waiting to write parity...")
			time.sleep(1)
			if server_first_parity == self.server1_first_parity:
				try:
					parity_data = self.XOR_Method(parity_block_number+1,parity_block_number+2,parity_block_number+3)
					self.update_data_block(parity_block_number, parity_data)
					print("Parity block number " + str(parity_block_number) + " is updated by server1")
				except:
					print("Parity block number " + str(parity_block_number) + " does not have enough data to update")

			if server_first_parity == self.server2_first_parity:
				try:
					parity_data = self.XOR_Method(parity_block_number-1,parity_block_number+1,parity_block_number+2)
					self.update_data_block(parity_block_number, parity_data)
					print("Parity block number " + str(parity_block_number) + " is updated by server2")
				except:
					print("Parity block number " + str(parity_block_number) + " does not have enough data to update")

			if server_first_parity == self.server3_first_parity:
				try:
					parity_data = self.XOR_Method(parity_block_number-2,parity_block_number-1,parity_block_number+1)
					self.update_data_block(parity_block_number, parity_data)
					print("Parity block number " + str(parity_block_number) + " is updated by server3")
				except:
					print("Parity block number " + str(parity_block_number) + " does not have enough data to update")

			if server_first_parity == self.server4_first_parity:
				try:
					parity_data = self.XOR_Method(parity_block_number-3,parity_block_number-2,parity_block_number-1)
					self.update_data_block(parity_block_number, parity_data)
					print("Parity block number " + str(parity_block_number) + " is updated by server4")
				except:
					print("Parity block number " + str(parity_block_number) + " does not have enough data to update")
		
	#UPDATE THE PARITY BLOCK BEFORE THE BLOCK IS UPDATED
	def attempt_to_update_parity_block(self,block_number,server_first_parity,block_data):
		#FIND PARITY BLOCK BASED ON THE BLOCK BEING UPDATED		
		if server_first_parity == self.server1_first_parity:
			if ((block_number - self.server1_first_block) % 16)//4 == 3:
				parity_block_number = block_number + 0
			if ((block_number - self.server1_first_block) % 16)//4 == 2:
				parity_block_number = block_number + 1
			if ((block_number - self.server1_first_block) % 16)//4 == 1:
				parity_block_number = block_number + 2
			if ((block_number - self.server1_first_block) % 16)//4 == 0:
				parity_block_number = block_number + 3
		if server_first_parity == self.server2_first_parity:
			if ((block_number - self.server2_first_block) % 16)//4 == 3:
				parity_block_number = block_number - 1
			if ((block_number - self.server2_first_block) % 16)//4 == 2:
				parity_block_number = block_number + 0
			if ((block_number - self.server2_first_block) % 16)//4 == 1:
				parity_block_number = block_number + 1
			if ((block_number - self.server2_first_block) % 16)//4 == 0:
				parity_block_number = block_number + 2
		if server_first_parity == self.server3_first_parity:
			if ((block_number - self.server3_first_block) % 16)//4 == 3:
				parity_block_number = block_number - 2
			if ((block_number - self.server3_first_block) % 16)//4 == 2:
				parity_block_number = block_number - 1
			if ((block_number - self.server3_first_block) % 16)//4 == 1:
				parity_block_number = block_number + 0
			if ((block_number - self.server3_first_block) % 16)//4 == 0:
				parity_block_number = block_number + 1
		if server_first_parity == self.server4_first_parity:
			if ((block_number - self.server4_first_block) % 16)//4 == 3:
				parity_block_number = block_number - 3
			if ((block_number - self.server4_first_block) % 16)//4 == 2:
				parity_block_number = block_number - 2
			if ((block_number - self.server4_first_block) % 16)//4 == 1:
				parity_block_number = block_number - 1
			if ((block_number - self.server4_first_block) % 16)//4 == 0:
				parity_block_number = block_number + 0
		print("Waiting to update the parity data...")
		time.sleep(1)
		try:
			string1 = self.get_data_block(block_number)
			new_data= []
			lst = (i.rstrip('\x00') for i in string1)
			for j in lst: 
				new_data.append(j)
			string1 = ''.join(new_data)

			string2 = self.get_data_block(parity_block_number)
			new_data= []
			lst = (i.rstrip('\x00') for i in string2)
			for j in lst: 
				new_data.append(j)
			string2 = ''.join(new_data)

			string3 = block_data
			a = int(binascii.hexlify(string1),16)
			b = int(binascii.hexlify(string2),16)
			c = int(binascii.hexlify(string3),16)
			d = a^b^c
			n= bin(d)
			word = int(n, 2)
			parity_data = binascii.unhexlify('%x' % word)
			self.update_data_block(parity_block_number, parity_data)
			print("Parity block number " + str(parity_block_number) + " is updated")
		except:
			print("Parity block number " + str(parity_block_number) + " so far does not have enough data to update")


	#TRYING TO RECOVER THE BLOCK BY PARITY BLOCK
	def recover_from_parity(self,block_number,server_first_parity):
		if server_first_parity == self.server1_first_parity:
			#TRYING TO FIND PARITY BLOCK IN SERVER1 BASED ON THE CURRENT BLOCK NUMBER
			if ((block_number - self.server1_first_block) % 16)//4 == 3:
				parity_block_number = block_number
				print("Try to recover the parity block number" + str(parity_block_number))

			recovery_data = self.XOR_Method(block_number+1,block_number+2,block_number+3)
			#WHEN THERE IS A PARITY BLOCK TO RECOVER DATA
			if recovery_data != -999:
				print("The data in block number "+str(block_number) +" is recovered!")
				return recovery_data
			#WHEN THERE IS NO PARITY BLOCK UPDATED
			else:
				print("The data in block number "+str(block_number) +" does not have parity block to recover!")

		if server_first_parity == self.server2_first_parity:
			if ((block_number - self.server1_first_block) % 16)//4 == 2:
				parity_block_number = block_number
				print("Try to recover the parity block number" + str(parity_block_number))
			recovery_data = self.XOR_Method(block_number-1,block_number+1,block_number+2)
			if recovery_data != -999:
				print("The data in block number "+str(block_number) +" is recovered!")
				return recovery_data
			else:
				print("The data in block number "+str(block_number) +" does not have parity block to recover!")

		if server_first_parity == self.server3_first_parity:
			if ((block_number - self.server3_first_block) % 16)//4 == 1:
				parity_block_number = block_number
				print("Try to recover the parity block number" + str(parity_block_number))

			recovery_data = self.XOR_Method(block_number-2,block_number-1,block_number+1)
			if recovery_data != -999:
				print("The data in block number "+str(block_number) +" is recovered!")
				return recovery_data
			else:
				print("The data in block number "+str(block_number) +" does not have parity block to recover!")

		if server_first_parity == self.server4_first_parity:
			if ((block_number - self.server4_first_block) % 16)//4 == 0:
				parity_block_number = block_number
				print("Try to recover the parity block number" + str(parity_block_number))

			recovery_data = self.XOR_Method(block_number-3,block_number-2,block_number-1)
			if recovery_data != -999:
				print("The data in block number "+str(block_number) +" is recovered!")
				return recovery_data
			else:
				print("The data in block number "+str(block_number) +" does not have parity block to recover!")



	#XOR METHOD THAT CAN APPLY XOR FOR THREE DATA BLOCKS AND RETURN THE OUTPUT DATA
	def XOR_Method(self,block_number_1,block_number_2,block_number_3):
		try:
			string1 = self.get_data_block(block_number_1)
			new_data= []
			lst = (i.rstrip('\x00') for i in string1)
			for j in lst: 
				new_data.append(j)
			string1 = ''.join(new_data)
			string2 = self.get_data_block(block_number_2)
			new_data= []
			lst = (i.rstrip('\x00') for i in string2)
			for j in lst: 
				new_data.append(j)
			string2 = ''.join(new_data)
			string3 = self.get_data_block(block_number_3)
			new_data= []
			lst = (i.rstrip('\x00') for i in string3)
			for j in lst: 
				new_data.append(j)
			string3 = ''.join(new_data)
			a = int(binascii.hexlify(string1),16)
			b = int(binascii.hexlify(string2),16)
			c = int(binascii.hexlify(string3),16)
			d = a^b^c
			n= bin(d)
			word = int(n, 2)
			reconstructed_data = binascii.unhexlify('%x' % word)
			return reconstructed_data
		except:
			print("No enough data for performing XOR_Method!")
			return -999
			
