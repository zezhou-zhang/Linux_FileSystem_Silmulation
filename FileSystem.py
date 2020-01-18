import MemoryInterface, AbsolutePathNameLayer

def Initialize_My_FileSystem():
    MemoryInterface.Initialize_My_FileSystem()
    AbsolutePathNameLayer.AbsolutePathNameLayer().new_entry('/', 1)

#HANDLE TO ABSOLUTE PATH NAME LAYER
interface = AbsolutePathNameLayer.AbsolutePathNameLayer()

class FileSystemOperations():

    #MAKES NEW DIRECTORY
    def mkdir(self, path):
        interface.new_entry(path, 1)

    #CREATE FILE
    def create(self, path):
        interface.new_entry(path, 0)
        

    #WRITE TO FILE
    def write(self, path, data, offset=0):
        interface.write(path, offset, data)
      

    #READ
    def read(self, path, offset=0, size=-1):
        read_buffer = interface.read(path, offset, size)
        if read_buffer != -1: print(path + " : " + read_buffer)

    
    #DELETE
    def rm(self, path):
        interface.unlink(path)


    #MOVING FILE
    def mv(self, old_path, new_path):
        interface.mv(old_path, new_path)


    #CHECK STATUS
    def status(self):
        print(MemoryInterface.status())

    def command(self,a):
        if(a[0] != '$'):
            print("Please start your command with $")
            return -999, -999
        else:
            if(a[1] != ' '):
                print("Please follow $ with space")
                return -999, -999
            else:
            	if a[2:len(a)] == 'status':
            		command = 'status'
            		instruction = 0
            		return command, instruction
                for i in range(2,len(a)):
                    if(a[i] == ' '):
                        command = a[2:i]
                        instruction = a[i+1:]
                        return command,instruction
                        break;


if __name__ == '__main__':
    #DO NOT MODIFY THIS
    while True:
        raid = raw_input("Choose the type of RAID (1 or 5): ")
        print(raid)
        if(int(raid) == 5):
            print("RAID 5 Method is applied!")
            MemoryInterface.RAID_5()
            break;
        if(int(raid) == 1):
            print("RAID 1 Method is applied!")
            MemoryInterface.RAID_1()
            break;
        else:
            print("Wrong Number Typed. Please choose either 1 or 5.")
    Initialize_My_FileSystem()
    my_object = FileSystemOperations()

    #=======================INITIAL START FOR RUNNING TEST=====================
    #IF YOU WANT TO TYPE FROM BEGINNING, COMMENT THIS AREA
    my_object.mkdir("/A")
    my_object.mkdir("/B")
    my_object.mkdir("/C")
    my_object.mkdir("/D")
    my_object.create("/A/1.txt")
    my_object.create("/B/2.txt")
    my_object.create("/C/3.txt")
    my_object.create("/D/4.txt")
    'WRITING A INITIAL STRING TO FILE'
    my_object.write("/A/1.txt", "012345678", 0)
    my_object.read("/A/1.txt", 0 , 9)
    'READ FILE FROM OFFSET'
    my_object.read("/A/1.txt", 2 , 2)
    'WRITE IN THE MIDDLE OF FILE'
    my_object.write("/A/1.txt", "write", 1)
    my_object.read("/A/1.txt", 0 , 10)
    'WRITE ATTEMPT BEYOND FILE'
    my_object.write("/A/1.txt", "beyond", 12)
    'WRITE TO APPEND FILE'
    my_object.write("/A/1.txt", "append", 6)
    my_object.read("/A/1.txt", 0 , 16)
    'WRITE TO ANOTHER 3 FILES'
    my_object.write("/B/2.txt", "abcdefg", 0)
    my_object.read("/B/2.txt", 0 , 8)
    my_object.write("/C/3.txt", "987654321", 0)
    my_object.read("/C/3.txt", 0 , 10)
    my_object.write("/D/4.txt", "7777777", 0)
    my_object.read("/D/4.txt", 0 , 8)
    #=======================INITIAL START FOR RUNNING TEST=====================
    while True:
        g = raw_input("Enter your command : ") 
        if g == 'exit':
            break
        else:
            command,instr =  my_object.command(g)
            if command == -999 or instr == -999:
                continue
            if command == 'mkdir':
                my_object.mkdir(instr)
            if command == 'create':
                my_object.create(instr)
            if command == 'write':
                for i in range(len(instr)):
                    if(instr[i] == ' '):
                        location = instr[:i]
                        print(location)
                        rest = instr[i+1:]
                        break;
                for i in range(len(rest)):
                    if(rest[i] == ' '):
                        data = rest[:i]
                        print(data)
                        offset = rest[i+1:]
                        print(offset)
                my_object.write(location, data, int(offset))
            if command == 'read':
                for i in range(len(instr)):
                    if(instr[i] == ' '):
                        location = instr[:i]
                        print(location)
                        rest = instr[i+1:]
                        break;
                for i in range(len(rest)):
                    if(rest[i] == ' '):
                        offset = rest[:i]
                        print(offset)
                        length = rest[i+1:]
                        print(length)
                my_object.read(location, int(offset), int(length))

            if command == 'mv':
                for i in range(len(instr)):
                    if(instr[i] == ' '):
                        location1 = instr[:i]
                        print(location1)
                        location2 = instr[i+1:]
                        print(location2)
                my_object.mv(location1, location2)

            if command == 'rm':
                my_object.rm(instr)

            if command == 'status':
                my_object.status()

    print("Final status:")
    my_object.status()
